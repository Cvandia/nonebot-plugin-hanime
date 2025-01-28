from pathlib import Path

from nonebot import get_plugin_config, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .config import Config
from .download import download, search
from .utils import open_image, upFile

config = get_plugin_config(Config)


class Hanime1:
    def __init__(self):
        self.base_path = config.base_path
        self.genre_list = config.genre_list

    async def download_id(self, id: int, level: int = 2):
        if not Path(self.base_path + f"{id}/{id}.mp4").exists():
            logger.info(f"开始下载: {id}")
            await download(video_id=id, quality=level)
        share_link = None
        if Path(self.base_path + f"{id}/{id}.mp4").exists():
            share_link = await upFile(file_path=self.base_path + f"{id}/{id}.mp4")
        return share_link

    async def search_video(self, query: str = "", genre_num: int = 0):
        msgs = []
        MAX_GENRE_NUM = 7
        if genre_num > MAX_GENRE_NUM:
            genre_num = 1  # 防止超过预定的数

        res_list = await search(query=query, genre_num=genre_num)
        if len(res_list) == 0:
            return msgs

        for res in res_list:
            title = res["title"]  # 标题
            video_id = res["id"]  # 视频id
            pic = open_image(
                file_path=self.base_path + f"{video_id}/{video_id}.jpg"
            )  # 视频封面

            msg_str = Message(f"标题: {title}\n视频ID: {video_id}")
            msg_pic = MessageSegment.image(pic)
            msg = msg_pic + msg_str

            msgs.append(msg)

        return msgs


hanime1 = Hanime1()
