from pathlib import Path

from PIL import Image, ImageChops


ASSETS = Path(__file__).parent / "assets"


def render_card(source, size):
    with Image.open(ASSETS / "edge.png") as image:
        edge = image.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    with Image.open(ASSETS / "coverage.png") as image:
        coverage = image.convert("L").resize(size, Image.Resampling.LANCZOS)
    source = source.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    gain = Image.merge("RGB", (coverage, coverage, coverage))
    color = ImageChops.add(ImageChops.multiply(source.convert("RGB"), gain), edge.convert("RGB"))
    if source.getchannel("A").getextrema() != (255, 255):
        with Image.open(ASSETS / "base.png") as image:
            base = image.convert("RGB").resize(size, Image.Resampling.LANCZOS)
        color = Image.composite(color, base, source.getchannel("A"))
    color.putalpha(edge.getchannel("A"))
    return color
