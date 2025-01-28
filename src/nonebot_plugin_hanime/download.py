import asyncio
import re
from pathlib import Path

import aiohttp
import anyio
from bs4 import BeautifulSoup
from nonebot import logger
from playwright.async_api import async_playwright

from .config import config
from .exception import DownloadError

GENRE_LIST = config.genre_list
PROXY = config.proxy


class HanimeDownloader:
    def __init__(self):
        self.playwright = None
        self.browser = None

    async def _init_browser(self):
        """初始化浏览器"""
        if not self.playwright:
            self.playwright = await async_playwright().start()
        if not self.browser:
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                ],
            )

    async def _close_browser(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    async def search(self, query: str = "", genre_num: int = 0):
        """搜索"""
        await self._init_browser()
        res_list = []
        try:
            genre = GENRE_LIST[genre_num - 1] if genre_num != 0 else ""
            search_url = f"https://hanime1.me/search?query={query}&type=&genre={genre}&sort=&year=&month="
            page = await self.browser.new_page(proxy=PROXY)
            await page.goto(search_url)
            page_source = await page.content()
            res_list = await process_search_html(page_source)
            logger.info(f"搜索完成，共匹配了{len(res_list)}个结果")
        finally:
            await page.close()

        return res_list

    async def download(self, video_id, quality: int = 2):
        """下载视频 (quality: 1-1080p 2-720p 3-480p)"""
        match quality:
            case 1:
                type = "1080p"
            case 2:
                type = "720p"
            case 3:
                type = "480p"
            case _:
                type = "720p"
        logger.info(f"开始下载视频: {video_id}")
        url = f"https://hanime1.me/download?v={video_id}"
        await self._init_browser()

        try:
            page = await self.browser.new_page(proxy=PROXY)
            await page.goto(url)
            page_source = await page.content()
            res_list = extract_download_links(page_source)
            for res in res_list:
                if type in res:
                    logger.info(f"获取{type}视频成功，正在下载...")
                    await download_video(res, video_id)
        except DownloadError as e:
            logger.error(e)
        finally:
            await page.close()


async def process_search_html(html_content):
    """解析 HTML，下载封面并获取title和video_id"""
    Path(config.base_path).mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(html_content, "html.parser")

    a_tags = [
        a
        for a in soup.find_all("a", style="text-decoration: none;")
        if a.get("target") != "_blank"
    ]
    logger.info(f"匹配成功，数量:{len(a_tags)}")

    async with aiohttp.ClientSession(proxy=PROXY) as session:
        tasks = []
        results = []
        MAX_RESULTS = 20
        for i, a_tag in enumerate(a_tags, start=1):
            if i > MAX_RESULTS:
                break
            href = a_tag.get("href")

            # 使用正则表达式提取 ID
            match = re.search(r"watch\?v=(\d+)", href)
            video_id = match.group(1)

            # 提取标题
            title_div = a_tag.find("div", class_="home-rows-videos-title")
            title = title_div.text.strip()
            results.append({"title": title, "id": video_id})

            img_tag = a_tag.find("img")
            if img_tag and href:
                img_url = img_tag["src"]
                logger.info(f"正在下载图片: {img_url}")
                tasks.append(download_image(session, img_url, video_id=video_id))
        await asyncio.gather(*tasks)
    return results


def extract_download_links(html_content):
    """提取下载链接"""
    soup = BeautifulSoup(html_content, "html.parser")

    download_links = []
    for a_tag in soup.find_all("a", class_="exoclick-popunder"):
        href = a_tag.get("href")  # 获取 href 属性
        if href:
            download_links.append(href)

    return download_links


async def download_video(url, video_id):
    """下载视频"""
    Path(config.base_path + f"{video_id}/").mkdir(parents=True, exist_ok=True)
    async with aiohttp.ClientSession(proxy=PROXY) as session:  # 创建会话
        try:
            async with session.get(url) as response:  # 使用会话进行请求
                logger.info(f"下载视频{video_id},状态码: {response.status}")
                filename = config.base_path + f"{video_id}/{video_id}.mp4"
                async with await anyio.open_file(filename) as f:
                    await f.write(await response.read())
                logger.info(f"{video_id}视频下载成功")
            await asyncio.sleep(0.5)  # 防止过多请求
        except Exception as e:
            raise DownloadError(f"{video_id}视频下载失败: {e}") from e


async def download_image(session, url, video_id):
    """下载图片"""
    if Path(config.base_path + f"{video_id}/{video_id}.jpg").exists():
        return
    Path(config.base_path + f"{video_id}/").mkdir(parents=True, exist_ok=True)
    try:
        async with session.get(url) as response:
            filename = config.base_path + f"{video_id}/{video_id}.jpg"
            async with await anyio.open_file(filename, "wb") as f:
                await f.write(await response.read())
        await asyncio.sleep(0.5)
    except Exception as e:
        raise DownloadError(f"{video_id}封面下载失败: {e}") from e
