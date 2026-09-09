import numpy as np
import torch
from PIL import Image, ImageChops

from nodes import SaveImage
from .render import render_card


class CardpackCutout:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "width": ("INT", {"default": 284, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 393, "min": 1, "max": 8192}),
            },
            "optional": {"mask": ("MASK",)},
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("images", "mask")
    FUNCTION = "cut"
    CATEGORY = "image/卡牌切图"
    DESCRIPTION = "直接缩放并套用内置卡牌轮廓和描边。支持图片批次；蒙版遵循 ComfyUI 的 1=透明约定。无需 Photoshop。"

    def cut(self, images, width, height, mask=None):
        if mask is not None:
            if mask.ndim == 2:
                mask = mask.unsqueeze(0)
            if len(mask) not in (1, len(images)):
                raise ValueError("蒙版数量必须为 1 或与图片数量一致。")
        size = (width, height)
        results = []
        masks = []
        for index, tensor in enumerate(images):
            pixels = np.clip(np.rint(tensor.detach().cpu().numpy() * 255), 0, 255).astype(np.uint8)
            source = Image.fromarray(pixels).convert("RGBA")
            if mask is not None:
                current_mask = mask[0 if len(mask) == 1 else index].detach().cpu().numpy()
                opacity = Image.fromarray(np.clip(np.rint((1 - current_mask) * 255), 0, 255).astype(np.uint8))
                opacity = opacity.resize(source.size, Image.Resampling.LANCZOS)
                source.putalpha(ImageChops.multiply(source.getchannel("A"), opacity))
            color = render_card(source, size)
            results.append(torch.from_numpy(np.asarray(color.convert("RGB"), dtype=np.float32) / 255.0))
            masks.append(torch.from_numpy(1 - np.asarray(color.getchannel("A"), dtype=np.float32) / 255.0))
        return torch.stack(results), torch.stack(masks)


class CardpackSavePNG(SaveImage):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"]["mask"] = ("MASK",)
        inputs["required"]["filename_prefix"][1]["default"] = "cardpack/card"
        return inputs

    CATEGORY = "image/卡牌切图"
    DESCRIPTION = "将图片和透明蒙版保存为 PNG32，保留工作流信息。蒙版中 1 表示透明。"

    def save_images(self, images, mask, filename_prefix="cardpack/card", prompt=None, extra_pnginfo=None):
        if mask.ndim == 2:
            mask = mask.unsqueeze(0)
        if mask.shape[1:] != images.shape[1:3] or len(mask) not in (1, len(images)):
            raise ValueError("保存蒙版的尺寸须与图片一致，数量须为 1 或与图片数量一致。")
        alpha = (1 - mask).clamp(0, 1).to(device=images.device, dtype=images.dtype)
        if len(alpha) == 1 and len(images) != 1:
            alpha = alpha.expand(len(images), -1, -1)
        rgba = torch.cat((images[..., :3], alpha.unsqueeze(-1)), dim=-1)
        # Quantize before the standard saver truncates float values to bytes.
        rgba = torch.round(rgba * 255) / 255
        return super().save_images(rgba, filename_prefix, prompt, extra_pnginfo)


NODE_CLASS_MAPPINGS = {
    "CardpackCutout": CardpackCutout,
    "CardpackSavePNG": CardpackSavePNG,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CardpackCutout": "卡牌模板切图（免PS）",
    "CardpackSavePNG": "保存卡牌 PNG32（透明）",
}
