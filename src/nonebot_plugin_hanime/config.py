from nonebot.plugin import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    help_str: str = (
        "hanime帮助:\n"
        "1.hanime_help 显示帮助\n"
        "2.hanime_add 添加群组白名单(管理员)\n"
        "3.hanime_remove 移除群组白名单(管理员)\n"
        "4.hanime_unlock 解除锁(管理员)\n"
        "5./hanime + 关键词 + (类型号，默认为1) 根据关键词和类型搜索\n"
        "6.hanime_id + id 根据id下载\n"
        "类型号列表如下：0-全部,1-裏番,2-泡麵番,3-Motion Anime,4-3D動畫,5-同人作品,6-MMD,7-Cosplay,(8-無碼黃油,9-新番預告,10-H漫畫, 这三者暂不支持)"
    )
    base_path: str = "./data/hanime/"
    list_path: str = base_path + "list.json"
    search_regex: str = r"^(/hanime)\s?(.*)?\s?(\d+)?"
    genre_list: list = [
        "裏番",
        "泡麵番",
        "Motion Anime",
        "3D動畫",
        "同人作品",
        "MMD",
        "Cosplay",
        "無碼黃油",
        "新番預告",
        "H漫畫",
    ]

config = get_plugin_config(Config)
