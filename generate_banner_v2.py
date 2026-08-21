#!/usr/bin/env python3
"""
Dithered Portrait Banner Generator v2
Phase 1 — Terminal Aesthetic

Generates dark.svg and light.svg with:
- 1-bit Floyd-Steinberg dithered portrait (serpentine order)
- Background segmentation for dark mode
- Intro shimmer animation (~3.2s)
- Loop animation with drift bands (~14.2s)
- Info panel with dotted leaders and LIVE badge

Theme: Terminal/Cyberpunk
Palette: Portrait [#A78BFA dark / #7C3AED light] · UI chrome [#22D3EE / #0891B2] · accent [#10B981] · background [#0A101F]
"""

import os
import sys
import base64
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy import ndimage

# ─── Configuration ───────────────────────────────────────────────────────────

BANNER_WIDTH = 1180
BANNER_HEIGHT = 610

# Portrait processing
PORTRAIT_WIDTH = 300
PORTRAIT_HEIGHT = 340
DOT_SIZE = 3  # pixels per dot

# Animation timing
INTRO_DURATION = 3.2  # seconds
LOOP_DURATION = 14.2  # seconds

# Cyberpunk color palette
COLORS = {
    "dark": {
        "bg": "#0A101F",
        "bg_gradient_start": "#0A101F",
        "bg_gradient_end": "#0F172A",
        "portrait_hue": "#A78BFA",  # Purple for dots
        "portrait_bg": "#1E1B4B",  # Dark background for portrait frame
        "ui_chrome": "#22D3EE",    # Cyan for UI elements
        "accent": "#10B981",       # Green for accents
        "live_badge": "#EF4444",   # Red for LIVE badge
        "text": "#F8FAFC",
        "text_dim": "#94A3B8",
        "dot_empty": "#2d3343",    # Visible slate for empty cells
        "border": "#334155",
        "terminal_bg": "rgba(15,23,42,0.95)",
    },
    "light": {
        "bg": "#F8FAFC",
        "bg_gradient_start": "#F1F5F9",
        "bg_gradient_end": "#E2E8F0",
        "portrait_hue": "#7C3AED",  # Deeper purple for light mode dots
        "portrait_bg": "#DDD6FE",  # Light purple background
        "ui_chrome": "#0891B2",    # Darker cyan for light mode
        "accent": "#059669",       # Darker green
        "live_badge": "#DC2626",   # Darker red
        "text": "#1E293B",
        "text_dim": "#64748B",
        "dot_empty": "#CBD5E1",    # Light slate for empty cells
        "border": "#CBD5E1",
        "terminal_bg": "rgba(248,250,252,0.95)",
    }
}

# Asset paths
PORTRAIT_DIR = Path("image/myimage")
LOGOS_DIR = Path("image/logos")

# Selected logos for morph animation
SELECTED_LOGOS = ["python.jpeg", "html.jpeg", "csslogo.png", "bashlogo.jpeg", "n8n logo.png"]

# Personal info
PERSONAL_INFO = {
    "name": "Pallav Dholariya",
    "username": "Shivala-08",
    "role": "AI/ML Engineer • Full Stack Developer",
    "origin": "Pune, India",
    "education": "B.Tech CSE (AI & ML)",
    "status": "Building · Learning · Shipping",
    "toolchain": "VS Code, Git, Docker",
    "languages": "Python, JavaScript, TypeScript",
    "frontend": "React, Next.js, Tailwind CSS",
    "backend": "FastAPI, Node.js",
    "database": "PostgreSQL, Supabase",
    "infra": "Docker, GitHub Actions, Vercel",
    "email": "pallavdholariya@gmail.com",
    "portfolio": "pallav-os.vercel.app",
    "linkedin": "linkedin.com/in/pallavdholariya",
    "github": "github.com/Shivala-08",
    "facebook": "—",
}


# ─── Image Processing ────────────────────────────────────────────────────────

def find_best_portrait():
    """Find the best portrait image from the myimage directory."""
    images = list(PORTRAIT_DIR.glob("*.png")) + list(PORTRAIT_DIR.glob("*.jpg")) + list(PORTRAIT_DIR.glob("*.jpeg"))
    if not images:
        raise FileNotFoundError("No portrait image found in image/myimage/")
    best = max(images, key=lambda p: p.stat().st_size)
    print(f"Selected portrait: {best.name}")
    return best


def process_portrait(path, target_width=PORTRAIT_WIDTH, target_height=PORTRAIT_HEIGHT):
    """Process portrait: crop to head/shoulders, resize, preserve identity."""
    img = Image.open(path).convert("L")  # Convert to grayscale
    
    # Center crop to focus on head/shoulders
    w, h = img.size
    target_ratio = target_width / target_height
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int(h * 0.05)  # Slight shift up for head
        img = img.crop((0, top, w, top + new_h))
    
    # Resize to target
    img = img.resize((target_width, target_height), Image.LANCZOS)
    
    # Apply contrast enhancement (1.3x)
    img = ImageOps.autocontrast(img, cutoff=1)
    
    # Apply UnsharpMask
    img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    
    return img


def floyd_steinberg_dither(img_array, num_levels=2):
    """Apply Floyd-Steinberg dithering with serpentine order."""
    h, w = img_array.shape
    dithered = np.zeros((h, w), dtype=np.uint8)
    
    # Quantization step
    step = 255 / (num_levels - 1)
    
    for y in range(h):
        # Serpentine order: alternate direction each row
        if y % 2 == 0:
            x_range = range(w)
        else:
            x_range = range(w - 1, -1, -1)
        
        for x in x_range:
            old_pixel = img_array[y, x]
            new_pixel = round(old_pixel / step) * step
            new_pixel = max(0, min(255, new_pixel))
            
            dithered[y, x] = int(new_pixel)
            error = old_pixel - new_pixel
            
            # Distribute error
            if y % 2 == 0:  # Left to right
                if x + 1 < w:
                    img_array[y, x + 1] += error * 7 / 16
                if y + 1 < h:
                    if x - 1 >= 0:
                        img_array[y + 1, x - 1] += error * 3 / 16
                    img_array[y + 1, x] += error * 5 / 16
                    if x + 1 < w:
                        img_array[y + 1, x + 1] += error * 1 / 16
            else:  # Right to left
                if x - 1 >= 0:
                    img_array[y, x - 1] += error * 7 / 16
                if y + 1 < h:
                    if x - 1 >= 0:
                        img_array[y + 1, x - 1] += error * 1 / 16
                    img_array[y + 1, x] += error * 5 / 16
                    if x + 1 < w:
                        img_array[y + 1, x + 1] += error * 3 / 16
    
    return dithered


def segment_background(img_array, threshold=50):
    """Segment foreground (subject) from background."""
    # Apply Gaussian blur
    blurred = ndimage.gaussian_filter(img_array.astype(float), sigma=5)
    
    # Create binary mask using Otsu-like threshold
    mask = img_array < threshold
    
    # Clean up mask
    mask = ndimage.binary_closing(mask, iterations=3)
    mask = ndimage.binary_fill_holes(mask)
    
    # Keep largest component (the subject)
    labeled, num_features = ndimage.label(mask)
    if num_features > 0:
        sizes = ndimage.sum(mask, labeled, range(1, num_features + 1))
        largest = np.argmax(sizes) + 1
        mask = labeled == largest
    
    return mask


def generate_dots_from_dithered(dithered, mask, theme_colors, is_dark=True):
    """Generate SVG dot paths for colored foreground only."""
    h, w = dithered.shape
    dots = []
    
    hue_color = theme_colors["portrait_hue"]
    
    for y in range(0, h, DOT_SIZE):
        for x in range(0, w, DOT_SIZE):
            # Check if this dot represents subject details (lit / dark in dithered)
            is_lit = (dithered[y, x] == 0)
            
            # In dark mode, we only color the dot if it is foreground (subject) and lit.
            # In light mode, we color the dot if it is lit.
            if is_dark:
                is_colored = is_lit and mask[y, x]
            else:
                is_colored = is_lit
            
            if is_colored:
                # Foreground dot
                color = hue_color
                dots.append({
                    "x": x,
                    "y": y,
                    "color": color,
                    "opacity": 1.0
                })
    return dots


def optimize_dots_to_svg_path(dots):
    """Convert dots to SVG path elements with horizontal RLE merging for maximum compression."""
    paths = []
    
    # Group dots by (color, opacity)
    grouped = {}
    for dot in dots:
        key = (dot["color"], dot["opacity"])
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(dot)
        
    for (color, opacity), color_dots in grouped.items():
        # Group by y coordinate
        y_groups = {}
        for dot in color_dots:
            y = dot["y"]
            if y not in y_groups:
                y_groups[y] = []
            y_groups[y].append(dot["x"])
            
        d_segments = []
        # Process each y level
        for y, x_coords in sorted(y_groups.items()):
            x_coords = sorted(x_coords)
            if not x_coords:
                continue
                
            # Merge adjacent x coordinates
            start_x = x_coords[0]
            current_x = x_coords[0]
            
            for x in x_coords[1:]:
                if x == current_x + DOT_SIZE:
                    # Adjacent, extend interval
                    current_x = x
                else:
                    # Gap, output current interval
                    width = (current_x - start_x) + DOT_SIZE
                    d_segments.append(f"M{start_x},{y}h{width}v{DOT_SIZE}h-{width}z")
                    # Start new interval
                    start_x = x
                    current_x = x
                    
            # Output the last interval
            width = (current_x - start_x) + DOT_SIZE
            d_segments.append(f"M{start_x},{y}h{width}v{DOT_SIZE}h-{width}z")
            
        if d_segments:
            paths.append({
                "color": color,
                "opacity": opacity,
                "d": " ".join(d_segments)
            })
            
    return paths


# ─── Logo Processing ─────────────────────────────────────────────────────────

def make_white_transparent(img, threshold=240):
    """Make white/near-white pixels in RGBA image transparent."""
    datas = img.getdata()
    newData = []
    for item in datas:
        # If r, g, b are all above threshold, set alpha to 0
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img


def process_logo(path, target_size=40):
    """Process a logo: resize, center, make white background transparent."""
    img = Image.open(path).convert("RGBA")
    img = make_white_transparent(img)
    
    # Resize maintaining aspect ratio
    w, h = img.size
    ratio = min(target_size / w, target_size / h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Create square canvas and center
    canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    offset_x = (target_size - new_w) // 2
    offset_y = (target_size - new_h) // 2
    canvas.paste(img, (offset_x, offset_y), mask=img)
    
    return canvas


def image_to_base64(img):
    """Convert PIL Image to base64 data URI."""
    import io
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


# ─── SVG Generation ──────────────────────────────────────────────────────────

def generate_info_panel_svg(x, y, colors, info):
    """Generate the info panel with dotted leaders."""
    rows = [
        ("Subject", info["name"]),
        ("Role", info["role"]),
        ("Origin", info["origin"]),
        ("Education", info["education"]),
        ("Status", info["status"]),
        ("ToolChain", info["toolchain"]),
        ("", ""),  # Spacer
        ("Core.Lang", info["languages"]),
        ("Core.Frontend", info["frontend"]),
        ("Core.Backend", info["backend"]),
        ("Core.Database", info["database"]),
        ("Core.Infra", info["infra"]),
        ("", ""),  # Spacer
        ("Grid.Mail", info["email"]),
        ("Grid.Portfolio", info["portfolio"]),
        ("Grid.LinkedIn", info["linkedin"]),
        ("Grid.GitHub", info["github"]),
    ]
    
    svg_lines = []
    y_offset = y
    spacing = 20
    font_size = 14
    header_size = 13
    pill_size = 14
    
    # Header
    svg_lines.append(f'<text x="{x}" y="{y_offset}" font-family="\'SF Mono\', \'Fira Code\', monospace" font-size="{header_size}" fill="{colors["ui_chrome"]}" letter-spacing="2">SYSTEM.INFO</text>')
    y_offset += 20
    
    # LIVE badge
    svg_lines.append(f'<rect x="{x}" y="{y_offset - 12}" width="40" height="16" rx="3" fill="{colors["live_badge"]}"/>')
    svg_lines.append(f'<text x="{x + 20}" y="{y_offset}" font-family="\'SF Mono\', monospace" font-size="10" fill="white" text-anchor="middle">LIVE</text>')
    y_offset += 20
    
    # Handle pill
    svg_lines.append(f'<rect x="{x}" y="{y_offset - 12}" width="180" height="18" rx="4" fill="{colors["ui_chrome"]}" opacity="0.2"/>')
    svg_lines.append(f'<text x="{x + 10}" y="{y_offset}" font-family="\'SF Mono\', monospace" font-size="{pill_size}" fill="{colors["ui_chrome"]}">@{info["username"]}</text>')
    y_offset += 25
    
    # Info rows
    for label, value in rows:
        if not label:
            y_offset += 8
            continue
        
        # Calculate dotted leaders
        label_len = len(label)
        value_len = len(value)
        dots_needed = max(2, 30 - label_len - value_len)
        dots = "·" * dots_needed
        
        value_esc = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        svg_lines.append(f'<text x="{x}" y="{y_offset}" font-family="\'SF Mono\', monospace" font-size="{font_size}">')
        svg_lines.append(f'  <tspan fill="{colors["text_dim"]}">{label}</tspan>')
        svg_lines.append(f'  <tspan fill="{colors["text_dim"]}" opacity="0.5"> {dots} </tspan>')
        svg_lines.append(f'  <tspan fill="{colors["text"]}">{value_esc}</tspan>')
        svg_lines.append(f'</text>')
        y_offset += spacing
    
    return "\n".join(svg_lines)


def process_and_dither_logo(path, target_width=PORTRAIT_WIDTH, target_height=PORTRAIT_HEIGHT):
    """Process a logo to full portrait size and dither it."""
    img = Image.open(path).convert("L")
    
    # Resize to fit inside target size with some padding (say 180 max size)
    max_size = 180
    w, h = img.size
    ratio = min(max_size / w, max_size / h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Place on 300x340 white background (since white is 255)
    bg = Image.new("L", (target_width, target_height), 255)
    offset_x = (target_width - new_w) // 2
    offset_y = (target_height - new_h) // 2
    bg.paste(img, (offset_x, offset_y))
    
    # Dither it
    bg_array = np.array(bg).copy().astype(float)
    dithered = floyd_steinberg_dither(bg_array)
    return dithered


def generate_svg(theme="dark"):
    """Generate the complete dithered portrait banner SVG."""
    colors = COLORS[theme]
    is_dark = theme == "dark"
    
    # 1. Process portrait
    portrait_path = find_best_portrait()
    portrait_gray = process_portrait(portrait_path)
    portrait_array = np.array(portrait_gray)
    dithered_array = portrait_array.copy().astype(float)
    dithered_portrait = floyd_steinberg_dither(dithered_array)
    mask = segment_background(portrait_array)
    
    # Generate dots for portrait (colored/foreground only)
    portrait_dots = generate_dots_from_dithered(dithered_portrait, mask, colors, is_dark)
    portrait_paths = optimize_dots_to_svg_path(portrait_dots)
    
    portrait_svg_elements = []
    for path_data in portrait_paths:
        opacity_attr = f' opacity="{path_data["opacity"]}"' if path_data.get("opacity", 1.0) != 1.0 else ''
        portrait_svg_elements.append(f'<path d="{path_data["d"]}" fill="{path_data["color"]}"{opacity_attr} shape-rendering="crispEdges"/>')
    portrait_dot_paths_svg = "\n      ".join(portrait_svg_elements)
    
    # Generate static background grid (once, RLE-compressed)
    bg_dots = []
    empty_color = colors["dot_empty"]
    for y in range(0, PORTRAIT_HEIGHT, DOT_SIZE):
        for x in range(0, PORTRAIT_WIDTH, DOT_SIZE):
            bg_dots.append({
                "x": x,
                "y": y,
                "color": empty_color,
                "opacity": 0.3
            })
    bg_paths = optimize_dots_to_svg_path(bg_dots)
    bg_svg_elements = []
    for path_data in bg_paths:
        opacity_attr = f' opacity="{path_data["opacity"]}"' if path_data.get("opacity", 1.0) != 1.0 else ''
        bg_svg_elements.append(f'<path d="{path_data["d"]}" fill="{path_data["color"]}"{opacity_attr} shape-rendering="crispEdges"/>')
    bg_grid_svg = "\n      ".join(bg_svg_elements)
    
    # 2. Process each logo to target size 300x340 and dither
    slides = []
    
    # Slide 0 is the portrait
    slides.append({
        "svg": portrait_dot_paths_svg,
        "opacity": "1",
        "animate_opacity": "1;1;0;0;1",
        "animate_transform": "0,0;0,0;-300,0;300,0;0,0",
        "key_times": "0.0;0.125;0.167;0.958;1.0"
    })
    
    # Slide animations timing (dur = 24s)
    logo_timings = [
        {"animate_opacity": "0;0;1;1;0;0", "animate_transform": "-300,0;300,0;0,0;0,0;-300,0;-300,0", "key_times": "0.0;0.125;0.167;0.292;0.333;1.0"}, # Python
        {"animate_opacity": "0;0;1;1;0;0", "animate_transform": "-300,0;300,0;0,0;0,0;-300,0;-300,0", "key_times": "0.0;0.292;0.333;0.458;0.500;1.0"}, # HTML
        {"animate_opacity": "0;0;1;1;0;0", "animate_transform": "-300,0;300,0;0,0;0,0;-300,0;-300,0", "key_times": "0.0;0.458;0.500;0.625;0.667;1.0"}, # CSS
        {"animate_opacity": "0;0;1;1;0;0", "animate_transform": "-300,0;300,0;0,0;0,0;-300,0;-300,0", "key_times": "0.0;0.625;0.667;0.792;0.833;1.0"}, # Bash
        {"animate_opacity": "0;0;1;1;0", "animate_transform": "-300,0;300,0;0,0;0,0;-300,0", "key_times": "0.0;0.792;0.833;0.958;1.0"}          # n8n
    ]
    
    for idx, logo_name in enumerate(SELECTED_LOGOS):
        logo_path = LOGOS_DIR / logo_name
        if logo_path.exists():
            # Process to 300x340 and dither
            logo_dithered = process_and_dither_logo(logo_path)
            
            # Generate dots: colored foreground only
            dummy_mask = np.ones_like(logo_dithered, dtype=bool)
            logo_dots = generate_dots_from_dithered(logo_dithered, dummy_mask, colors, is_dark=True)
            logo_paths = optimize_dots_to_svg_path(logo_dots)
            
            logo_svg_elements = []
            for path_data in logo_paths:
                opacity_attr = f' opacity="{path_data["opacity"]}"' if path_data.get("opacity", 1.0) != 1.0 else ''
                logo_svg_elements.append(f'<path d="{path_data["d"]}" fill="{path_data["color"]}"{opacity_attr} shape-rendering="crispEdges"/>')
            logo_dot_paths_svg = "\n      ".join(logo_svg_elements)
            
            timing = logo_timings[idx] if idx < len(logo_timings) else logo_timings[-1]
            slides.append({
                "svg": logo_dot_paths_svg,
                "opacity": "0",
                "animate_opacity": timing["animate_opacity"],
                "animate_transform": timing["animate_transform"],
                "key_times": timing["key_times"]
            })
            print(f"Processed logo slide: {logo_name}")
            
    # Combine slides SVG
    slides_svg_elements = []
    for idx, slide in enumerate(slides):
        slides_svg_elements.append(f'''    <g class="slide-{idx}" opacity="{slide['opacity']}">
      <animate attributeName="opacity" values="{slide['animate_opacity']}" dur="24s" repeatCount="indefinite" keyTimes="{slide['key_times']}"/>
      <animateTransform attributeName="transform" type="translate" values="{slide['animate_transform']}" dur="24s" repeatCount="indefinite" keyTimes="{slide['key_times']}"/>
      {slide['svg']}
    </g>''')
    
    slides_svg = "\n".join(slides_svg_elements)
    
    # Generate info panel
    info_panel = generate_info_panel_svg(420, 60, colors, PERSONAL_INFO)
    
    # SVG template
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{BANNER_WIDTH}" height="{BANNER_HEIGHT}" viewBox="0 0 {BANNER_WIDTH} {BANNER_HEIGHT}">
  <defs>
    <!-- Gradient Background -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['bg_gradient_start']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors['bg_gradient_end']};stop-opacity:1" />
    </linearGradient>
    
    <!-- Portrait clip path -->
    <clipPath id="portraitClip">
      <rect x="40" y="60" width="{PORTRAIT_WIDTH}" height="{PORTRAIT_HEIGHT}" rx="8"/>
    </clipPath>
    
    <!-- Glow filter -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="{BANNER_WIDTH}" height="{BANNER_HEIGHT}" fill="url(#bgGrad)"/>
  
  <!-- Border frame -->
  <rect x="10" y="10" width="{BANNER_WIDTH - 20}" height="{BANNER_HEIGHT - 20}" 
        fill="none" stroke="{colors['ui_chrome']}" stroke-width="1" opacity="0.3" rx="4"/>
  
  <!-- Portrait frame -->
  <rect x="20" y="40" width="{PORTRAIT_WIDTH + 40}" height="{PORTRAIT_HEIGHT + 40}" 
        fill="{colors['portrait_bg']}" stroke="{colors['ui_chrome']}" stroke-width="2" rx="8"/>
  
  <!-- Frame label -->
  <text x="{(PORTRAIT_WIDTH + 80) // 2}" y="30" 
        font-family="'SF Mono', 'Fira Code', monospace" font-size="11" 
        fill="{colors['ui_chrome']}" text-anchor="middle" letter-spacing="3">
    VISUAL.MAP
  </text>
  
  <!-- Dithered portrait dots (Slideshow) -->
  <g clip-path="url(#portraitClip)">
    <g id="portraitDots" opacity="0" transform="translate(40, 60)">
      {bg_grid_svg}
      {slides_svg}
      <!-- Intro animation -->
      <animate attributeName="opacity" 
               values="0;1" 
               dur="{INTRO_DURATION}s" 
               begin="0s"
               fill="freeze"/>
    </g>
  </g>
  
  <!-- Portrait frame accent lines -->
  <line x1="20" y1="40" x2="60" y2="40" stroke="{colors['accent']}" stroke-width="2"/>
  <line x1="20" y1="40" x2="20" y2="80" stroke="{colors['accent']}" stroke-width="2"/>
  <line x1="{BANNER_WIDTH - 60}" y1="{BANNER_HEIGHT - 40}" x2="{BANNER_WIDTH - 20}" y2="{BANNER_HEIGHT - 40}" stroke="{colors['accent']}" stroke-width="2"/>
  <line x1="{BANNER_WIDTH - 20}" y1="{BANNER_HEIGHT - 80}" x2="{BANNER_WIDTH - 20}" y2="{BANNER_HEIGHT - 40}" stroke="{colors['accent']}" stroke-width="2"/>
  
  <!-- Info panel -->
  <g transform="translate(0, 0)">
    {info_panel}
  </g>
  
  <!-- Bottom status bar -->
  <rect x="20" y="{BANNER_HEIGHT - 50}" width="{BANNER_WIDTH - 40}" height="30" rx="4"
        fill="{colors['terminal_bg']}" stroke="{colors['border']}" stroke-width="1"/>
  
  <text x="40" y="{BANNER_HEIGHT - 30}" font-family="'SF Mono', monospace" font-size="11" fill="{colors['text_dim']}">
    <tspan fill="{colors['accent']}">❯</tspan>
    <tspan fill="{colors['text']}"> {PERSONAL_INFO['status']}</tspan>
  </text>
  
  <text x="{BANNER_WIDTH - 40}" y="{BANNER_HEIGHT - 30}" 
        font-family="'SF Mono', monospace" font-size="11" fill="{colors['text_dim']}" text-anchor="end">
    <tspan fill="{colors['ui_chrome']}">⌘</tspan> @{PERSONAL_INFO['username']}
  </text>
  
</svg>'''
    
    return svg


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Dithered Portrait Banner Generator v2")
    print("  Theme: Terminal/Cyberpunk")
    print("=" * 60)
    print()
    
    # Generate dark theme
    print("[1/2] Generating dark.svg...")
    dark_svg = generate_svg("dark")
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print(f"  ✓ Saved dark.svg ({len(dark_svg):,} bytes)")
    print()
    
    # Generate light theme
    print("[2/2] Generating light.svg...")
    light_svg = generate_svg("light")
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print(f"  ✓ Saved light.svg ({len(light_svg):,} bytes)")
    print()
    
    print("=" * 60)
    print("  Generation complete!")
    print("  Files: dark.svg, light.svg")
    print("=" * 60)


if __name__ == "__main__":
    main()
