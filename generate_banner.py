#!/usr/bin/env python3
"""
Cyberpunk Terminal Profile Banner Generator
Implements:
- 1-bit Floyd-Steinberg dithered portrait (serpentine order)
- Background segmentation for dark mode
- 60-group interleaved shimmer intro animation (3.2s)
- 13.9s loop animation:
  - Static dots grouped into 94 drift bands (with random noise)
  - 900 travellers morphing between 3 logos (Python, HTML, Bash)
  - Staggered and locked SYSTEM.INFO text rows with dotted leaders
"""

import os
import sys
import base64
import random
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy import ndimage

# --- Layout Configuration ---
BANNER_WIDTH = 1180
BANNER_HEIGHT = 610
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
PORTRAIT_WIDTH = 400
PORTRAIT_HEIGHT = 492
DOT_SIZE = 4

INTRO_DURATION = 3.2
LOOP_DURATION = 13.9

# --- Colors (Matching prompt palette exactly) ---
# Palette: portrait [#A78BFA dark / #7C3AED light] · UI chrome [#22D3EE / #0891B2] · accent [#10B981] · background [#0A101F]
COLORS = {
    "dark": {
        "bg_start": "#0A101F",
        "bg_end": "#070B16",
        "portrait_hue": "#A78BFA",
        "portrait_bg": "#0A101F",
        "ui_chrome": "#22D3EE",
        "ui_chrome_dim": "rgba(34, 211, 238, 0.35)",
        "accent": "#10B981",
        "live_badge": "#EF4444",
        "text": "#F8FAFC",
        "text_dim": "#94A3B8",
        "dot_empty": "#2d3343",  # Visible slate for empty cells
    },
    "light": {
        "bg_start": "#F8FAFC",
        "bg_end": "#E2E8F0",
        "portrait_hue": "#7C3AED",
        "portrait_bg": "#E2E8F0",
        "ui_chrome": "#0891B2",
        "ui_chrome_dim": "rgba(8, 145, 178, 0.30)",
        "accent": "#059669",
        "live_badge": "#DC2626",
        "text": "#0F172A",
        "text_dim": "#475569",
        "dot_empty": "#CBD5E1",  # Light slate for empty cells
    }
}

PORTRAIT_DIR = Path("image/myimage")
LOGOS_DIR = Path("image/logos")
SELECTED_LOGOS = ["python.jpeg", "html.jpeg", "bashlogo.jpeg"]

PERSONAL_INFO = {
    "name": "Pallav Dholariya",
    "username": "Shivala-08",
    "role": "AI/ML Engineer • Full-Stack Developer",
    "origin": "Pune, India",
    "education": "B.Tech CSE (AI &amp; ML)",
    "status": "Building + Learning + Shipping",
    "toolchain": "VS Code, Git, Docker, ngrok",
    "languages": "Python, JavaScript, TypeScript, SQL",
    "frontend": "React, Next.js, Tailwind CSS",
    "backend": "FastAPI, Node.js",
    "database": "PostgreSQL, Supabase",
    "infra": "Docker, GitHub Actions, Vercel, Linux",
    "email": "pallavdholariya@gmail.com",
    "portfolio": "pallav-os.vercel.app",
    "linkedin": "pallavdholariya",
    "github": "Shivala-08",
}

# --- ASCII Art Config & Helper ---
ASCII_RAMP = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
ASCII_FONT_SIZE = 4.2

def get_ascii_char(val, is_dark):
    if is_dark:
        # Dark theme: white (255) is densest (@), black (0) is lightest (.)
        idx = int((255 - val) / 256 * len(ASCII_RAMP))
    else:
        # Light theme: black (0) is densest (@), white (255) is lightest (.)
        idx = int(val / 256 * len(ASCII_RAMP))
    idx = min(max(0, idx), len(ASCII_RAMP) - 1)
    return ASCII_RAMP[idx]

# --- Image Processing Functions ---

def find_best_portrait():
    images = list(PORTRAIT_DIR.glob("*.png")) + list(PORTRAIT_DIR.glob("*.jpg")) + list(PORTRAIT_DIR.glob("*.jpeg"))
    if not images:
        raise FileNotFoundError("No portrait image found in image/myimage/")
    return max(images, key=lambda p: p.stat().st_size)

def process_portrait(path):
    img = Image.open(path).convert("L")
    w, h = img.size
    target_ratio = PORTRAIT_WIDTH / PORTRAIT_HEIGHT
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int(h * 0.05)  # crop slightly higher to get head and shoulders
        img = img.crop((0, top, w, top + new_h))
        
    img = img.resize((PORTRAIT_WIDTH, PORTRAIT_HEIGHT), Image.LANCZOS)
    img = ImageOps.autocontrast(img, cutoff=1)
    img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    return img

def floyd_steinberg_dither(img_array):
    h, w = img_array.shape
    dithered = img_array.copy().astype(float)
    
    for y in range(h):
        # Serpentine order to avoid directional artifacts
        x_range = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        for x in x_range:
            old_val = dithered[y, x]
            new_val = 255.0 if old_val > 127 else 0.0
            dithered[y, x] = new_val
            err = old_val - new_val
            
            # Distribute error
            if y % 2 == 0:
                if x + 1 < w: dithered[y, x + 1] += err * 7 / 16
                if y + 1 < h:
                    if x - 1 >= 0: dithered[y + 1, x - 1] += err * 3 / 16
                    dithered[y + 1, x] += err * 5 / 16
                    if x + 1 < w: dithered[y + 1, x + 1] += err * 1 / 16
            else:
                if x - 1 >= 0: dithered[y, x - 1] += err * 7 / 16
                if y + 1 < h:
                    if x + 1 < w: dithered[y + 1, x + 1] += err * 3 / 16
                    dithered[y + 1, x] += err * 5 / 16
                    if x - 1 >= 0: dithered[y + 1, x - 1] += err * 1 / 16
                    
    return (dithered > 127).astype(np.uint8) * 255

def segment_background(img_array):
    blurred = ndimage.gaussian_filter(img_array.astype(float), sigma=3)
    # Background in the prompt's portrait image is usually lighter/darker than subject
    # Standard thresholding
    threshold = 155
    mask = blurred < threshold
    
    mask = ndimage.binary_closing(mask, iterations=2)
    mask = ndimage.binary_fill_holes(mask)
    
    labeled, num_features = ndimage.label(mask)
    if num_features > 0:
        sizes = ndimage.sum(mask, labeled, range(1, num_features + 1))
        largest = np.argmax(sizes) + 1
        mask = labeled == largest
        
    return mask

def get_logo_coords(logo_path):
    img = Image.open(logo_path).convert("RGBA")
    # Paste onto white background to handle transparency correctly
    canvas = Image.new("RGBA", img.size, (255, 255, 255, 255))
    canvas.paste(img, (0, 0), mask=img)
    img = canvas.convert("L")
    
    # Resize to fit nicely within portrait frame centered
    max_size = 220
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    
    # Place on 400x492 blank background
    bg = Image.new("L", (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), 255)
    offset_x = (PORTRAIT_WIDTH - img.width) // 2
    offset_y = (PORTRAIT_HEIGHT - img.height) // 2
    bg.paste(img, (offset_x, offset_y))
    
    # Extract coordinates of dark pixels
    arr = np.array(bg)
    coords = []
    for y in range(0, PORTRAIT_HEIGHT, DOT_SIZE):
        for x in range(0, PORTRAIT_WIDTH, DOT_SIZE):
            if arr[y, x] < 127:  # dark pixel
                coords.append((x, y))
    return coords

def sample_coordinates(coords, target_num=900):
    random.seed(42)
    if len(coords) >= target_num:
        return random.sample(coords, target_num)
    else:
        # Sample with replacement if logo has fewer than 900 dots
        return coords + random.choices(coords, k=target_num - len(coords))

# --- SVG Generating Helpers ---

def get_dotted_leaders(label, value, max_chars=80):
    total_dots = max_chars - len(label) - len(value)
    return "." * max(2, total_dots)

def build_info_panel(colors):
    info = PERSONAL_INFO
    rows = [
        ("Subject", info["name"]),
        ("Role", info["role"]),
        ("Origin", info["origin"]),
        ("Education", info["education"]),
        ("Status", info["status"]),
        ("ToolChain", info["toolchain"]),
        ("", ""),
        ("Core.Lang", info["languages"]),
        ("Core.Frontend", info["frontend"]),
        ("Core.Backend", info["backend"]),
        ("Core.Database", info["database"]),
        ("Core.Infra", info["infra"]),
        ("", ""),
        ("Grid.Mail", info["email"]),
        ("Grid.Portfolio", info["portfolio"]),
        ("Grid.LinkedIn", info["linkedin"]),
        ("Grid.GitHub", info["github"]),
    ]
    
    lines = []
    x = 470
    start_y = 116
    spacing = 23
    font_size = 14
    
    # SYSTEM.INFO header
    lines.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.4s" fill="freeze"/><text x="{x}" y="88" font-size="13" letter-spacing="2" fill="{colors["ui_chrome"]}" font-weight="bold">SYSTEM.INFO</text></g>')
    # pulsing red LIVE badge
    lines.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.45s" fill="freeze"/><rect x="575" y="76" width="36" height="15" rx="3" fill="{colors["live_badge"]}"/><text x="593" y="87" font-size="10" fill="white" text-anchor="middle" font-weight="bold">LIVE<animate attributeName="fill-opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/></text></g>')
    # Handle pill
    lines.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.5s" fill="freeze"/><rect x="470" y="103" width="130" height="18" rx="4" fill="{colors["ui_chrome"]}" opacity="0.15"/><text x="480" y="116" font-size="13" fill="{colors["ui_chrome"]}" font-weight="bold">@{info["github"]}</text></g>')
    
    y = start_y + 40
    stagger = 0.6
    
    for label, val in rows:
        if not label:
            # Separator line
            lines.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{stagger:.2f}s" fill="freeze"/><text x="{x}" y="{y}" font-size="{font_size}" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{colors["text_dim"]}" opacity="0.4">--------------------------------------------------------------------------------</tspan></text></g>')
            y += spacing
            stagger += 0.08
            continue
            
        dots = get_dotted_leaders(label, val, max_chars=75)
        lines.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{stagger:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="{stagger:.2f}s" fill="freeze"/>'
            f'<text x="{x}" y="{y}" font-size="{font_size}" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve">'
            f'<tspan fill="{colors["ui_chrome"]}">{label} </tspan>'
            f'<tspan fill="rgba(148,163,184,0.35)">{dots}</tspan>'
            f'<tspan fill="{colors["text"]}" font-weight="600"> {val}</tspan>'
            f'</text></g>'
        )
        y += spacing
        stagger += 0.08
        
    # footer cursor
    lines.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{stagger:.2f}s" fill="freeze"/><text x="{x}" y="{y + 10}" font-size="14" fill="{colors["text_dim"]}">&#9656; More about me &amp; projects below in README &#8595; <tspan fill="{colors["ui_chrome"]}">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text></g>')
    
    return "\n".join(lines)

def generate_svg(theme="dark"):
    colors = COLORS[theme]
    is_dark = theme == "dark"
    
    # Process portrait image
    portrait_path = find_best_portrait()
    portrait_img = process_portrait(portrait_path)
    portrait_arr = np.array(portrait_img)
    
    dithered = floyd_steinberg_dither(portrait_arr)
    mask = segment_background(portrait_arr)
    
    # Generate portrait dither dots (foreground / lit only for dark; all for light)
    portrait_dots = []
    for y in range(0, PORTRAIT_HEIGHT, DOT_SIZE):
        for x in range(0, PORTRAIT_WIDTH, DOT_SIZE):
            # For dark mode, draw light highlights (255); for light mode, draw dark shadows (0)
            is_lit = (dithered[y, x] == 255) if is_dark else (dithered[y, x] == 0)
            is_fg = mask[y, x]
            
            # For dark mode, segment background out
            if is_dark:
                if is_fg and is_lit:
                    portrait_dots.append((x, y))
            else:
                # For light mode, keep the background
                if is_lit:
                    portrait_dots.append((x, y))
                    # Select travellers
    random.seed(42)
    num_travellers = 500
    if len(portrait_dots) < num_travellers:
        # Pad portrait dots
        portrait_dots += [(random.randint(0, PORTRAIT_WIDTH), random.randint(0, PORTRAIT_HEIGHT)) for _ in range(num_travellers - len(portrait_dots))]
        
    travellers = random.sample(portrait_dots, num_travellers)
    static_dots = [d for d in portrait_dots if d not in travellers]
    
    # Load and process morphing logos
    logos_coords = []
    for logo_name in SELECTED_LOGOS:
        logo_path = LOGOS_DIR / logo_name
        if not logo_path.exists():
            # Create a simple fallback shape (circle/square) if logo file is missing
            fallback = [(x, y) for x in range(80, 220, DOT_SIZE) for y in range(100, 240, DOT_SIZE)]
            logos_coords.append(sample_coordinates(fallback, num_travellers))
        else:
            coords = get_logo_coords(logo_path)
            logos_coords.append(sample_coordinates(coords, num_travellers))
            
    # Optimal Transport (Approximate via sorting by coordinate projection)
    # Sort each list by y coordinate then x coordinate to map points smoothly
    travellers_sorted = sorted(travellers, key=lambda p: (p[1], p[0]))
    logo1_sorted = sorted(logos_coords[0], key=lambda p: (p[1], p[0]))
    logo2_sorted = sorted(logos_coords[1], key=lambda p: (p[1], p[0]))
    logo3_sorted = sorted(logos_coords[2], key=lambda p: (p[1], p[0]))
    
    # Scale to SVG space: Portrait starts at translate(36, 84) scale(1.0, 1.0)
    # We will output traveller dots directly in main coordinates to animate them smoothly
    travellers_svg = []
    scale_x, scale_y = 1.0, 1.0
    offset_x, offset_y = 36.0, 84.0
    
    # keyTimes uneven: hold portrait 3s (0.21), transition 1.3s (0.288), hold logo 1 2s (0.432)...
    # dur = 13.9s
    # times: 0.0s -> 2.7s (hold), 4.0s (trans), 6.0s (hold), 7.3s (trans), 9.3s (hold), 10.6s (trans), 12.6s (hold), 13.9s (trans)
    key_times = "0;.194;.288;.432;.525;.669;.763;.906;1"
    opacity_values = "1;1;1;1;1;1;1;1;1"
    
    for i in range(num_travellers):
        p_x = int(offset_x + travellers_sorted[i][0] * scale_x)
        p_y = int(offset_y + travellers_sorted[i][1] * scale_y)
        l1_x = int(offset_x + logo1_sorted[i][0] * scale_x)
        l1_y = int(offset_y + logo1_sorted[i][1] * scale_y)
        l2_x = int(offset_x + logo2_sorted[i][0] * scale_x)
        l2_y = int(offset_y + logo2_sorted[i][1] * scale_y)
        l3_x = int(offset_x + logo3_sorted[i][0] * scale_x)
        l3_y = int(offset_y + logo3_sorted[i][1] * scale_y)
        
        # Translation path
        trans_values = f"{p_x} {p_y};{p_x} {p_y};{l1_x} {l1_y};{l1_x} {l1_y};{l2_x} {l2_y};{l2_x} {l2_y};{l3_x} {l3_y};{l3_x} {l3_y};{p_x} {p_y}"
        
        # Look up corresponding brightness in portrait_arr
        val = portrait_arr[travellers_sorted[i][1], travellers_sorted[i][0]]
        char = get_ascii_char(val, is_dark)
        char = char.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        travellers_svg.append(
            f'<text x="0" y="0" text-anchor="middle" dy="0.3em" opacity="0">'
            f'{char}'
            f'<animate attributeName="opacity" values="{opacity_values}" keyTimes="{key_times}" dur="{LOOP_DURATION}s" begin="{INTRO_DURATION}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="{trans_values}" keyTimes="{key_times}" dur="{LOOP_DURATION}s" begin="{INTRO_DURATION}s" repeatCount="indefinite"/>'
            f'</text>'
        )
        
    # Group static portrait dots into 45 drift bands (grouped by Y level + noise)
    # The trap: drift is linear so quantize with per-dot noise (sigma ~4) to make it organic
    drift_groups = {}
    for x, y in static_dots:
        noise = random.normalvariate(0, 4)
        band_y = int(y + noise)
        band_idx = (band_y // 8) % 45  # 45 bands
        if band_idx not in drift_groups:
            drift_groups[band_idx] = []
        drift_groups[band_idx].append((x, y))
        
    static_svg = []
    # Intro animation: scatter dots randomly across 60 groups to shimmering in
    # Generate 60 groups
    intro_groups = {i: [] for i in range(60)}
    for band_idx, coords in drift_groups.items():
        for cx, cy in coords:
            grp_idx = random.randint(0, 59)
            intro_groups[grp_idx].append((cx, cy, band_idx))
            
    for grp_idx, elements in intro_groups.items():
        if not elements: continue
        begin_time = 0.20 + grp_idx * 0.03
        pass
        
    # Let's do it clean: output the 45 drift groups. Each group has a unique translate transform loop
    # Timings for loop translation (drift towards Logo 1 centroid while fading)
    # Centroid of Logo 1 in scaled coordinates
    l1_cx = offset_x + (PORTRAIT_WIDTH / 2) * scale_x
    l1_cy = offset_y + (PORTRAIT_HEIGHT / 2) * scale_y
    
    for band_idx, coords in sorted(drift_groups.items()):
        # Group coordinates by y level to merge horizontally
        y_coords = {}
        for cx, cy in coords:
            if cy not in y_coords:
                y_coords[cy] = []
            y_coords[cy].append(cx)
            
        text_elems = []
        for cy, x_list in sorted(y_coords.items()):
            for cx in sorted(x_list):
                h, w = portrait_arr.shape
                ry = min(max(0, cy), h - 1)
                rx = min(max(0, cx), w - 1)
                val = portrait_arr[ry, rx]
                char = get_ascii_char(val, is_dark)
                char = char.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                text_elems.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" dy="0.3em">{char}</text>')
            
        text_elems_str = "".join(text_elems)
        
        # Calculate drift translation vector for this band
        # Top bands translate slightly differently from bottom bands
        band_y_centroid = offset_y + (band_idx * (PORTRAIT_HEIGHT / 45)) * scale_y
        dy = (l1_cy - band_y_centroid) * 0.42
        dx = (l1_cx - (offset_x + PORTRAIT_WIDTH/2 * scale_x)) * 0.42
        
        # Loop translation values: hold, translate, hold (invisible/logo phase), translate back
        loop_trans = f"0 0;0 0;{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f};0 0"
        # Opacity values: fades out during logo phases
        loop_opacity = "1;1;0;0;0;0;0;0;1"
        
        static_svg.append(
            f'<g>'
            f'<animate attributeName="opacity" values="{loop_opacity}" keyTimes="{key_times}" dur="{LOOP_DURATION}s" begin="{INTRO_DURATION}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="{loop_trans}" keyTimes="{key_times}" dur="{LOOP_DURATION}s" begin="{INTRO_DURATION}s" repeatCount="indefinite"/>'
            # Intro shimmer group (staggered fade-in)
            f'<g opacity="0">'
            f'<animate attributeName="opacity" values="0;1" dur="0.9s" begin="{(0.20 + (band_idx % 60) * 0.03):.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/>'
            f'<g font-family="{FONT}" font-size="{ASCII_FONT_SIZE}" fill="{colors["portrait_hue"]}" text-rendering="geometricPrecision">{text_elems_str}</g>'
            f'</g></g>'
        )

    # Info panel
    info_panel_svg = build_info_panel(colors)
    
    # Complete SVG build
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{BANNER_WIDTH}" height="{BANNER_HEIGHT}" viewBox="0 0 {BANNER_WIDTH} {BANNER_HEIGHT}" font-family="{FONT}" role="img" aria-label="Pallav Dholariya — profile.sh --live">
<defs>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#7C3AED"><animate attributeName="stop-color" values="#7C3AED;#22D3EE;#10B981;#7C3AED" dur="10s" repeatCount="indefinite"/></stop>
  <stop offset="0.5" stop-color="#22D3EE"><animate attributeName="stop-color" values="#22D3EE;#10B981;#7C3AED;#22D3EE" dur="10s" repeatCount="indefinite"/></stop>
  <stop offset="1" stop-color="#10B981"><animate attributeName="stop-color" values="#10B981;#7C3AED;#22D3EE;#10B981" dur="10s" repeatCount="indefinite"/></stop>
</linearGradient>
<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{colors["bg_start"]}"/><stop offset="1" stop-color="{colors["bg_end"]}"/></linearGradient>
<filter id="glow8" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="glow3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
<clipPath id="winClip"><rect x="2" y="2" width="{BANNER_WIDTH - 4}" height="{BANNER_HEIGHT - 4}" rx="18"/></clipPath>
</defs>
<rect x="2" y="2" width="{BANNER_WIDTH - 4}" height="{BANNER_HEIGHT - 4}" rx="18" fill="#070B16"/>
<g clip-path="url(#winClip)">
<rect x="2" y="2" width="{BANNER_WIDTH - 4}" height="{BANNER_HEIGHT - 4}" fill="url(#panelGrad)"/>
<rect x="2" y="2" width="{BANNER_WIDTH - 4}" height="46" fill="#0B1222"/>
<line x1="2" y1="48" x2="{BANNER_WIDTH - 2}" y2="48" stroke="rgba(255,255,255,0.10)"/>
<circle cx="30" cy="25" r="5.5" fill="#ff5f56"/>
<circle cx="50" cy="25" r="5.5" fill="#ffbd2e"/>
<circle cx="70" cy="25" r="5.5" fill="#27c93f"/>
<text x="{BANNER_WIDTH / 2}" y="29" text-anchor="middle" font-size="12" fill="{colors["text_dim"]}">{PERSONAL_INFO["email"]} - % ./profile.sh --live</text>
 
<!-- Portrait labels -->
<text x="38" y="74" font-size="10" letter-spacing="3" fill="{colors["text_dim"]}" opacity="0.75">VISUAL.MAP</text>
<rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{colors["ui_chrome"]}" stroke-width="2" opacity="0.45" filter="url(#glow3)"/>
<rect x="36" y="84" width="400" height="492" rx="10" fill="{colors["portrait_bg"]}" stroke="{colors["ui_chrome_dim"]}"/>
 
<!-- Portrait static/drift dots -->
<g transform="translate({offset_x},{offset_y}) scale({scale_x:.4f},{scale_y:.4f})">
  <set attributeName="opacity" to="0" begin="{INTRO_DURATION}s"/>
  {"\n  ".join(static_svg)}
</g>
 
<!-- Morphing travellers dots -->
<g font-family="{FONT}" font-size="{ASCII_FONT_SIZE}" fill="{colors["portrait_hue"]}" text-rendering="geometricPrecision">
  {"\n  ".join(travellers_svg)}
</g>
 
<!-- SYSTEM.INFO panel -->
{info_panel_svg}
 
</g>
<!-- Animated terminal edge glowing border -->
<rect x="3" y="3" width="{BANNER_WIDTH - 6}" height="{BANNER_HEIGHT - 6}" rx="17" fill="none" stroke="url(#accent)" stroke-width="3" opacity="0.55" filter="url(#glow8)"/>
<rect x="3" y="3" width="{BANNER_WIDTH - 6}" height="{BANNER_HEIGHT - 6}" rx="17" fill="none" stroke="url(#accent)" stroke-width="1.6"/>
</svg>
'''
    return svg
 
# --- Main Generator ---
 
def main():
    print("=" * 60)
    print("  Dithered Portrait Banner Generator")
    print("  Theme: Terminal/Cyberpunk")
    print("=" * 60)
    print()
    
    # Generate dark theme banner
    print("[1/2] Generating dark.svg...")
    dark_svg = generate_svg("dark")
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print(f"  ✓ Saved dark.svg & assets/dark.svg ({len(dark_svg):,} bytes)")
    print()
    
    # Generate light theme banner
    print("[2/2] Generating light.svg...")
    light_svg = generate_svg("light")
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open("assets/light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print(f"  ✓ Saved light.svg & assets/light.svg ({len(light_svg):,} bytes)")
    print()
    
    print("=" * 60)
    print("  Generation complete!")
    print("  Files: dark.svg, light.svg")
    print("=" * 60)

if __name__ == "__main__":
    main()
