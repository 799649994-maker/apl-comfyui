# 卡牌模板切图（免PS）

推荐按[仓库安装说明](../../README.md)安装整个 `apl-comfyui` 仓库，然后重启 ComfyUI。也可只复制本目录 `cardpack_cutout` 到 ComfyUI 的 `custom_nodes`，但不要与整包或旧版重复安装。仅使用 ComfyUI 已有的 Pillow、NumPy 和 PyTorch，不需要 Photoshop 或额外安装依赖。

搜索“卡牌模板切图（免PS）”和“保存卡牌 PNG32（透明）”，或拖入 `examples/卡牌切图_免PS.json`。

连接：加载图像 → 卡牌模板切图 → 保存卡牌 PNG32；图片与 MASK 两条线均按示例连接。成品默认位于 ComfyUI/output/cardpack。

| 上游输出 | 下游输入 |
| --- | --- |
| 加载图像：IMAGE | 卡牌模板切图：images |
| 加载图像：MASK | 卡牌模板切图：mask |
| 卡牌模板切图：images | 保存卡牌 PNG32：images |
| 卡牌模板切图：mask | 保存卡牌 PNG32：mask |

双击画布搜索 `CardpackCutout` 和 `CardpackSavePNG` 即可添加两个节点。使用示例工作流时，在加载图像节点中上传自己的图片，然后运行。

如果输出出现白底，检查最后是否使用了“保存卡牌 PNG32（透明）”，并且接上了 `images` 和 `mask` 两条线。切图节点的 IMAGE 输出只有 RGB，单独接普通“保存图像”不会保留透明度。

- 支持 IMAGE 批次，每张均输出对应 MASK。
- MASK 遵循 ComfyUI 约定：1=透明、0=不透明。可选输入 MASK 可接加载图像的 MASK；不接时按图片自身通道处理。
- 默认直接缩放至 284×393，套用原模板轮廓和描边；不同宽高比会拉伸。
- 透明输入区域沿用原模板底图的填充行为。输出蒙版由固定模板轮廓决定。
- 自定义宽高会同时缩放模板；与原 PS 输出对照验证的尺寸为 284×393。
- 使用专用保存节点将图片与蒙版合成为 RGBA PNG32，并沿用 ComfyUI 原生文件命名与工作流元数据。
- 原模板素材已内置；没有网络请求或 Photoshop 调用。

