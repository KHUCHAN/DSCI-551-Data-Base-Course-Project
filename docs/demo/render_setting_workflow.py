from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
DEMO_DIR = ROOT / "docs" / "demo"
TMP_DIR = DEMO_DIR / "tmp"
OUTPUT_PATH = DEMO_DIR / "setting_workflow.png"

ROWS = [
    {
        "title": "1. Reset and Start Environment",
        "desc": "Bring up a clean AGE-enabled PostgreSQL container from the repository root.",
        "files": [
            "scripts/reset_pipeline.sh",
            "README.md",
        ],
        "image": TMP_DIR / "row1.png",
    },
    {
        "title": "2. Load Data and Build Graphs",
        "desc": "Generate synthetic CSVs, load relational tables, then project the workload into AGE.",
        "files": [
            "src/data_generation/generate_synthetic_data.py",
            "database/migrations/001_schema.sql",
            "database/seeds/load_from_csv.sql",
            "database/setup_age.sql",
            "database/seeds/load_age_graph.sql",
            "database/seeds/load_age_graph_tuned.sql",
        ],
        "image": TMP_DIR / "row2.png",
    },
    {
        "title": "3. Demo Queries and Benchmark",
        "desc": "Show the AML queries in order, then optionally run the performance benchmark.",
        "files": [
            "database/queries/smurfing_detection.sql",
            "database/queries/smurfing_detection_age.sql",
            "database/queries/circular_trading_recursive.sql",
            "database/queries/circular_trading_cypher.sql",
            "database/queries/circular_trading_cypher_tuned.sql",
            "src/analysis/benchmark_cycle_queries.py",
        ],
        "image": TMP_DIR / "row3.png",
    },
]

PAGE_W, PAGE_H = 1800, 1200
BG = "#f5f7fb"
PANEL_BG = "#ffffff"
PANEL_BORDER = "#d7dfeb"
TITLE_COLOR = "#10233f"
TEXT_COLOR = "#2a3c57"
SUBTLE_TEXT = "#4d6282"
ACCENT = "#4367c7"
FILE_BG = "#eef3ff"


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates: list[str] = []

    if mono:
        candidates.extend(
            [
                "/System/Library/Fonts/SFNSMono.ttf",
                "/System/Library/Fonts/Menlo.ttc",
                "/Library/Fonts/Menlo.ttc",
            ]
        )
    elif bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/Library/Fonts/Arial Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/Library/Fonts/Arial.ttf",
            ]
        )

    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue

    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        test = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_file_badges(
    draw: ImageDraw.ImageDraw,
    files: list[str],
    x: int,
    y: int,
    max_width: int,
    badge_font: ImageFont.ImageFont,
) -> int:
    cursor_x = x
    cursor_y = y
    line_height = 0
    gap_x = 10
    gap_y = 8

    for file_label in files:
        text_bbox = draw.textbbox((0, 0), file_label, font=badge_font)
        badge_w = (text_bbox[2] - text_bbox[0]) + 22
        badge_h = (text_bbox[3] - text_bbox[1]) + 14

        if cursor_x + badge_w > x + max_width:
            cursor_x = x
            cursor_y += line_height + gap_y
            line_height = 0

        draw.rounded_rectangle(
            (cursor_x, cursor_y, cursor_x + badge_w, cursor_y + badge_h),
            radius=10,
            fill=FILE_BG,
            outline=PANEL_BORDER,
            width=1,
        )
        draw.text((cursor_x + 11, cursor_y + 7), file_label, fill=ACCENT, font=badge_font)

        cursor_x += badge_w + gap_x
        line_height = max(line_height, badge_h)

    return cursor_y + line_height


def main() -> None:
    img = Image.new("RGB", (PAGE_W, PAGE_H), BG)
    draw = ImageDraw.Draw(img)

    font_title = load_font(42, bold=True)
    font_header = load_font(26, bold=True)
    font_body = load_font(17)
    font_footer = load_font(16)
    font_label = load_font(15, bold=True)
    font_badge = load_font(14, mono=True)

    margin_x = 42
    header_y = 32

    draw.text((margin_x, header_y), "Hybrid-AML Shell Setup Workflow", fill=TITLE_COLOR, font=font_title)
    draw.text(
        (PAGE_W - 560, header_y + 18),
        "Docker Desktop + reset_pipeline.sh + PostgreSQL + Apache AGE",
        fill=TEXT_COLOR,
        font=font_footer,
    )

    content_top = 118
    content_bottom = 36
    row_gap = 22
    panel_h = (PAGE_H - content_top - content_bottom - row_gap * 2) // 3
    panel_x1 = margin_x
    panel_x2 = PAGE_W - margin_x

    for idx, row in enumerate(ROWS):
        y1 = content_top + idx * (panel_h + row_gap)
        y2 = y1 + panel_h
        draw.rounded_rectangle((panel_x1, y1, panel_x2, y2), radius=18, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
        draw.rounded_rectangle((panel_x1 + 18, y1 + 16, panel_x1 + 34, y1 + 32), radius=4, fill=ACCENT)

        draw.text((panel_x1 + 48, y1 + 10), row["title"], fill=TITLE_COLOR, font=font_header)

        desc_lines = wrap_text(draw, row["desc"], font_body, panel_x2 - panel_x1 - 90)
        desc_y = y1 + 46
        for line in desc_lines:
            draw.text((panel_x1 + 48, desc_y), line, fill=TEXT_COLOR, font=font_body)
            desc_y += 22

        label_y = desc_y + 6
        draw.text((panel_x1 + 48, label_y), "Relevant files:", fill=SUBTLE_TEXT, font=font_label)

        badges_end_y = draw_file_badges(
            draw,
            row["files"],
            panel_x1 + 160,
            label_y - 3,
            panel_x2 - panel_x1 - 210,
            font_badge,
        )

        row_img = Image.open(row["image"]).convert("RGBA")
        max_w = panel_x2 - panel_x1 - 56
        image_top = badges_end_y + 18
        max_h = y2 - image_top - 18
        scale = min(max_w / row_img.width, max_h / row_img.height)
        new_size = (max(1, int(row_img.width * scale)), max(1, int(row_img.height * scale)))
        row_img = row_img.resize(new_size, Image.LANCZOS)
        paste_x = panel_x1 + (panel_x2 - panel_x1 - row_img.width) // 2
        paste_y = image_top + max(0, (max_h - row_img.height) // 2)
        img.paste(row_img, (paste_x, paste_y), row_img)

    img.save(OUTPUT_PATH)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
