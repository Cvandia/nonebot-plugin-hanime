<div align="center">

# nonebot-plugin-hanime

<a href="https://v2.nonebot.dev/store">
<img src="https://count.littlebell.top/get/@nonebot-plugin-hanime?theme=booru-lewd"></a>

_⭐基于Nonebot2的hanime1.me搜索下载插件⭐_

<a href="https://www.python.org/downloads/release/python-3100/">
    <img src="https://img.shields.io/badge/python-3.10+-blue"></a>
<a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue"></a>
<a href="https://v2.nonebot.dev/">
    <img src="https://img.shields.io/badge/Nonebot2-2.2.0+-red"></a>
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fpdm-project%2F.github%2Fbadge.json" alt="pdm-managed"></a>
<a href="https://github.com/Cvandia/nonebot-plugin-hanime/actions/workflows/python-app.yml">
    <img src="https://github.com/Cvandia/nonebot-plugin-hanime/actions/workflows/python-app.yml/badge.svg?branch=main"></a>

</div>

## 📘 介绍

基于 [hanime1.me](https://hanime1.me) 网站实现视频搜索下载功能的插件

## 📜 免责声明

> [!CAUTION]
> 本插件仅供**学习**和**研究**使用，使用者需自行承担使用插件的风险。作者不对插件的使用造成的任何损失或问题负责。请合理使用插件，**遵守相关法律法规。**
使用**本插件即表示您已阅读并同意遵守以上免责声明**。如果您不同意或无法遵守以上声明，请不要使用本插件。

---

## 💿 安装

<details>
<summary>安装方式</summary>

使用 nb-cli 安装

```bash
nb plugin install nonebot-plugin-hanime
```

使用 pip 安装

```bash
pip install nonebot-plugin-hanime
```

使用 包管理器 安装
```bash
poetry add nonebot-plugin-hanime
or
pdm add nonebot-plugin-hanime
```

</details>

## ⚙️ 配置

在 `.env` 文件中添加以下配置:

|  配置项   | 类型  | 必填  |      默认值      |   说明   |
| :-------: | :---: | :---: | :--------------: | :------: |
|   proxy   |  str  |  否   |       None       | 代理地址 |
| base_path |  str  |  否   | "./data/hanime/" | 下载路径 |

## 🎮 使用

> [!note]
> 请注意以下指令需要有command_start的前缀触发

### 指令列表

|         指令          |    权限    |       说明       |
| :-------------------: | :--------: | :--------------: |
|      hanime_help      |    全部    |   显示帮助信息   |
|      hanime_add       |    超管    |  添加群到白名单  |
|     hanime_remove     |    超管    | 从白名单移除群聊 |
|     hanime_unlock     |    超管    |   解除插件锁定   |
| /hanime 关键词 类型号 | 白名单群聊 |     搜索视频     |
|     hanime_id ID      | 白名单群聊 |  下载指定ID视频  |

### 类型ID说明

- 1: 里番
- 2: 泡面番
- 3: Motion Anime
- 4: 3D动画
- 5: 同人作品
- 6: MMD
- 7: Cosplay

## 🔮 未来

- [ ] 暂无规划

## 📝 开源许可

本项目使用 [MIT](./LICENSE) 许可证开源

## ❤️ 鸣谢

- [nonebot2](https://github.com/nonebot/nonebot2) - 一个 Python 3.10+ 的机器人框架
- [hanime1.me](https://hanime1.me) - 一个提供hanime视频的网站

## 👥 贡献者
<a href="https://github.com/Cvandia/nonebot-plugin-hanime/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=N791/UpFileLive"/>
<a href="https://github.com/Cvandia/nonebot-plugin-hanime/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Cvandia/nonebot-plugin-hanime"/>
</a>
