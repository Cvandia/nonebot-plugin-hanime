# Description: nonebot2的 插件主文件，用于处理nonebot2的响应逻辑
#
# Copyright (c) 2025 N791

from dataclasses import dataclass
from re import I

from nonebot import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageSegment,
)
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg, RegexGroup
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata, on_command, on_regex

from .config import Config, config
from .hanime import hanime1
from .utils import add_list, in_list, remove_list

__plugin_meta__ = PluginMetadata(
    name="里番搜索",
    description="还没想好",  # TODO
    usage="还没想好",  # TODO
    config=Config,
    homepage="https://github.com/Cvandia/nonebot-plugin-hanime",
    supported_adapters={"~onebot.v11"},
    type="application",
)


@dataclass
class State:
    running: bool = False


state = State()


async def is_rule() -> bool:
    return not state.running  # 单例模式


hanime_help = on_command("hanime_help", priority=5, block=True)
hanime_add = on_command("hanime_add", priority=5, block=True, permission=SUPERUSER)
hanime_remove = on_command(
    "hanime_remove", priority=5, block=True, permission=SUPERUSER
)
hanime_unlock = on_command(
    "hanime_unlock", priority=5, block=True, permission=SUPERUSER
)
hanime_search = on_regex(
    pattern=config.search_regex, priority=20, block=True, rule=is_rule, flags=I
)
hanime_id = on_command("hanime_id", priority=5, block=True, rule=is_rule)


@hanime_help.handle()
async def hanime_help_handle(event: GroupMessageEvent):
    if in_list(event.group_id):
        await hanime_help.finish(config.hanime_help_str)
    await hanime_help.finish("请先添加本群到白名单")


@hanime_add.handle()
async def hanime_add_handle(event: GroupMessageEvent):
    if in_list(event.group_id):
        await hanime_add.finish("本群已添加")
    add_list(event.group_id)
    await hanime_add.finish("白名单添加成功")


@hanime_remove.handle()
async def hanime_remove_handle(event: GroupMessageEvent):
    if not in_list(event.group_id):
        await hanime_remove.finish("本群未添加")
    remove_list(event.group_id)
    await hanime_remove.finish("白名单删除成功")


@hanime_unlock.handle()
async def hanime_unlock_handle():
    state.running = False
    await hanime_unlock.finish("解锁完成")


@hanime_search.handle()
async def hanime_search_handle(
    bot: Bot, event: GroupMessageEvent, args: tuple = RegexGroup()
):
    if not in_list(event.group_id):
        await hanime_search.finish("本群未添加白名单")

    state.running = True
    await hanime_search.send("正在搜索中，请稍等...")
    query: str = args[1] if args[1] is not None else ""
    genre_num: int = (
        int(args[2]) if args[2] is not None and str(args[2]).isdigit() else 1
    )
    msgs = await hanime1.search_video(query, genre_num)
    state.running = False

    if msgs:
        res = [
            MessageSegment.node_custom(
                user_id=bot.self_id, nickname="hanime_search", content=msg
            )
            for msg in msgs
        ]
        try:
            await bot.call_api(
                "send_group_forward_msg", group_id=event.group_id, messages=res
            )
        except Exception as e:
            logger.error(f"发送失败: {e}")
            await hanime_search.finish(f"发送失败: {e}")

    else:
        await hanime_search.finish("没有找到结果")


@hanime_id.handle()
async def hanime_id_mid_handle(hanime_id_matcher: Matcher, id: Message = CommandArg()):  # noqa: B008
    if id.extract_plain_text():
        hanime_id_matcher.set_arg("id", id)


@hanime_id.got("id", prompt="请输入番剧ID")
async def hanime_id_handle(event: GroupMessageEvent, id: str = ArgPlainText()):
    video_id = int(id)
    if not in_list(event.group_id):
        await hanime_search.finish("本群未添加白名单")

    state.running = True
    await hanime_id.send(f"正在下载{video_id}中，请稍等...")
    share_link = await hanime1.download_id(video_id)
    state.running = False

    if share_link is None:
        await hanime_id.finish("下载失败, 请检查日志")
    else:
        await hanime_id.finish(f"下载完成，分享链接为：{share_link}")
