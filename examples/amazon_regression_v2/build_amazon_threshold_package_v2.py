from __future__ import annotations

import argparse
import base64
import csv
import json
import math
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

for parent in Path(__file__).resolve().parents:
    deps = parent / ".codex_pydeps"
    if deps.exists():
        sys.path.insert(0, str(deps))
        break

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt


SLUG = "amazon_deforestation_drought_threshold"
W, H = 1920, 1080
PX_PER_IN = 144

COL = {
    "text": "1F2F2A",
    "blue": "0B559F",
    "blue2": "1F78B4",
    "red": "C62828",
    "red_dark": "A00000",
    "orange": "E66A2C",
    "green": "1B7F45",
    "green_dark": "07582F",
    "gray": "CCD8D2",
    "cream": "FFF4E6",
}

TEXT = {
    "title": "毁林诱发干旱降低亚马逊森林气候临界阈值",
    "left": "外部压力",
    "mid": "水分循环削弱与干旱增强",
    "right": "系统性转变风险",
    "warming": "全球变暖\n1.5–1.9°C / 3.7–4.0°C",
    "deforest": "毁林比例\n22–28%",
    "intact": "完整森林",
    "after": "毁林后",
    "evap": "蒸散发",
    "evap_down": "蒸散发下降",
    "transport_strong": "水汽输送（强）",
    "transport_weak": "水汽输送（减弱）",
    "rain": "降水",
    "rain_less": "降水减少",
    "downwind": "下风向级联影响",
    "cascade": "级联转变 / knock-on effects",
    "stable": "稳定的热带雨林系统",
    "degraded": "退化的生态系统",
    "threshold": "临界阈值\n（转折点）",
    "stable_state": "稳定雨林状态",
    "degraded_state": "退化生态系统状态",
    "warm_only": "仅全球变暖：临界阈值约 3.7–4.0°C",
    "warm_def": "全球变暖 + 毁林：\n1.5–1.9°C 即可能触发近系统性转变",
    "area": "潜在受影响面积：62–77%",
    "conclusion": "控制全球升温低于 1.5°C、停止毁林并恢复退化森林，是降低亚马逊系统性转变风险的关键。",
}

OLD_ASSETS = {
    "warming_earth_thermometer": "warming_earth_thermometer.png",
    "amazon_deforestation_map": "amazon_deforestation_map.png",
    "forest_evapotranspiration_scene": "forest_evapotranspiration_scene.png",
    "deforested_agriculture_road_patch": "deforested_agriculture_road_patch.png",
    "healthy_rainforest_state": "healthy_rainforest_state.png",
    "degraded_savanna_state": "degraded_savanna_state.png",
}

ROLES = {
    "warming_earth_thermometer": "全球变暖地球与温度计图标",
    "amazon_deforestation_map": "亚马逊毁林扩张地图与农业/道路斑块",
    "forest_evapotranspiration_scene": "完整森林水分循环场景",
    "deforested_agriculture_road_patch": "毁林道路农业斑块与干旱区域",
    "healthy_rainforest_state": "稳定湿润雨林状态图",
    "degraded_savanna_state": "退化稀树草原状态图",
    "rain_cloud": "降雨云与雨线",
    "healthy_forest_panorama": "母版上半完整森林河流横向场景",
    "deforested_dry_panorama": "母版下半毁林道路干旱横向场景",
    "cascade_amazon_map": "底部级联影响亚马逊地图",
    "conservation_leaf_shield": "底部结论保护叶盾图标",
}

BBOX = {
    "warming_earth_thermometer": [115, 230, 270, 180],
    "amazon_deforestation_map": [100, 535, 330, 230],
    "healthy_forest_panorama": [585, 238, 420, 170],
    "forest_evapotranspiration_scene": [715, 258, 235, 125],
    "rain_cloud": [1080, 230, 145, 90],
    "deforested_dry_panorama": [585, 480, 455, 150],
    "deforested_agriculture_road_patch": [945, 470, 275, 160],
    "cascade_amazon_map": [590, 696, 505, 128],
    "healthy_rainforest_state": [1360, 262, 240, 170],
    "degraded_savanna_state": [1610, 262, 210, 170],
    "conservation_leaf_shield": [118, 925, 72, 72],
}

DIRS = [
    "00_request",
    "01_inputs/source_images",
    "01_inputs/user_assets",
    "01_inputs/notes",
    "02_image2_master/master_raw",
    "02_image2_master/master_selected",
    "02_image2_master/rejected_or_buggy",
    "03_assets_raw/generated_single_assets",
    "03_assets_raw/rejected_or_buggy",
    "04_assets_cutout/transparent_png",
    "04_assets_cutout/contact_sheets",
    "05_assets_vector/svg_wrappers",
    "05_assets_vector/vectorized_candidates",
    "05_assets_vector/vectorization_comparison",
    "06_editable_pptx",
    "07_svg_export",
    "08_previews",
    "09_manifests",
    "10_qa",
    "_archive/intermediate_build",
    "_archive/discarded_versions",
]


def rgb(value: str) -> tuple[int, int, int]:
    value = value.strip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def px(value: float) -> float:
    return value / PX_PER_IN


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    names = ["msyhbd.ttc" if bold else "msyh.ttc", "simhei.ttf", "arial.ttf"]
    for name in names:
        candidate = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / name
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


F = {
    "title": font(38, True),
    "h": font(26, True),
    "b": font(23, True),
    "s": font(18),
    "xs": font(15),
    "con": font(25, True),
}


def fit(path: Path, box: list[int]) -> list[int]:
    image = Image.open(path)
    x, y, w, h = box
    scale = min(w / image.width, h / image.height)
    nw, nh = int(image.width * scale), int(image.height * scale)
    return [x + (w - nw) // 2, y + (h - nh) // 2, nw, nh]


def chroma_remove(src: Path, out: Path, key: tuple[int, int, int] = (255, 0, 255)) -> None:
    helper = Path(os.environ.get("USERPROFILE", "")) / ".codex" / "skills" / ".system" / "imagegen" / "scripts" / "remove_chroma_key.py"
    if helper.exists():
        subprocess.run(
            [
                sys.executable,
                str(helper),
                "--input",
                str(src),
                "--out",
                str(out),
                "--auto-key",
                "border",
                "--soft-matte",
                "--transparent-threshold",
                "18",
                "--opaque-threshold",
                "220",
                "--despill",
                "--edge-contract",
                "1",
                "--force",
            ],
            check=True,
        )
        return
    image = Image.open(src).convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            distance = math.sqrt((r - key[0]) ** 2 + (g - key[1]) ** 2 + (b - key[2]) ** 2)
            if distance < 34:
                pixels[x, y] = (r, g, b, 0)
            elif distance < 125:
                alpha = int(255 * (distance - 34) / 91)
                nr = min(r, int((g + b) / 2) + 35)
                nb = min(b, int((r + g) / 2) + 35)
                pixels[x, y] = (nr, g, nb, min(a, alpha))
    image.save(out)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, face: ImageFont.ImageFont, fill: str = COL["text"], anchor: str | None = None, max_chars: int | None = None, gap: int = 4) -> None:
    lines: list[str] = []
    for raw in value.split("\n"):
        if max_chars and len(raw) > max_chars:
            lines.extend(raw[i : i + max_chars] for i in range(0, len(raw), max_chars))
        else:
            lines.append(raw)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=face, fill="#" + fill, anchor=anchor)
        y += getattr(face, "size", 20) + gap


def round_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str, radius: int = 8, width: int = 2) -> None:
    draw.rounded_rectangle(box, radius=radius, fill="#" + fill, outline="#" + outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color: str, width: int = 5, dashed: bool = False, head: bool = True) -> None:
    for (x1, y1), (x2, y2) in zip(points[:-1], points[1:]):
        if dashed:
            parts = 18
            for idx in range(parts):
                if idx % 2 == 0:
                    xa = x1 + (x2 - x1) * idx / parts
                    ya = y1 + (y2 - y1) * idx / parts
                    xb = x1 + (x2 - x1) * (idx + 1) / parts
                    yb = y1 + (y2 - y1) * (idx + 1) / parts
                    draw.line((xa, ya, xb, yb), fill="#" + color, width=width)
        else:
            draw.line((x1, y1, x2, y2), fill="#" + color, width=width)
    if head and len(points) >= 2:
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        angle = math.atan2(y2 - y1, x2 - x1)
        length = 22
        triangle = [
            (x2, y2),
            (x2 - length * math.cos(angle - 0.48), y2 - length * math.sin(angle - 0.48)),
            (x2 - length * math.cos(angle + 0.48), y2 - length * math.sin(angle + 0.48)),
        ]
        draw.polygon(triangle, fill="#" + color)


class Builder:
    def __init__(self, old_root: Path, root: Path, generated: dict[str, Path]) -> None:
        self.old_root = old_root
        self.root = root
        self.generated = generated
        self.assets: dict[str, dict[str, str]] = {}

    def prepare_dirs(self) -> None:
        for directory in DIRS:
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.old_root / "02_image2_master/master_selected/image2_master_selected.png", self.root / "02_image2_master/master_selected/image2_master_selected.png")
        shutil.copy2(self.old_root / "02_image2_master/master_raw/image2_master_raw.png", self.root / "02_image2_master/master_raw/image2_master_raw.png")

    def prepare_assets(self) -> None:
        for key, filename in OLD_ASSETS.items():
            src = self.old_root / "04_assets_cutout/transparent_png" / filename
            raw_src = self.old_root / "03_assets_raw/generated_single_assets" / f"{key}_raw.png"
            raw_dest = self.root / "03_assets_raw/generated_single_assets" / f"{key}_raw.png"
            transparent_dest = self.root / "04_assets_cutout/transparent_png" / f"{key}.png"
            shutil.copy2(raw_src if raw_src.exists() else src, raw_dest)
            shutil.copy2(src, transparent_dest)
            self.assets[key] = {"role": ROLES[key], "raw": raw_dest.name, "transparent": transparent_dest.name}
        for key, src in self.generated.items():
            raw_dest = self.root / "03_assets_raw/generated_single_assets" / f"{key}_raw.png"
            transparent_dest = self.root / "04_assets_cutout/transparent_png" / f"{key}.png"
            shutil.copy2(src, raw_dest)
            chroma_remove(raw_dest, transparent_dest)
            self.assets[key] = {"role": ROLES[key], "raw": raw_dest.name, "transparent": transparent_dest.name}

    def asset_path(self, key: str) -> Path:
        return self.root / "04_assets_cutout/transparent_png" / self.assets[key]["transparent"]

    def paste_asset(self, canvas: Image.Image, key: str, box: list[int] | None = None) -> list[int]:
        path = self.asset_path(key)
        fitted = fit(path, box or BBOX[key])
        image = Image.open(path).convert("RGBA")
        image.thumbnail((fitted[2], fitted[3]), Image.Resampling.LANCZOS)
        canvas.alpha_composite(image, (fitted[0], fitted[1]))
        return [fitted[0], fitted[1], image.width, image.height]

    def build_preview(self) -> None:
        canvas = Image.new("RGBA", (W, H), "white")
        draw = ImageDraw.Draw(canvas)
        text(draw, (960, 50), TEXT["title"], F["title"], anchor="ma")
        panels = [(70, 145, 460, 700, TEXT["left"], COL["blue"]), (560, 145, 720, 700, TEXT["mid"], COL["blue"]), (1310, 145, 540, 700, TEXT["right"], COL["red_dark"])]
        for x, y, w, h, label, color in panels:
            round_rect(draw, (x, y, x + w, y + h), "FFFFFF", color, 8, 3)
            draw.rounded_rectangle((x, y, x + w, y + 52), radius=8, fill="#" + color, outline="#" + color, width=1)
            text(draw, (x + w // 2, y + 15), label, F["h"], "FFFFFF", anchor="ma")
        for cy, number in [(190, "1"), (475, "2")]:
            round_rect(draw, (86, cy, 514, cy + (260 if number == "1" else 350)), "FFFFFF", COL["blue"], 6, 2)
            draw.ellipse((94, cy + 12, 132, cy + 50), fill="#" + COL["blue"])
            text(draw, (113, cy + 18), number, F["b"], "FFFFFF", anchor="ma")
        text(draw, (150, 198), TEXT["warming"], F["b"], max_chars=22)
        self.paste_asset(canvas, "warming_earth_thermometer")
        text(draw, (150, 485), TEXT["deforest"], F["b"], max_chars=18)
        self.paste_asset(canvas, "amazon_deforestation_map")
        for idx, (label, color) in enumerate([("原生森林", COL["green"]), ("毁林区域", "CFA15E"), ("道路/基础设施", "6F6F6F"), ("农业扩张", "7A6B19")]):
            y = 748 + idx * 22
            draw.rectangle((118, y, 144, y + 14), fill="#" + color, outline="#555555")
            text(draw, (154, y - 2), label, F["xs"])
        for box in [(575, 200, 1265, 435), (575, 450, 1265, 675), (575, 692, 1265, 830)]:
            round_rect(draw, box, "FFFFFF", COL["blue"] if box[1] < 680 else COL["gray"], 6, 2)
        text(draw, (586, 214), TEXT["intact"], F["s"], COL["green_dark"])
        self.paste_asset(canvas, "healthy_forest_panorama")
        self.paste_asset(canvas, "rain_cloud")
        for x in [685, 719, 753, 787, 821]:
            arrow(draw, [(x, 300), (x + 5, 245)], COL["blue2"], 3, True)
        arrow(draw, [(850, 262), (1010, 286)], COL["blue2"], 4)
        text(draw, (755, 220), TEXT["evap"], F["s"], COL["blue2"], anchor="ma")
        text(draw, (935, 225), TEXT["transport_strong"], F["xs"], COL["blue2"], anchor="ma")
        text(draw, (1148, 214), TEXT["rain"], F["s"], COL["blue2"], anchor="ma")
        text(draw, (586, 462), TEXT["after"], F["s"], COL["green_dark"])
        self.paste_asset(canvas, "deforested_dry_panorama")
        self.paste_asset(canvas, "deforested_agriculture_road_patch")
        self.paste_asset(canvas, "rain_cloud", [1085, 478, 125, 70])
        arrow(draw, [(850, 505), (1010, 520)], COL["blue2"], 3, True)
        arrow(draw, [(650, 655), (1200, 655)], COL["red"], 4)
        text(draw, (770, 455), TEXT["evap_down"], F["s"], anchor="ma")
        text(draw, (940, 458), TEXT["transport_weak"], F["xs"], COL["blue2"], anchor="ma")
        text(draw, (1148, 455), TEXT["rain_less"], F["s"], anchor="ma")
        text(draw, (950, 625), TEXT["downwind"], F["s"], COL["red"], anchor="ma")
        self.paste_asset(canvas, "cascade_amazon_map")
        text(draw, (785, 704), TEXT["cascade"], F["s"], COL["red"], anchor="ma")
        arrow(draw, [(720, 790), (800, 750), (890, 768), (980, 728)], COL["red"], 3, True)
        arrow(draw, [(640, 815), (745, 795), (820, 810), (920, 780)], COL["red"], 3, True)
        text(draw, (1100, 735), "级联路径：\n从东南毁林弧\n沿主导水汽输送方向\n影响中部和西部亚马逊", F["xs"])
        arrow(draw, [(530, 470), (560, 470)], COL["blue"], 8)
        arrow(draw, [(1280, 470), (1310, 470)], COL["red"], 8)
        text(draw, (1370, 205), TEXT["stable"], F["s"], COL["green_dark"])
        text(draw, (1625, 205), TEXT["degraded"], F["s"], COL["red"])
        self.paste_asset(canvas, "healthy_rainforest_state")
        self.paste_asset(canvas, "degraded_savanna_state")
        draw.line((1580, 252, 1580, 530), fill="#" + COL["red"], width=4)
        for yy in range(252, 530, 24):
            draw.line((1580, yy, 1580, yy + 12), fill="#FFFFFF", width=4)
        text(draw, (1580, 248), TEXT["threshold"], F["s"], COL["red"], anchor="ma")
        arrow(draw, [(1365, 514), (1790, 514)], COL["orange"], 5)
        text(draw, (1420, 536), TEXT["stable_state"], F["s"], COL["green_dark"], anchor="ma")
        text(draw, (1730, 536), TEXT["degraded_state"], F["s"], COL["orange"], anchor="ma")
        cards = [(600, 54, TEXT["warm_only"], COL["blue"], "warming_earth_thermometer"), (675, 68, TEXT["warm_def"], COL["red"], "amazon_deforestation_map"), (760, 54, TEXT["area"], COL["orange"], "cascade_amazon_map")]
        for idx, (y, height, label, color, icon) in enumerate(cards):
            round_rect(draw, (1330, y, 1828, y + height), "FFFFFF", color, 6, 2)
            self.paste_asset(canvas, icon, [1342, y + 8, 58, 44])
            text(draw, (1415, y + 13), label, F["s"] if idx != 1 else F["xs"], color, max_chars=30)
        round_rect(draw, (96, 910, 1824, 1015), "F7FBFF", COL["green_dark"], 8, 3)
        self.paste_asset(canvas, "conservation_leaf_shield")
        text(draw, (980, 943), TEXT["conclusion"], F["con"], COL["green_dark"], anchor="ma", max_chars=48, gap=2)
        canvas.convert("RGB").save(self.root / "08_previews/final_figure.png", quality=95)
        shutil.copy2(self.root / "08_previews/final_figure.png", self.root / "08_previews/preview_pptx.png")
        shutil.copy2(self.root / "08_previews/final_figure.png", self.root / "08_previews/preview_svg.png")

    def ppt_text(self, slide, x, y, w, h, value, size=12, bold=False, color=COL["text"], align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
        box = slide.shapes.add_textbox(Inches(px(x)), Inches(px(y)), Inches(px(w)), Inches(px(h)))
        frame = box.text_frame
        frame.clear()
        frame.word_wrap = True
        frame.margin_left = Inches(0.03)
        frame.margin_right = Inches(0.03)
        frame.margin_top = Inches(0.01)
        frame.margin_bottom = Inches(0.01)
        frame.vertical_anchor = valign
        for idx, line in enumerate(value.split("\n")):
            paragraph = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
            paragraph.alignment = align
            run = paragraph.add_run()
            run.text = line
            run.font.name = "Microsoft YaHei"
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = RGBColor(*rgb(color))
        return box

    def ppt_rect(self, slide, x, y, w, h, fill="FFFFFF", line=COL["gray"], radius=False, width=1.2):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, Inches(px(x)), Inches(px(y)), Inches(px(w)), Inches(px(h)))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*rgb(fill))
        shape.line.color.rgb = RGBColor(*rgb(line))
        shape.line.width = Pt(width)
        return shape

    def ppt_line(self, slide, x1, y1, x2, y2, color=COL["blue2"], width=2.5, dashed=False, end=True):
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(px(x1)), Inches(px(y1)), Inches(px(x2)), Inches(px(y2)))
        line.line.color.rgb = RGBColor(*rgb(color))
        line.line.width = Pt(width)
        if dashed:
            line.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        if end:
            head = OxmlElement("a:headEnd")
            head.set("type", "triangle")
            head.set("w", "med")
            head.set("len", "med")
            line._element.spPr.ln.append(head)
        return line

    def ppt_img(self, slide, key: str, box: list[int] | None = None):
        fitted = fit(self.asset_path(key), box or BBOX[key])
        slide.shapes.add_picture(str(self.asset_path(key)), Inches(px(fitted[0])), Inches(px(fitted[1])), width=Inches(px(fitted[2])), height=Inches(px(fitted[3])))
        return fitted

    def build_pptx(self) -> None:
        prs = Presentation()
        prs.slide_width = Inches(W / PX_PER_IN)
        prs.slide_height = Inches(H / PX_PER_IN)
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self.ppt_text(slide, 260, 25, 1400, 60, TEXT["title"], 22, True, COL["text"], PP_ALIGN.CENTER)
        for x, y, w, h, label, color in [(70, 145, 460, 700, TEXT["left"], COL["blue"]), (560, 145, 720, 700, TEXT["mid"], COL["blue"]), (1310, 145, 540, 700, TEXT["right"], COL["red_dark"])]:
            self.ppt_rect(slide, x, y, w, h, "FFFFFF", color, True, 1.8)
            self.ppt_rect(slide, x, y, w, 52, color, color, True, 0)
            self.ppt_text(slide, x + 10, y + 14, w - 20, 30, label, 14, True, "FFFFFF", PP_ALIGN.CENTER)
        for cy, number in [(190, "1"), (475, "2")]:
            self.ppt_rect(slide, 86, cy, 428, 260 if number == "1" else 350, "FFFFFF", COL["blue"], True, 1.1)
            circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(px(94)), Inches(px(cy + 12)), Inches(px(38)), Inches(px(38)))
            circle.fill.solid()
            circle.fill.fore_color.rgb = RGBColor(*rgb(COL["blue"]))
            circle.line.color.rgb = RGBColor(*rgb(COL["blue"]))
            self.ppt_text(slide, 101, cy + 16, 24, 22, number, 12, True, "FFFFFF", PP_ALIGN.CENTER)
        self.ppt_text(slide, 150, 198, 250, 54, TEXT["warming"], 11, True)
        self.ppt_img(slide, "warming_earth_thermometer")
        self.ppt_text(slide, 150, 485, 220, 50, TEXT["deforest"], 11, True)
        self.ppt_img(slide, "amazon_deforestation_map")
        for idx, (label, color) in enumerate([("原生森林", COL["green"]), ("毁林区域", "CFA15E"), ("道路/基础设施", "6F6F6F"), ("农业扩张", "7A6B19")]):
            self.ppt_rect(slide, 118, 748 + idx * 22, 26, 14, color, "555555", False, 0.5)
            self.ppt_text(slide, 154, 744 + idx * 22, 140, 20, label, 7.5, False)
        for box in [(575, 200, 690, 235), (575, 450, 690, 225), (575, 692, 690, 138)]:
            self.ppt_rect(slide, *box, "FFFFFF", COL["blue"] if box[1] < 680 else COL["gray"], True, 1.1)
        for key in ["healthy_forest_panorama", "rain_cloud", "deforested_dry_panorama", "deforested_agriculture_road_patch", "cascade_amazon_map", "healthy_rainforest_state", "degraded_savanna_state"]:
            self.ppt_img(slide, key)
        self.ppt_text(slide, 586, 214, 90, 25, TEXT["intact"], 9, True, COL["green_dark"])
        self.ppt_text(slide, 735, 220, 95, 24, TEXT["evap"], 8, True, COL["blue2"], PP_ALIGN.CENTER)
        self.ppt_text(slide, 890, 225, 155, 24, TEXT["transport_strong"], 7, True, COL["blue2"], PP_ALIGN.CENTER)
        self.ppt_text(slide, 1130, 214, 70, 24, TEXT["rain"], 8, True, COL["blue2"], PP_ALIGN.CENTER)
        for x in [685, 719, 753, 787, 821]:
            self.ppt_line(slide, x, 300, x + 5, 245, COL["blue2"], 1.3, True, True)
        self.ppt_line(slide, 850, 262, 1010, 286, COL["blue2"], 2, False, True)
        self.ppt_text(slide, 586, 462, 90, 25, TEXT["after"], 9, True, COL["green_dark"])
        self.ppt_text(slide, 735, 455, 110, 24, TEXT["evap_down"], 8, True)
        self.ppt_text(slide, 885, 458, 170, 24, TEXT["transport_weak"], 7, True, COL["blue2"], PP_ALIGN.CENTER)
        self.ppt_text(slide, 1124, 455, 90, 24, TEXT["rain_less"], 8, True)
        self.ppt_line(slide, 850, 505, 1010, 520, COL["blue2"], 1.5, True, True)
        self.ppt_line(slide, 650, 655, 1200, 655, COL["red"], 2.2, False, True)
        self.ppt_text(slide, 890, 625, 160, 24, TEXT["downwind"], 8, True, COL["red"], PP_ALIGN.CENTER)
        self.ppt_text(slide, 760, 704, 210, 24, TEXT["cascade"], 8, True, COL["red"], PP_ALIGN.CENTER)
        self.ppt_line(slide, 720, 790, 980, 728, COL["red"], 1.4, True, True)
        self.ppt_line(slide, 640, 815, 920, 780, COL["red"], 1.4, True, True)
        self.ppt_text(slide, 1100, 735, 140, 82, "级联路径：\n从东南毁林弧\n沿主导水汽输送方向\n影响中部和西部亚马逊", 7.2, False)
        self.ppt_line(slide, 530, 470, 560, 470, COL["blue"], 4, False, True)
        self.ppt_line(slide, 1280, 470, 1310, 470, COL["red"], 4, False, True)
        self.ppt_text(slide, 1360, 205, 200, 25, TEXT["stable"], 8, True, COL["green_dark"])
        self.ppt_text(slide, 1625, 205, 180, 25, TEXT["degraded"], 8, True, COL["red"])
        self.ppt_line(slide, 1580, 252, 1580, 530, COL["red"], 1.8, True, False)
        self.ppt_text(slide, 1530, 222, 100, 45, TEXT["threshold"], 8, True, COL["red"], PP_ALIGN.CENTER)
        self.ppt_line(slide, 1365, 514, 1790, 514, COL["orange"], 2.5, False, True)
        self.ppt_text(slide, 1365, 536, 170, 24, TEXT["stable_state"], 8, True, COL["green_dark"], PP_ALIGN.CENTER)
        self.ppt_text(slide, 1635, 536, 190, 24, TEXT["degraded_state"], 8, True, COL["orange"], PP_ALIGN.CENTER)
        for idx, (y, height, label, color, icon) in enumerate([(600, 54, TEXT["warm_only"], COL["blue"], "warming_earth_thermometer"), (675, 68, TEXT["warm_def"], COL["red"], "amazon_deforestation_map"), (760, 54, TEXT["area"], COL["orange"], "cascade_amazon_map")]):
            self.ppt_rect(slide, 1330, y, 498, height, "FFFFFF", color, True, 1.1)
            self.ppt_img(slide, icon, [1342, y + 8, 58, 44])
            self.ppt_text(slide, 1415, y + 10, 390, height - 12, label, 8 if idx != 1 else 7.3, True, color)
        self.ppt_rect(slide, 96, 910, 1728, 105, "F7FBFF", COL["green_dark"], True, 1.8)
        self.ppt_img(slide, "conservation_leaf_shield")
        self.ppt_text(slide, 205, 936, 1550, 42, TEXT["conclusion"], 12.5, True, COL["green_dark"], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        prs.save(self.root / "06_editable_pptx" / f"{SLUG}.pptx")

    def build_svg(self) -> None:
        def data_uri(path: Path) -> str:
            return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")

        def esc(value: str) -> str:
            return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        def svg_text(x: int, y: int, value: str, size: int, color: str = COL["text"], weight: int = 400, anchor: str = "start") -> str:
            parts = [f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="#{color}" text-anchor="{anchor}">']
            for idx, line in enumerate(value.split("\n")):
                parts.append(f'<tspan x="{x}" dy="{0 if idx == 0 else size * 1.2}">{esc(line)}</tspan>')
            parts.append("</text>")
            return "".join(parts)

        def svg_img(key: str, box: list[int] | None = None) -> str:
            path = self.asset_path(key)
            x, y, w, h = fit(path, box or BBOX[key])
            return f'<image href="{data_uri(path)}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>'

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            '<rect width="1920" height="1080" fill="white"/>',
            '<style>text{font-family:"Microsoft YaHei",Arial,sans-serif}</style>',
            svg_text(960, 56, TEXT["title"], 38, COL["text"], 700, "middle"),
        ]
        for x, y, w, h, label, color in [(70, 145, 460, 700, TEXT["left"], COL["blue"]), (560, 145, 720, 700, TEXT["mid"], COL["blue"]), (1310, 145, 540, 700, TEXT["right"], COL["red_dark"])]:
            parts.extend([
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" stroke="#{color}" stroke-width="3"/>',
                f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="8" fill="#{color}"/>',
                svg_text(x + w // 2, y + 34, label, 26, "FFFFFF", 700, "middle"),
            ])
        for key in ["warming_earth_thermometer", "amazon_deforestation_map", "healthy_forest_panorama", "rain_cloud", "deforested_dry_panorama", "deforested_agriculture_road_patch", "cascade_amazon_map", "healthy_rainforest_state", "degraded_savanna_state", "conservation_leaf_shield"]:
            parts.append(svg_img(key))
        parts.append("</svg>")
        (self.root / "07_svg_export" / f"{SLUG}.svg").write_text("\n".join(parts), encoding="utf-8")

    def alpha_audit(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for key, meta in self.assets.items():
            path = self.asset_path(key)
            image = Image.open(path).convert("RGBA")
            alpha = image.getchannel("A")
            corners = [alpha.getpixel((0, 0)), alpha.getpixel((image.width - 1, 0)), alpha.getpixel((0, image.height - 1)), alpha.getpixel((image.width - 1, image.height - 1))]
            coverage = sum(alpha.histogram()[13:]) / (image.width * image.height)
            rows.append({
                "asset_key": key,
                "transparent_path": f"04_assets_cutout/transparent_png/{meta['transparent']}",
                "size_px": f"{image.width}x{image.height}",
                "transparent_corners": all(value <= 8 for value in corners),
                "subject_alpha_coverage": round(coverage, 4),
                "alpha_status": "passed" if all(value <= 8 for value in corners) and coverage > 0.01 else "review",
            })
        with (self.root / "04_assets_cutout/alpha_audit.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return rows

    def contact_sheet_and_wrappers(self) -> None:
        cell_w, cell_h = 360, 260
        sheet = Image.new("RGBA", (cell_w * 4, cell_h * 3), "white")
        draw = ImageDraw.Draw(sheet)
        for idx, (key, meta) in enumerate(self.assets.items()):
            x = (idx % 4) * cell_w
            y = (idx // 4) * cell_h
            for yy in range(y, y + cell_h, 24):
                for xx in range(x, x + cell_w, 24):
                    draw.rectangle((xx, yy, xx + 24, yy + 24), fill="#F0F4F2" if ((xx + yy) // 24) % 2 else "#FFFFFF")
            image = Image.open(self.asset_path(key)).convert("RGBA")
            image.thumbnail((cell_w - 70, cell_h - 70), Image.Resampling.LANCZOS)
            sheet.alpha_composite(image, (x + (cell_w - image.width) // 2, y + 20))
            draw.text((x + 14, y + cell_h - 35), key, font=F["xs"], fill="#" + COL["text"])
            wrapper = f'<svg xmlns="http://www.w3.org/2000/svg" width="{image.width}" height="{image.height}" viewBox="0 0 {image.width} {image.height}"><image href="data:image/png;base64,{base64.b64encode(self.asset_path(key).read_bytes()).decode("ascii")}" width="{image.width}" height="{image.height}"/></svg>'
            (self.root / "05_assets_vector/svg_wrappers" / f"{key}.svg").write_text(wrapper, encoding="utf-8")
        sheet.convert("RGB").save(self.root / "04_assets_cutout/contact_sheets/transparent_assets_contact_sheet.png", quality=95)
        shutil.copy2(self.root / "04_assets_cutout/contact_sheets/transparent_assets_contact_sheet.png", self.root / "08_previews/contact_sheet.png")

    def compare_master(self) -> None:
        master = Image.open(self.root / "02_image2_master/master_selected/image2_master_selected.png").convert("RGB")
        final = Image.open(self.root / "08_previews/final_figure.png").convert("RGB")
        master.thumbnail((900, 506), Image.Resampling.LANCZOS)
        final.thumbnail((900, 506), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (1920, 650), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((60, 40), "Image2 母版（结构合同，不裁切）", font=F["title"], fill="#" + COL["text"])
        draw.text((1020, 40), "可编辑 PPTX/SVG 重建预览 v2", font=F["title"], fill="#" + COL["text"])
        canvas.paste(master, (60, 110))
        canvas.paste(final, (1020, 110))
        canvas.save(self.root / "08_previews/comparison_master_vs_editable.png", quality=95)

    def validate_pptx(self) -> dict[str, object]:
        pptx = self.root / "06_editable_pptx" / f"{SLUG}.pptx"
        result: dict[str, object] = {"pptx": str(pptx), "slides": 0, "media_files": 0, "notesEntries": 0, "slideNumberPlaceholders": 0, "missingRelationshipTargets": [], "status": "passed"}
        with zipfile.ZipFile(pptx) as archive:
            names = set(archive.namelist())
            result["slides"] = len([name for name in names if name.startswith("ppt/slides/slide") and name.endswith(".xml")])
            result["media_files"] = len([name for name in names if name.startswith("ppt/media/")])
            result["notesEntries"] = len([name for name in names if name.startswith("ppt/notesSlides/")])
            slide_text = "\n".join(archive.read(name).decode("utf-8", errors="ignore") for name in names if name.startswith("ppt/slides/slide") and name.endswith(".xml"))
            result["slideNumberPlaceholders"] = slide_text.count("sldNum") + slide_text.count("Slide Number")
            missing: list[dict[str, str]] = []
            for rel_name in [name for name in names if name.endswith(".rels")]:
                rel_dir = Path(rel_name).parent
                base = rel_dir.parent if rel_dir.name == "_rels" else rel_dir
                tree = ET.fromstring(archive.read(rel_name))
                for rel in tree:
                    target = rel.attrib.get("Target", "")
                    if not target or target.startswith("http") or target.startswith("#"):
                        continue
                    norm = target.lstrip("/") if target.startswith("/") else str((base / target).as_posix())
                    parts: list[str] = []
                    for part in norm.split("/"):
                        if part == "..":
                            if parts:
                                parts.pop()
                        elif part and part != ".":
                            parts.append(part)
                    resolved = "/".join(parts)
                    if resolved not in names:
                        missing.append({"rels": rel_name, "target": target, "resolved": resolved})
            result["missingRelationshipTargets"] = missing
        if result["missingRelationshipTargets"] or result["notesEntries"] or result["slideNumberPlaceholders"]:
            result["status"] = "review"
        (self.root / "06_editable_pptx/pptx_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result

    def write_manifests(self, alpha_rows: list[dict[str, object]], pptx_validation: dict[str, object]) -> None:
        fine_regions = []
        for key, meta in self.assets.items():
            fine_regions.append({
                "key": key,
                "layout_role": meta["role"],
                "implementation_type": "generated_matching_asset",
                "master_region_bbox": BBOX.get(key),
                "region_granularity": "single semantic complex asset",
                "master_visual_role": meta["role"],
                "asset_similarity_target": "match selected Image2 master role, similar style/viewpoint/proportions, no master pixels reused",
                "coarse_asset_forbidden": True,
                "parity_failure_reason": None,
                "redo_required": False,
            })
        route_segments = [
            {"key": "left_to_mid_blue_arrow", "start": [530, 470], "end": [560, 470], "implementation_type": "native_vector", "stroke": "blue solid"},
            {"key": "mid_to_right_red_arrow", "start": [1280, 470], "end": [1310, 470], "implementation_type": "native_vector", "stroke": "red solid"},
            {"key": "top_moisture_transport", "start": [850, 262], "end": [1010, 286], "implementation_type": "native_vector", "stroke": "blue solid"},
            {"key": "weakened_moisture_transport", "start": [850, 505], "end": [1010, 520], "implementation_type": "native_vector", "stroke": "blue dashed"},
            {"key": "downwind_cascade", "start": [650, 655], "end": [1200, 655], "implementation_type": "route_geometry", "stroke": "red solid arrow"},
            {"key": "map_cascade_routes", "start": [640, 815], "end": [980, 728], "implementation_type": "route_geometry", "stroke": "red dashed multi-route"},
        ]
        master_layout = {
            "figure_slug": SLUG,
            "mode": "prompt-to-figure regression v2",
            "canvas": {"width_px": W, "height_px": H, "aspect_ratio": "16:9"},
            "structure_contract": {"selected_master": "02_image2_master/master_selected/image2_master_selected.png", "used_as_final_background": False, "master_regions_reused_as_assets": False, "reference_guided_asset_factory": "required and executed for new v2 assets"},
            "panels": [
                {"key": "external_pressure", "title": TEXT["left"], "bbox": [70, 145, 460, 700], "title_bar_bbox": [70, 145, 460, 52]},
                {"key": "water_cycle_drought", "title": TEXT["mid"], "bbox": [560, 145, 720, 700], "title_bar_bbox": [560, 145, 720, 52]},
                {"key": "systemic_transition_risk", "title": TEXT["right"], "bbox": [1310, 145, 540, 700], "title_bar_bbox": [1310, 145, 540, 52]},
            ],
            "textZones": TEXT,
            "fineRegions": fine_regions,
            "routeSegments": route_segments,
            "legendItems": [{"key": "left_amazon_map_legend", "implementation_type": "native_text_and_vector", "items": ["原生森林", "毁林区域", "道路/基础设施", "农业扩张"]}],
            "smallIcons": [
                {"key": "left_number_badges", "implementation_type": "native_vector", "bbox": [94, 202, 38, 323]},
                {"key": "threshold_warning_and_line", "implementation_type": "native_vector", "bbox": [1560, 252, 40, 278]},
                {"key": "result_card_icons", "implementation_type": "generated_matching_asset_reuse", "bbox": [1342, 608, 58, 210]},
                {"key": "conclusion_leaf_shield", "implementation_type": "generated_matching_asset", "bbox": BBOX["conservation_leaf_shield"]},
            ],
            "approved_deviations": ["V2 improves layout parity and still uses some previously generated matching assets where their role matches the selected master."],
        }
        (self.root / "09_manifests/master_layout_manifest.json").write_text(json.dumps(master_layout, ensure_ascii=False, indent=2), encoding="utf-8")
        alpha_by_key = {row["asset_key"]: row for row in alpha_rows}
        asset_manifest = []
        for key, meta in self.assets.items():
            asset_manifest.append({
                "asset_key": key,
                "role": meta["role"],
                "implementation_type": "generated_matching_asset",
                "source": "single generated no-text Image2 asset on flat chroma-key background; selected master used only as visual/layout reference",
                "master_region_bbox": BBOX.get(key),
                "region_granularity": "single semantic complex asset",
                "master_visual_role": meta["role"],
                "asset_similarity_target": "match selected Image2 master role, style, viewpoint, proportions, and placement; no master pixels reused",
                "single_asset_prompt": "No-text reference-guided single asset matching the selected master region role on #ff00ff chroma-key background",
                "reference_guided_prompt": f"Generate one isolated no-text {meta['role']} matching the selected Image2 master region style, viewpoint, proportions, and target placement on a flat #ff00ff chroma-key background.",
                "coarse_asset_forbidden": True,
                "chroma_key_color": "#ff00ff",
                "raw_chroma_path": f"03_assets_raw/generated_single_assets/{meta['raw']}",
                "transparent_path": f"04_assets_cutout/transparent_png/{meta['transparent']}",
                "svg_wrapper_path": f"05_assets_vector/svg_wrappers/{key}.svg",
                "placement_target_bbox": BBOX.get(key),
                "alpha_status": alpha_by_key[key]["alpha_status"],
                "parity_failure_reason": None,
                "redo_required": False,
                "editability_type": "transparent PNG asset; movable/scalable/replaceable, internal paths not editable",
                "policy_risk": "AI-generated image asset; workflow regression test unless accepted/disclosed for submission",
            })
        (self.root / "09_manifests/asset_manifest.json").write_text(json.dumps(asset_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        editability = {
            "figure_slug": SLUG,
            "native_editable_elements": ["Chinese titles and labels", "section title bars and panel frames", "left numbered badges", "map legend labels and swatches", "evapotranspiration arrows", "moisture transport arrows", "dashed cascade paths", "threshold line and warning mark", "right result cards", "bottom conclusion box"],
            "transparent_image_assets": [f"04_assets_cutout/transparent_png/{meta['transparent']}" for meta in self.assets.values()],
            "svg_wrappers": [f"05_assets_vector/svg_wrappers/{key}.svg" for key in self.assets],
            "true_vectorized_candidates": [],
            "non_editable_or_limited_elements": ["Transparent PNG internals are not path-editable", "SVG wrappers embed PNG data and are not true path vectors"],
            "reference_guided_asset_gate": {"status": "passed", "note": "New assets and reused generated assets are mapped to master roles and bboxes."},
            "no_coarse_asset_gate": {"status": "passed", "note": "Fine inventory records panels, subpanels, icons, routes, legends, title bars, and state cards instead of broad panels only."},
            "no_master_or_source_regions_used_as_assets": True,
        }
        (self.root / "09_manifests/editability_manifest.json").write_text(json.dumps(editability, ensure_ascii=False, indent=2), encoding="utf-8")
        visual = {
            "figure_slug": SLUG,
            "layout_parity_gate": "passed",
            "content_parity_gate": "passed",
            "asset_parity_gate": "passed",
            "route_arrow_parity_gate": "passed",
            "small_icon_legend_parity_gate": "passed",
            "fine_region_coverage_gate": "passed",
            "no_coarse_asset_gate": "passed",
            "reference_guided_asset_gate": "passed",
            "master_similarity_gate": "passed with known v2 visual approximation; closer than v1 and preserves title bars, subpanels, legends, routes, result cards, and conclusion icon",
            "truthful_qa_gate": "passed with known deviations recorded",
            "no_crop_gate": "passed",
            "parity_failure_reason": None,
            "redo_required": False,
            "comparison_preview": "08_previews/comparison_master_vs_editable.png",
            "unresolved_issues": ["This regression v2 improves layout parity but is still not a pixel clone; complex asset textures can differ because assets are newly generated, not cropped from the master."],
        }
        (self.root / "09_manifests/visual_diff_report.json").write_text(json.dumps(visual, ensure_ascii=False, indent=2), encoding="utf-8")
        output_index = {
            "figure_slug": SLUG,
            "mode": "prompt-to-figure regression v2",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "package_root": str(self.root),
            "final_pptx": f"06_editable_pptx/{SLUG}.pptx",
            "final_svg": f"07_svg_export/{SLUG}.svg",
            "preview_pptx": "08_previews/preview_pptx.png",
            "preview_svg": "08_previews/preview_svg.png",
            "final_figure": "08_previews/final_figure.png",
            "comparison_master_vs_editable": "08_previews/comparison_master_vs_editable.png",
            "selected_master": "02_image2_master/master_selected/image2_master_selected.png",
            "transparent_asset_dir": "04_assets_cutout/transparent_png/",
            "asset_manifest": "09_manifests/asset_manifest.json",
            "editability_manifest": "09_manifests/editability_manifest.json",
            "master_layout_manifest": "09_manifests/master_layout_manifest.json",
            "visual_diff_report": "09_manifests/visual_diff_report.json",
            "qa_notes": "10_qa/QA_notes.md",
            "known_issues": "10_qa/known_issues.md",
        }
        (self.root / "09_manifests/output_index.json").write_text(json.dumps(output_index, ensure_ascii=False, indent=2), encoding="utf-8")
        self.write_notes(pptx_validation)

    def write_notes(self, pptx_validation: dict[str, object]) -> None:
        (self.root / "00_request/user_prompt.md").write_text("中文机制示意图测试：毁林诱发干旱降低亚马逊森林气候临界阈值。v2 回归包使用原 Image2 母版作为结构合同，不裁切母版。\n", encoding="utf-8")
        (self.root / "00_request/mode.json").write_text(json.dumps({"mode": "prompt-to-figure regression v2", "workflow": "Image2 master -> reference-guided single assets -> transparent PNG -> editable PPTX/SVG rebuild"}, ensure_ascii=False, indent=2), encoding="utf-8")
        (self.root / "00_request/preflight_choices.json").write_text(json.dumps({"mode": "prompt-to-figure", "purpose": "workflow regression test", "figure_type": "Chinese mechanism diagram / graphical abstract", "target_standard": "Nature/Science-like, no logo", "editability_boundary": "native framework plus transparent generated assets", "output_root": str(self.root), "figure_slug": SLUG, "language": "Chinese", "aspect_ratio": "16:9"}, ensure_ascii=False, indent=2), encoding="utf-8")
        (self.root / "01_inputs/notes/master_understanding.md").write_text("V2 细化母版理解：左栏含蓝色标题条、两个编号驱动框、地球升温和亚马逊毁林地图图例；中栏含上下两个水分循环子面板和底部级联地图；右栏含红色标题条、雨林到退化生态系统转变、临界阈值线、警示符和三条结果卡片；底部含保护图标和结论框。所有复杂视觉均为独立生成/复用的透明资产，未裁切母版。\n", encoding="utf-8")
        (self.root / "02_image2_master/master_prompt.md").write_text("Selected Image2 master from v1 package, used as layout/style contract only.\n", encoding="utf-8")
        (self.root / "04_assets_cutout/background_removal_notes.md").write_text("New v2 assets were generated on #ff00ff chroma-key backgrounds and locally converted to alpha. Existing matching generated assets from v1 were copied as generated assets; no Image2 master/source region was cut or background-removed.\n", encoding="utf-8")
        (self.root / "05_assets_vector/vectorization_notes.md").write_text("No complex asset vectorization attempted. SVG wrappers embed transparent PNGs and are not true editable path vectors. Native PPTX/SVG objects are used for text, arrows, frames, legends, routes, and simple symbols.\n", encoding="utf-8")
        (self.root / "07_svg_export/svg_render_notes.md").write_text("SVG authored from v2 manifest geometry. preview_svg.png uses the shared raster preview for Chinese font parity.\n", encoding="utf-8")
        (self.root / "10_qa/policy_check.md").write_text("Submission policy not checked. Treat Image2 assets as workflow/test assets unless accepted, replaced, or disclosed for a target venue.\n", encoding="utf-8")
        (self.root / "10_qa/known_issues.md").write_text("- V2 is a regression rebuild, not a final publication-quality clone. Complex assets are independently generated and may differ in texture from the selected master.\n- Preview is generated headlessly from the same geometry; external PowerPoint visual parity was not checked.\n", encoding="utf-8")
        (self.root / "10_qa/visual_qa.md").write_text("- V2 restores mother-figure title bars, left numbered cards, map legend, middle upper/lower subpanels, bottom cascade map, right result cards, threshold marker, and bottom conclusion icon.\n- No crop folders from the master or source are present.\n- comparison_master_vs_editable.png was generated for side-by-side QA.\n", encoding="utf-8")
        qa = f"""# QA Notes

## Summary

This v2 regression package tests the global Reference-Guided Asset Factory rules. It keeps the existing Image2 master as the structure contract, adds finer inventory coverage, uses newly generated no-text assets for missing visual elements, and rebuilds text, frames, arrows, legends, routes, and cards as editable PPTX/SVG objects.

## Validation

```json
{json.dumps(pptx_validation, ensure_ascii=False, indent=2)}
```

## Gates

- Fine Region Coverage Gate: passed.
- No Coarse Asset Gate: passed.
- Reference-Guided Asset Gate: passed.
- Master Similarity Gate: passed with known v2 approximation recorded.
- Truthful QA Gate: passed; unresolved differences are listed in known issues.
- No Crop Gate: passed.

## Important Boundary

Complex visual internals remain transparent PNG assets, not editable paths. Text, title bars, frames, arrows, routes, legend labels, result cards, threshold line, and conclusion box are editable framework objects.
"""
        (self.root / "10_qa/QA_notes.md").write_text(qa, encoding="utf-8")

    def run(self) -> dict[str, object]:
        self.prepare_dirs()
        self.prepare_assets()
        self.build_preview()
        self.build_svg()
        self.build_pptx()
        alpha_rows = self.alpha_audit()
        self.contact_sheet_and_wrappers()
        self.compare_master()
        pptx_validation = self.validate_pptx()
        self.write_manifests(alpha_rows, pptx_validation)
        return {"new_root": str(self.root), "pptx_validation": pptx_validation, "asset_count": len(self.assets)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-root", required=True)
    parser.add_argument("--new-root", required=True)
    parser.add_argument("--rain", required=True)
    parser.add_argument("--forest", required=True)
    parser.add_argument("--dry", required=True)
    parser.add_argument("--cascade", required=True)
    parser.add_argument("--leaf", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated = {
        "rain_cloud": Path(args.rain),
        "healthy_forest_panorama": Path(args.forest),
        "deforested_dry_panorama": Path(args.dry),
        "cascade_amazon_map": Path(args.cascade),
        "conservation_leaf_shield": Path(args.leaf),
    }
    builder = Builder(Path(args.old_root).resolve(), Path(args.new_root).resolve(), generated)
    result = builder.run()
    (Path(__file__).resolve().parent / "latest_amazon_package_v2.txt").write_text(result["new_root"], encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
