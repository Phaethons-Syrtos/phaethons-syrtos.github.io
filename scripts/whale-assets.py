"""生成鲸鱼主题的站点素材（头像、favicon、导航 logo、壁纸）。

用法：
    python scripts/whale-assets.py "C:/Users/FHPR/Desktop/deepseek-wanju-maid.png"

源图是一张方形的鲸鱼娘玩偶照片。输出的文件都会写进仓库：
    src/assets/images/avatar-whale.webp
    src/assets/images/logo/whale-logo.png
    src/assets/images/wallpaper-whale-desktop.jpg
    src/assets/images/wallpaper-whale-mobile.jpg
    public/favicon/whale-{32,128,180,192}.png
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "C:/Users/FHPR/Desktop/deepseek-wanju-maid.png")

DEEP = (4, 12, 32)          # 深海军蓝
MID = (77, 107, 254)        # DeepSeek 蓝
LIGHT = (176, 200, 255)     # 浅蓝高光


def duotone(img: Image.Image) -> Image.Image:
    gray = img.convert("L")
    gray = ImageOps.autocontrast(gray, cutoff=1)
    return ImageOps.colorize(gray, DEEP, LIGHT)


def cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    w, h = size
    scale = max(w / img.width, h / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (resized.width - w) // 2
    top = (resized.height - h) // 2
    return resized.crop((left, top, left + w, top + h))


def rounded(img: Image.Image, radius_ratio: float = 0.22) -> Image.Image:
    size = img.size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    radius = int(min(size) * radius_ratio)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def circle(img: Image.Image) -> Image.Image:
    size = img.size
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size[0], size[1]), fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def wallpaper(src: Image.Image, size: tuple[int, int], focus: tuple[float, float]) -> Image.Image:
    w, h = size
    tone = duotone(src)

    # 底：深蓝渐变 + 一团 DeepSeek 蓝光晕
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (yy / h)[..., None]
    arr = np.array(DEEP, dtype=np.float32) / 255.0 * (1 - t) + np.array((16, 34, 74), dtype=np.float32) / 255.0 * t
    cx, cy = w * 0.5, h * 0.38
    dist = np.sqrt(((xx - cx) / (w * 0.62)) ** 2 + ((yy - cy) / (h * 0.7)) ** 2)
    glow = np.exp(-(dist ** 2) * 2.2)[..., None] * (np.array(MID, dtype=np.float32) / 255.0)
    arr = 1 - (1 - arr) * (1 - glow * 0.55)

    # 玩偶：放在右侧，柔边淡入，只当纹理，不抢文字
    pw = int(min(w, h) * 1.05)
    plush = tone.resize((pw, pw), Image.LANCZOS).filter(ImageFilter.GaussianBlur(h / 220))
    px = int(w * focus[0] - pw / 2)
    py = int(h * focus[1] - pw / 2)

    alpha = np.zeros((h, w), dtype=np.float32)
    # 圆形柔边蒙版
    pyy, pxx = np.mgrid[0:pw, 0:pw].astype(np.float32)
    pd = np.sqrt(((pxx - pw / 2) / (pw / 2)) ** 2 + ((pyy - pw / 2) / (pw / 2)) ** 2)
    soft = np.exp(-((pd * 1.55) ** 3)) * 0.55
    x0, y0 = max(0, px), max(0, py)
    x1, y1 = min(w, px + pw), min(h, py + pw)
    alpha[y0:y1, x0:x1] = soft[y0 - py : y1 - py, x0 - px : x1 - px]
    canvas = Image.new("RGB", size)
    canvas.paste(plush, (px, py))
    plush_np = np.asarray(canvas, dtype=np.float32) / 255.0

    a = alpha[..., None]
    arr = arr * (1 - a) + plush_np * a

    # 顶部压暗 + 暗角
    vertical = np.clip(1.0 - 0.3 * (yy / h) ** 2, 0.65, 1.0)[..., None]
    vignette = np.clip(1.0 - 0.45 * np.clip(dist - 0.4, 0, None) ** 1.5, 0.4, 1.0)[..., None]
    arr = arr * vertical * vignette

    rng = np.random.default_rng(7)
    arr = arr + rng.normal(0, 0.005, arr.shape).astype(np.float32)
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8))


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"找不到源图：{SRC}")

    src = Image.open(SRC).convert("RGB")
    print(f"源图 {SRC.name} {src.size}")

    # 头像：裁到脸部附近，正方形 512
    side = int(src.width * 0.56)
    cx, cy = int(src.width * 0.47), int(src.height * 0.5)
    box = (
        max(0, cx - side // 2),
        max(0, cy - side // 2),
        min(src.width, cx + side // 2),
        min(src.height, cy + side // 2),
    )
    face = src.crop(box).resize((512, 512), Image.LANCZOS)
    face = ImageEnhance.Color(face).enhance(1.05)
    face = ImageEnhance.Contrast(face).enhance(1.03)

    avatar_path = ROOT / "src/assets/images/avatar-whale.webp"
    face.save(avatar_path, "WEBP", quality=90, method=6)
    print("写入", avatar_path.relative_to(ROOT), avatar_path.stat().st_size)

    # 导航栏 logo：圆形 160
    logo = circle(face.resize((160, 160), Image.LANCZOS))
    logo_path = ROOT / "src/assets/images/logo/whale-logo.png"
    logo.save(logo_path, "PNG", optimize=True)
    print("写入", logo_path.relative_to(ROOT), logo_path.stat().st_size)

    # favicon：圆角
    for size in (32, 128, 180, 192):
        icon = rounded(face.resize((size, size), Image.LANCZOS), 0.2)
        out = ROOT / f"public/favicon/whale-{size}.png"
        icon.save(out, "PNG", optimize=True)
        print("写入", out.relative_to(ROOT), out.stat().st_size)

    # 壁纸
    for name, size, focus in (
        ("wallpaper-whale-desktop.jpg", (1920, 1080), (0.72, 0.52)),
        ("wallpaper-whale-mobile.jpg", (1080, 1920), (0.5, 0.6)),
    ):
        img = wallpaper(src, size, focus)
        out = ROOT / "src/assets/images" / name
        img.save(out, "JPEG", quality=88, optimize=True, progressive=True)
        print("写入", out.relative_to(ROOT), out.stat().st_size)


if __name__ == "__main__":
    main()
