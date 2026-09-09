# apl-comfyui

爱谱雷 ComfyUI 自定义节点统一仓库。

用于集中维护各项目组的图像处理节点，统一管理源码、依赖、示例工作流和版本，便于本地 ComfyUI 使用，以及向 RunningHub 提供安装和更新所需的代码与说明。

## 当前状态

已接入卡牌切图节点，可将整个仓库作为 ComfyUI 自定义节点包安装。

## 安装与更新

在 ComfyUI 的 `custom_nodes` 目录中执行：

```sh
git clone https://github.com/799649994-maker/apl-comfyui.git
```

重启 ComfyUI 后生效。更新时在 `custom_nodes/apl-comfyui` 中执行 `git pull --ff-only`，然后重启。

卡牌切图仅使用 ComfyUI 已有的 Pillow、NumPy 和 PyTorch，无需额外依赖或模型。

如果已安装旧版 `cardpack_cutout` 或 `yxmys-cardpack-cutout`，请先将旧节点文件夹移到 `custom_nodes` 之外备份，再启用本仓库，避免同名节点重复注册。节点标识不变，已有工作流可继续使用。

## 节点目录

| 类别 | 文件夹 | 节点 |
| --- | --- | --- |
| 卡牌切图 | [nodes/cardpack_cutout](nodes/cardpack_cutout/README.md) | 卡牌模板切图（免PS）、保存卡牌 PNG32（透明） |

卡牌切图示例：[卡牌切图_免PS.json](nodes/cardpack_cutout/examples/卡牌切图_免PS.json)。拖入 ComfyUI 后，在“加载图像”节点选择自己的图片；IMAGE 与 MASK 两条线均须连接到专用保存节点，才能保留透明通道。

源码来源：[yxmys-cardpack-cutout](https://github.com/799649994-maker/yxmys-cardpack-cutout)，迁入版本 `39c6f96ed787b958478b91d37c71d2d616063fa2`。本次保留原节点实现、模板素材与工作流，增加统一仓库的加载入口。

## 后续接入约定

- 按节点类别划分独立文件夹，统一放在 `nodes/<类别>/` 下；具体类别随节点接入建立。
- 同类节点的代码放在对应类别文件夹中，说明、专属依赖与示例也就近维护，避免不同类别的文件混放。
- 每个节点附带功能说明、输入输出说明、依赖和示例工作流。
- 保持已发布节点的标识与接口兼容；不兼容变更应明确记录。
- 可交付版本使用 Git tag 标记，并记录变更、依赖及验证结果。
- 不提交密钥、账号配置、模型权重、客户素材或生成结果。

## RunningHub 交付

接入节点并完成验证后，向 RunningHub 对接人员提供仓库地址、版本 tag 或 commit、安装说明、依赖和示例工作流。

本仓库公开提供代码。GitHub 提交更新与 RunningHub 部署是两个独立步骤；具体安装方式与更新时间需与对接人员确认。仓库更新不代表 RunningHub 已同步部署。
