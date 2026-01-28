#!/usr/bin/env python3
"""Generate social-preview.png for PE Collective (1200x630px)"""

from PIL import Image, ImageDraw, ImageFont
import os

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
LOGO_PATH = os.path.join(PROJECT_DIR, "site", "assets", "logo.jpeg")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "site", "assets", "social-preview.png")

# Brand colors
BG_COLOR = (15, 45, 53)        # #0f2d35
TEAL_ACCENT = (26, 74, 86)     # #1a4a56
GOLD = (232, 168, 124)          # #e8a87c
WHITE = (255, 255, 255)
LIGHT_TEXT = (168, 197, 204)    # #a8c5cc

# Dimensions
WIDTH, HEIGHT = 1200, 630


def get_font(size, bold=False):
    """Try to load a system font, fall back to default."""
    font_paths = [
        # macOS
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)


def generate():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Subtle gradient overlay (top-center radial glow)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Distance from top-center
            dx = (x - WIDTH / 2) / (WIDTH / 2)
            dy = y / HEIGHT
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < 1.2:
                alpha = max(0, 1 - dist / 1.2) * 0.12
                r, g, b = img.getpixel((x, y))
                r = int(r + (61 - r) * alpha)
                g = int(g + (138 - g) * alpha)
                b = int(b + (154 - b) * alpha)
                img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    # Gold accent bar at top
    draw.rectangle([0, 0, WIDTH, 4], fill=GOLD)

    # Load and place logo
    logo_size = 100
    logo_x = 80
    logo_y = HEIGHT // 2 - logo_size // 2 - 30

    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Create circular mask
        mask = Image.new("L", (logo_size, logo_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, logo_size, logo_size], fill=255)

        # Draw circle border
        draw.ellipse(
            [logo_x - 3, logo_y - 3, logo_x + logo_size + 3, logo_y + logo_size + 3],
            outline=GOLD,
            width=2,
        )

        img.paste(logo, (logo_x, logo_y), mask)

    # Text area starts after logo
    text_x = logo_x + logo_size + 50

    # Site name
    font_name = get_font(28, bold=True)
    draw.text((text_x, logo_y - 10), "PE COLLECTIVE", fill=GOLD, font=font_name)

    # Main title
    font_title = get_font(44, bold=True)
    title_lines = ["Prompt engineering from", "people who actually do it"]
    y_offset = logo_y + 40
    for line in title_lines:
        draw.text((text_x, y_offset), line, fill=WHITE, font=font_title)
        y_offset += 54

    # Subtitle
    font_sub = get_font(22)
    subtitle = "Guides, salaries, and AI jobs from 1,300+ prompt engineers."
    draw.text((text_x, y_offset + 20), subtitle, fill=LIGHT_TEXT, font=font_sub)

    # Bottom bar with URL
    draw_rounded_rect(draw, [text_x, y_offset + 70, text_x + 280, y_offset + 105], 4, TEAL_ACCENT)
    font_url = get_font(18)
    draw.text((text_x + 15, y_offset + 77), "pecollective.com", fill=GOLD, font=font_url)

    # Save
    img.save(OUTPUT_PATH, "PNG", optimize=True)
    print(f"Social preview saved to: {OUTPUT_PATH}")
    print(f"Size: {WIDTH}x{HEIGHT}px")


if __name__ == "__main__":
    generate()
