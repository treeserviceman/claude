"""Generates 50 original flat-vector illustration cards (SVG) used across the
site in place of photographic stock/AI images (no image-generation tool was
available in this environment). Each is procedurally built, grouped by theme
so it stays visually relevant to the service it illustrates."""

import os, math

PALETTES = [
    ("#0f3d2e", "#1c6b4f", "#e8f5ee"),
    ("#0b3554", "#1a6fa3", "#e7f3fa"),
    ("#3d2b0f", "#a3651a", "#faf1e3"),
    ("#2b0f3d", "#6b2c91", "#f3e8fa"),
    ("#3d0f16", "#a31a2e", "#faeef0"),
    ("#0f2b3d", "#1a5c91", "#e8f1fa"),
    ("#233d0f", "#5c8a1a", "#f0f7e8"),
    ("#3d2f0f", "#8a6a1a", "#f7f2e8"),
]

def pal(i):
    return PALETTES[i % len(PALETTES)]

def _canvas_open(dark, mid, light, seed):
    blob1_x = 120 + (seed * 37) % 500
    blob1_y = 80 + (seed * 53) % 350
    blob2_x = 600 - (seed * 29) % 400
    blob2_y = 420 - (seed * 41) % 300
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img">
<defs>
<linearGradient id="bg{seed}" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{dark}"/><stop offset="1" stop-color="{mid}"/>
</linearGradient>
</defs>
<rect width="800" height="600" fill="url(#bg{seed})"/>
<circle cx="{blob1_x}" cy="{blob1_y}" r="140" fill="{light}" opacity="0.08"/>
<circle cx="{blob2_x}" cy="{blob2_y}" r="180" fill="{light}" opacity="0.06"/>
"""

def _canvas_close():
    return "</svg>"

def raccoon_icon(light, mid):
    return f"""
<g transform="translate(400,300)">
<ellipse cx="0" cy="40" rx="150" ry="120" fill="{light}"/>
<circle cx="-70" cy="-90" r="55" fill="{light}"/>
<circle cx="70" cy="-90" r="55" fill="{light}"/>
<circle cx="-70" cy="-90" r="28" fill="{mid}"/>
<circle cx="70" cy="-90" r="28" fill="{mid}"/>
<ellipse cx="0" cy="-30" rx="95" ry="80" fill="{light}"/>
<path d="M -95 -55 Q 0 -110 95 -55 Q 60 -30 0 -20 Q -60 -30 -95 -55 Z" fill="{mid}"/>
<circle cx="-32" cy="-40" r="14" fill="#1a1a1a"/>
<circle cx="32" cy="-40" r="14" fill="#1a1a1a"/>
<ellipse cx="0" cy="-8" rx="16" ry="11" fill="#1a1a1a"/>
<path d="M 150 60 Q 230 30 220 -40 Q 210 -100 150 -80" fill="none" stroke="{light}" stroke-width="42" stroke-linecap="round"/>
<path d="M 175 50 L 195 50 M 178 5 L 198 5 M 180 -35 L 200 -35" stroke="{mid}" stroke-width="14"/>
</g>"""

def skunk_icon(light, mid):
    return f"""
<g transform="translate(400,320)">
<ellipse cx="-20" cy="20" rx="150" ry="90" fill="#1a1a1a"/>
<path d="M -150 30 Q -60 -70 60 30 Q -30 60 -150 30 Z" fill="{light}"/>
<ellipse cx="120" cy="-20" rx="60" ry="55" fill="#1a1a1a"/>
<path d="M 85 -55 Q 120 -110 165 -60" fill="none" stroke="{light}" stroke-width="16" stroke-linecap="round"/>
<circle cx="108" cy="-25" r="26" fill="{mid}"/>
<circle cx="100" cy="-30" r="7" fill="#1a1a1a"/>
<ellipse cx="150" cy="-5" rx="10" ry="7" fill="#2a2a2a"/>
<path d="M -180 60 Q -260 30 -250 -60 Q -240 -140 -160 -120 Q -190 -60 -170 10 Q -160 45 -180 60 Z" fill="{light}"/>
</g>"""

def mosquito_icon(light, mid):
    legs = "".join(
        f'<line x1="0" y1="0" x2="{60*math.cos(a)}" y2="{60*math.sin(a)}" stroke="{light}" stroke-width="6" stroke-linecap="round" transform="translate({dx},{dy}) rotate({deg})"/>'
        for dx, dy, deg, a in [(-10,10,20,2.6),(-10,20,45,2.6),(-10,30,70,2.6),(10,10,-20,-2.6+math.pi),(10,20,-45,-2.6+math.pi),(10,30,-70,-2.6+math.pi)]
    )
    return f"""
<g transform="translate(400,300)">
<ellipse cx="0" cy="0" rx="26" ry="70" fill="{mid}" transform="rotate(15)"/>
<circle cx="0" cy="-70" r="22" fill="{mid}"/>
<path d="M 0 -90 L 90 -140" stroke="{mid}" stroke-width="7" stroke-linecap="round"/>
<ellipse cx="55" cy="-30" rx="110" ry="46" fill="{light}" opacity="0.85" transform="rotate(-18 55 -30)"/>
<ellipse cx="-55" cy="-30" rx="110" ry="46" fill="{light}" opacity="0.6" transform="rotate(18 -55 -30)"/>
{legs}
</g>"""

def rat_icon(light, mid):
    return f"""
<g transform="translate(400,320)">
<path d="M -160 40 Q -60 -120 140 -20 Q 220 20 180 90 Q 60 130 -160 40 Z" fill="{light}"/>
<circle cx="140" cy="-30" r="60" fill="{light}"/>
<circle cx="100" cy="-75" r="22" fill="{mid}"/>
<circle cx="165" cy="-70" r="20" fill="{mid}"/>
<circle cx="160" cy="-25" r="9" fill="#1a1a1a"/>
<ellipse cx="195" cy="-5" rx="12" ry="8" fill="#2a2a2a"/>
<path d="M 195 5 Q 230 15 220 30 Q 205 20 190 15" fill="{mid}"/>
<path d="M -160 40 Q -260 60 -320 20 Q -280 5 -220 15 Q -270 -20 -300 -60 Q -230 -40 -190 0" fill="none" stroke="{mid}" stroke-width="10" stroke-linecap="round"/>
</g>"""

def roach_icon(light, mid):
    stripes = "".join(
        f'<ellipse cx="0" cy="{y}" rx="70" ry="18" fill="{mid}" opacity="0.5"/>' for y in (-50,-20,10,40)
    )
    return f"""
<g transform="translate(400,300)">
<ellipse cx="0" cy="0" rx="90" ry="150" fill="{light}"/>
{stripes}
<ellipse cx="0" cy="-140" rx="45" ry="38" fill="{light}"/>
<path d="M -20 -170 L -70 -230 M 20 -170 L 70 -230" stroke="{mid}" stroke-width="6" stroke-linecap="round"/>
<path d="M -90 -60 L -170 -90 M -90 0 L -180 0 M -90 60 L -170 90" stroke="{mid}" stroke-width="10" stroke-linecap="round"/>
<path d="M 90 -60 L 170 -90 M 90 0 L 180 0 M 90 60 L 170 90" stroke="{mid}" stroke-width="10" stroke-linecap="round"/>
</g>"""

def bedbug_icon(light, mid):
    return f"""
<g transform="translate(400,300)">
<ellipse cx="0" cy="10" rx="120" ry="140" fill="{light}"/>
<ellipse cx="0" cy="-30" rx="95" ry="60" fill="{mid}" opacity="0.55"/>
<circle cx="0" cy="-130" r="34" fill="{light}"/>
<path d="M -14 -158 L -34 -190 M 14 -158 L 34 -190" stroke="{mid}" stroke-width="6" stroke-linecap="round"/>
<path d="M -110 -70 L -170 -95 M -120 0 L -190 0 M -110 70 L -170 95" stroke="{mid}" stroke-width="9" stroke-linecap="round"/>
<path d="M 110 -70 L 170 -95 M 120 0 L 190 0 M 110 70 L 170 95" stroke="{mid}" stroke-width="9" stroke-linecap="round"/>
</g>"""

def van_icon(light, mid):
    return f"""
<g transform="translate(400,340)">
<rect x="-220" y="-60" width="440" height="120" rx="18" fill="{light}"/>
<rect x="-220" y="-130" width="230" height="80" rx="14" fill="{light}"/>
<rect x="-190" y="-105" width="80" height="50" rx="6" fill="{mid}" opacity="0.6"/>
<circle cx="-130" cy="70" r="45" fill="#1a1a1a"/>
<circle cx="130" cy="70" r="45" fill="#1a1a1a"/>
<circle cx="-130" cy="70" r="18" fill="{light}"/>
<circle cx="130" cy="70" r="18" fill="{light}"/>
<rect x="-150" y="-25" width="300" height="14" fill="{mid}" opacity="0.7"/>
</g>"""

def shield_icon(light, mid):
    return f"""
<g transform="translate(400,300)">
<path d="M 0 -180 L 150 -120 Q 150 60 0 180 Q -150 60 -150 -120 Z" fill="{light}"/>
<path d="M -60 0 L -15 55 L 80 -60" fill="none" stroke="{mid}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>
</g>"""

def house_icon(light, mid):
    return f"""
<g transform="translate(400,320)">
<rect x="-160" y="-20" width="320" height="200" fill="{light}"/>
<path d="M -200 -20 L 0 -170 L 200 -20 Z" fill="{mid}"/>
<rect x="-40" y="60" width="80" height="120" fill="{mid}" opacity="0.7"/>
<rect x="-120" y="10" width="60" height="60" fill="#ffffff" opacity="0.35"/>
<rect x="60" y="10" width="60" height="60" fill="#ffffff" opacity="0.35"/>
</g>"""

def tech_icon(light, mid):
    return f"""
<g transform="translate(400,320)">
<circle cx="0" cy="-110" r="55" fill="{light}"/>
<path d="M -90 130 Q -90 -10 0 -10 Q 90 -10 90 130 Z" fill="{light}"/>
<rect x="-30" y="30" width="60" height="90" rx="10" fill="{mid}"/>
<rect x="-16" y="45" width="32" height="14" fill="#ffffff" opacity="0.6"/>
</g>"""

THEME_ICONS = {
    "raccoon": raccoon_icon, "skunk": skunk_icon, "mosquito": mosquito_icon,
    "rat": rat_icon, "roach": roach_icon, "bedbug": bedbug_icon,
    "van": van_icon, "shield": shield_icon, "house": house_icon, "tech": tech_icon,
}

PLAN = (
    [("raccoon", i) for i in range(8)] +
    [("skunk", i) for i in range(7)] +
    [("mosquito", i) for i in range(8)] +
    [("rat", i) for i in range(7)] +
    [("roach", i) for i in range(7)] +
    [("bedbug", i) for i in range(6)] +
    [("van", 0), ("van", 1), ("shield", 0), ("shield", 1), ("house", 0), ("house", 1), ("tech", 0)]
)

def build_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    manifest = {t: [] for t in THEME_ICONS}
    for idx, (theme, n) in enumerate(PLAN, start=1):
        dark, mid, light = pal(idx)
        svg = _canvas_open(dark, mid, light, idx) + THEME_ICONS[theme](light, mid) + _canvas_close()
        fname = f"svg-{idx:02d}-{theme}.svg"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(svg)
        manifest[theme].append(fname)
    return manifest
