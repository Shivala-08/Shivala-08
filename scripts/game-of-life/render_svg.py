import os
from conway import load_seed, generate_frames

CELL_SIZE = 12
GAP = 3
FRAME_DURATION = 0.4  # seconds per generation

def render(frames, out_path="dist/game-of-life.svg"):
    # Ensure directory exists
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    rows = len(frames[0])     # 53 (weeks)
    cols = len(frames[0][0])  # 7 (days)
    
    # We transpose visually to render horizontally:
    # Weeks (rows of the python grid, 0..52) will be columns (horizontal)
    # Days (cols of the python grid, 0..6) will be rows (vertical)
    width = rows * (CELL_SIZE + GAP)
    height = cols * (CELL_SIZE + GAP)
    total_duration = len(frames) * FRAME_DURATION

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
    ]

    for x in range(rows):
        for y in range(cols):
            cell_id = f"c{x}_{y}"
            
            # Alive = #00E5FF (arc-reactor cyan) — Phase 1 palette
            # Dead  = #05060A (deep space background)
            color_values = [
                "#00E5FF" if frames[t][x][y] else "#05060A"
                for t in range(len(frames))
            ]
            # Match the final keyTime (1.0)
            color_values.append(color_values[-1])
            values = ";".join(color_values)
            
            key_times = [str(round(t / len(frames), 3)) for t in range(len(frames))]
            key_times.append("1")
            keyTimes_str = ";".join(key_times)

            # Horizontal coordinate is x (week), vertical coordinate is y (day)
            svg_parts.append(
                f'<rect id="{cell_id}" x="{x*(CELL_SIZE+GAP)}" y="{y*(CELL_SIZE+GAP)}" '
                f'width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="#05060A">'
                f'<animate attributeName="fill" values="{values}" '
                f'dur="{total_duration}s" repeatCount="indefinite" '
                f'keyTimes="{keyTimes_str}" />'
                f'</rect>'
            )

    svg_parts.append("</svg>")
    with open(out_path, "w") as f:
        f.write("".join(svg_parts))

if __name__ == "__main__":
    seed = load_seed()
    frames = generate_frames(seed, generations=20)
    render(frames)
