#!/usr/bin/env python3
"""渲染投诉管理 Skill 图标：蓝底白色描边盾牌 + 两条横线/对勾 + "投诉管理"文字。
参考用户提供的"消保评价"图标风格，超采样 4x 抗锯齿。输出 512x512 PNG。
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "_icon.png"  # 输出到 skill 根目录

S = 4  # 超采样倍数
W = 512 * S
BG = (43, 78, 161, 255)      # #2B4EA1
FG = (255, 255, 255, 255)

img = Image.new("RGBA", (W, W), BG)
d = ImageDraw.Draw(img)

stroke = 26 * S
r = stroke // 2


def cubic(p0, p1, p2, p3, n=30):
    """三次贝塞尔曲线采样为折线点列。"""
    pts = []
    for i in range(1, n + 1):
        t = i / n
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        pts.append((x, y))
    return pts


# ---- 盾牌（描边风格）：顶部中峰 → 双肩 → 直边 → 贝塞尔曲线收至底尖 ----
top_peak = (256, 78)
l_shoulder = (112, 140)
l_side_end = (112, 255)
l_bezier = cubic(l_side_end, (118, 330), (182, 398), (256, 428))
r_bezier = cubic((256, 428), (330, 398), (394, 330), (400, 255))
r_shoulder = (400, 140)

path = ([top_peak, l_shoulder, l_side_end] + l_bezier + r_bezier + [r_shoulder, top_peak])
pts = [(x * S, y * S) for x, y in path]
d.line(pts, fill=FG, width=stroke, joint="curve")
for p in (top_peak, l_shoulder, l_side_end, r_shoulder, (256, 425)):
    q = (p[0] * S, p[1] * S)
    d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=FG)

# ---- 两条横线 + 对勾 ----
for y0 in (166, 226):
    d.rounded_rectangle([190 * S, y0 * S, 262 * S, (y0 + 22) * S], radius=11 * S, fill=FG)
    check = [(290, y0 + 2), (310, y0 + 24), (346, y0 - 16)]
    cpts = [(x * S, y * S) for x, y in check]
    d.line(cpts, fill=FG, width=22 * S, joint="curve")
    for p in (cpts[0], cpts[-1]):
        rr = 11 * S
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=FG)

# ---- 文字：投诉管理（Hiragino Sans GB W6 粗体），居中于盾内 ----
font = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 50 * S, index=1)
bbox = d.textbbox((0, 0), "投诉管理", font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
d.text((W // 2 - tw / 2 - bbox[0], 306 * S - th / 2 - bbox[1]), "投诉管理", font=font, fill=FG)

img = img.resize((512, 512), Image.LANCZOS)
img.save(OUT)
print("saved _icon.png 512x512")
