# Description: 一些 工具函数, 用于处理图片, 上传文件，添加群聊等操作
#
# Copyright (c) 2025 N791

import json
import secrets
from io import BytesIO
from pathlib import Path

from nonebot import logger
from PIL import Image
from UpFileLive import UpFileLive

from .config import config


async def upFile(file_path):
    upfile = UpFileLive(file_path)
    await upfile.async_upfile()
    return upfile.get_share_link()


def in_list(group_id: int) -> bool:
    if not Path(config.list_path).exists():
        list_data = []
        with Path.open(config.list_path, "w") as f:
            json.dump(list_data, f)
    else:
        try:
            with Path.open(config.list_path, "r") as f:
                list_data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"Error reading file {config.list_path}: {e}")
            list_data = []

    return group_id in list_data


def add_list(group_id: int):
    if not Path(config.list_path).exists():
        list_data = []
        with Path.open(config.list_path, "w") as f:
            json.dump(list_data, f)
    else:
        try:
            with Path.open(config.list_path, "r") as f:
                list_data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"Error reading file {config.list_path}: {e}")
            list_data = []

    if group_id not in list_data:
        list_data.append(group_id)
        try:
            with Path.open(config.list_path, "w") as f:
                json.dump(list_data, f)
        except OSError as e:
            logger.warning(f"Error writing to file {config.list_path}: {e}")


def remove_list(group_id: int):
    if not Path(config.list_path).exists():
        list_data = []
        with Path.open(config.list_path, "w") as f:
            json.dump(list_data, f)
    else:
        try:
            with Path.open(config.list_path, "r") as f:
                list_data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"Error reading file {config.list_path}: {e}")
            list_data = []

    if group_id in list_data:
        list_data.remove(group_id)
        try:
            with Path.open(config.list_path, "w") as f:
                json.dump(list_data, f)
        except OSError as e:
            logger.warning(f"Error writing to file {config.list_path}: {e}")


def change_pixel(image: Image.Image) -> Image.Image:
    """
    修改图片大小并随机修改左上角一个像素点
    """
    image_pixel = image.convert("RGB")
    image_pixel.load()[0, 0] = (
        secrets.randbelow(256),
        secrets.randbelow(256),
        secrets.randbelow(256),
    )

    return image_pixel


def open_image(file_path: str) -> bytes:
    """打开图片并修改尺寸"""
    try:
        with Path.open(file_path, "rb") as f:
            image = Image.open(BytesIO(f.read()))  # 打开图片

        res_img = change_pixel(image)  # 修改图片以防风控
    except Exception as e:
        logger.info(f"图片打开失败，请检查日志: {e!r}")
        return None

    res_data = BytesIO()
    res_img.save(res_data, format="JPEG", quality=95)
    return res_data.getvalue()
