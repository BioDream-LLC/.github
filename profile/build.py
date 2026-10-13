#!/usr/bin/env python3
"""Generate the organization profile artwork.

Every product card and the banner come in a dark and a light variant, matching the visitor's GitHub
theme through <picture> (the only media query GitHub honours). Cards are drawn at phone proportions
and shown 430 px wide: two to a row on a desktop, one per row on a phone, readable on both. GitHub paints a grey square behind transparent images and cannot style tables as cards,
so each card is drawn complete, shadow included, as one SVG.

Run from this directory: python3 build.py  (standard library only)
"""

import base64
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "gen")
FONT = "-apple-system, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(card0="#1b222c", card1="#121820", border="#30363d", text="#f0f6fc", muted="#9ea8b3",
                 shadow="#000000", shadow_op=0.55, chip_bg_op=0.16, rule="#ffffff", rule_op=0.07),
    "light": dict(card0="#ffffff", card1="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#57606a",
                  shadow="#1f2328", shadow_op=0.14, chip_bg_op=0.10, rule="#1f2328", rule_op=0.07),
}

# Chip colours: (dark-theme text, light-theme text, tint).
GREEN = ("#7ee2a8", "#1a7f37", "#2ea043")
ORANGE = ("#ffb36b", "#bc4c00", "#f58220")
BLUE = ("#8cc4ff", "#0b5cad", "#388bfd")
TEAL = ("#6ee7d8", "#0b766b", "#14b8a6")
VIOLET = ("#c2b8ff", "#5a3fc0", "#8b7bff")
GREY = ("#c4ccd4", "#57606a", "#8b949e")
AMBER = ("#ffcf70", "#9a6700", "#d29922")


def esc(s):
    return html.escape(s, quote=True)


def text_width(s, size):
    """A rough width for wrapping: average glyph widths of a sans-serif face."""
    w = 0.0
    for ch in s:
        if ch in "il.,:;'|!·":
            w += 0.28
        elif ch in "mwMW@":
            w += 0.86
        elif ch.isupper() or ch.isdigit():
            w += 0.64
        elif ch == " ":
            w += 0.28
        else:
            w += 0.53
    return w * size


def wrap(s, size, width):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if cur and text_width(trial, size) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- product icons, drawn inline

def icon_biodream(x, y, s):
    with open(os.path.join(HERE, "assets", "biodream-app.png"), "rb") as f:
        data = base64.b64encode(f.read()).decode()
    r = s / 2
    return (f'<clipPath id="bdclip"><circle cx="{x + r}" cy="{y + r}" r="{r}"/></clipPath>'
            f'<circle cx="{x + r}" cy="{y + r}" r="{r}" fill="#ffffff"/>'
            f'<image href="data:image/png;base64,{data}" x="{x}" y="{y}" width="{s}" height="{s}" '
            f'clip-path="url(#bdclip)" preserveAspectRatio="xMidYMid slice"/>')


def icon_frame(x, y, s, inner):
    return (f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 96 96">'
            f'<rect x="4" y="4" width="88" height="88" rx="20" fill="#0f172a"/>'
            f'<rect x="4.75" y="4.75" width="86.5" height="86.5" rx="19.25" fill="none" stroke="#2b3a52" stroke-width="1.5"/>'
            f'{inner}</svg>')


def icon_perfuse(x, y, s):
    inner = ('<defs><linearGradient id="pfg" gradientUnits="userSpaceOnUse" x1="18" y1="30" x2="62" y2="66">'
             '<stop offset="0" stop-color="#22d3ee"/><stop offset=".55" stop-color="#3b82f6"/><stop offset="1" stop-color="#6366f1"/>'
             '</linearGradient></defs>'
             '<g fill="none" stroke="url(#pfg)" stroke-width="3.5" stroke-linecap="round">'
             '<path d="M18 30 H34 Q44 30 46 40 L48 48"/><path d="M18 48 H46"/><path d="M18 66 H34 Q44 66 46 56 L48 48"/><path d="M48 48 H62"/></g>'
             '<path d="M60 48 h5 l3.5 -13 l5 26 l4 -13 H82" fill="none" stroke="#e2e8f0" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
             '<g fill="url(#pfg)"><circle cx="18" cy="30" r="3.5"/><circle cx="18" cy="48" r="3.5"/><circle cx="18" cy="66" r="3.5"/></g>')
    return icon_frame(x, y, s, inner)


BITVOICE_INNER = (
    '<defs><linearGradient id="bvg" gradientUnits="userSpaceOnUse" x1="20" y1="20" x2="76" y2="76">'
    '<stop offset="0" stop-color="#34d399"/><stop offset=".55" stop-color="#14b8a6"/><stop offset="1" stop-color="#0ea5e9"/>'
    '</linearGradient></defs>'
    '<g stroke="url(#bvg)" stroke-width="6" stroke-linecap="round">'
    '<path d="M24 42 V54"/><path d="M36 32 V64"/><path d="M48 22 V74"/><path d="M60 34 V62"/><path d="M72 42 V54"/></g>')

BITDISPATCHER_INNER = (
    '<defs><linearGradient id="bdg" gradientUnits="userSpaceOnUse" x1="18" y1="25" x2="78" y2="79">'
    '<stop offset="0" stop-color="#fbbf24"/><stop offset=".6" stop-color="#f97316"/><stop offset="1" stop-color="#ef4444"/>'
    '</linearGradient></defs>'
    '<g fill="none" stroke="url(#bdg)" stroke-linecap="round">'
    '<ellipse cx="48" cy="70" rx="30" ry="9" stroke-width="2.5" stroke-opacity="0.45"/>'
    '<ellipse cx="48" cy="70" rx="17" ry="5" stroke-width="3" stroke-opacity="0.8"/></g>'
    '<path d="M48 70 C40 58 33 50 33 40 a15 15 0 0 1 30 0 C63 50 56 58 48 70 Z" fill="url(#bdg)"/>'
    '<circle cx="48" cy="40" r="5.5" fill="#0f172a"/>')


def icon_bitvoice(x, y, s):
    return icon_frame(x, y, s, BITVOICE_INNER)


def icon_bitdispatcher(x, y, s):
    return icon_frame(x, y, s, BITDISPATCHER_INNER)


PRODUCTS = [
    dict(key="biodream", name="BioDream", accent="#f58220", icon=icon_biodream,
         tagline="An offline AI companion that feels.",
         body="A fine-tuned model running entirely on your phone, with a 16-dimension emotion engine, seven "
              "stages of closeness, and long-term memory that comes up only when it is relevant. "
              "No conversation ever leaves the device.",
         chips=[("Android · available", GREEN), ("100% on-device", ORANGE), ("iOS · planned", GREY)]),
    dict(key="perfuse", name="Perfuse", accent="#3b82f6", icon=icon_perfuse,
         tagline="Open-source healthcare integration engine.",
         body="HL7 v2, FHIR, DICOM, X12 and CDA in one static binary, with all four CMS-0057-F payer APIs, "
              "tested with Inferno. A modern alternative to Mirth Connect: no JVM, no installer, no licence fee.",
         chips=[("Apache 2.0", BLUE), ("Inferno tested", GREEN), ("Go", TEAL)]),
    dict(key="bitvoice", name="BitVoice", accent="#14b8a6", icon=icon_bitvoice,
         tagline="Open-source phone system and NG911 call handling.",
         body="One Go binary: a complete office phone system, NG911 call handling, a P25 radio dispatch "
              "console and NG911 Core Services, configured from a built-in web console and built to the "
              "911 reliability bar.",
         chips=[("Apache 2.0", BLUE), ("PBX · working", GREEN), ("911 · not yet certified", AMBER)]),
    dict(key="bitdispatcher", name="bitdispatcher", accent="#f97316", icon=icon_bitdispatcher,
         tagline="Open-source computer-aided dispatch.",
         body="CAD with built-in records management, mobile units and radio data, for emergency "
              "communications centres. It connects to any call-handling system through open standards "
              "(NENA i3, EIDO).",
         chips=[("In development", VIOLET), ("Apache 2.0", BLUE)]),
]

# Layouts. Sizes are chosen for the size the image is shown at: about 960 px wide on a desktop,
# about 345 px on a phone, so text stays near 15 px or more on screen in both.
LAYOUT = {
    "wide": dict(W=1200, pad=28, ip=40, icon=104, title=46, tag=26, body=24, lead=36, chip=20, chip_h=40, gap=26),
    "narrow": dict(W=720, pad=24, ip=40, icon=120, title=60, tag=34, body=32, lead=46, chip=28, chip_h=56, gap=30),
}


def chips_svg(chips, x, y, L, t, theme, maxw):
    out, cx, cy = [], x, y
    for label, (dark_fg, light_fg, tint) in chips:
        w = text_width(label, L["chip"]) + L["chip"] * 1.6
        if cx > x and cx + w > x + maxw:
            cx, cy = x, cy + L["chip_h"] + 14
        fg = dark_fg if theme == "dark" else light_fg
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{L["chip_h"]}" rx="{L["chip_h"] / 2}" '
                   f'fill="{tint}" fill-opacity="{t["chip_bg_op"]}" stroke="{tint}" stroke-opacity="0.55" stroke-width="1.5"/>'
                   f'<text x="{cx + w / 2:.1f}" y="{cy + L["chip_h"] * 0.66:.1f}" font-size="{L["chip"]}" font-weight="600" '
                   f'fill="{fg}" text-anchor="middle">{esc(label)}</text>')
        cx += w + 12
    return "".join(out), cy + L["chip_h"]


def card(p, theme, layout, min_h=0):
    t, L = THEMES[theme], LAYOUT[layout]
    W, pad, ip = L["W"], L["pad"], L["ip"]
    cw = W - 2 * pad                     # card width
    x0 = pad + ip                        # content left edge
    inner = cw - 2 * ip                  # content width
    parts = []

    if layout == "wide":
        # Icon on the left, everything else in a column beside it.
        tx = x0 + L["icon"] + 32
        tw = W - pad - ip - tx
        y = pad + ip
        icon = p["icon"](x0, y, L["icon"])
        title_y = y + L["title"] * 0.86
        tag_y = title_y + L["tag"] + 14
        body_lines = wrap(p["body"], L["body"], tw)
        body_y = tag_y + L["lead"] + 8
        chips_y = body_y + (len(body_lines) - 1) * L["lead"] + L["gap"]
        chips, chips_end = chips_svg(p["chips"], tx, chips_y, L, t, theme, tw)
        text_x = tx
    else:
        # Icon and title on one row, the rest full width below.
        y = pad + ip
        icon = p["icon"](x0, y, L["icon"])
        tx = x0 + L["icon"] + 28
        title_y = y + L["icon"] / 2 + L["title"] * 0.34
        tag_lines = wrap(p["tagline"], L["tag"], inner)
        tag_y = y + L["icon"] + 30 + L["tag"]
        body_y = tag_y + (len(tag_lines) - 1) * (L["tag"] + 10) + L["lead"] + 18
        body_lines = wrap(p["body"], L["body"], inner)
        chips_y = body_y + (len(body_lines) - 1) * L["lead"] + L["gap"]
        chips, chips_end = chips_svg(p["chips"], x0, chips_y, L, t, theme, inner)
        text_x = x0

    H = max(int(chips_end + ip + pad), min_h)
    ch = H - 2 * pad

    parts.append(f'<rect x="{pad}" y="{pad}" width="{cw}" height="{ch}" rx="22" fill="url(#cardfill)" '
                 f'stroke="{t["border"]}" stroke-width="1.5" filter="url(#lift)"/>')
    # Accent: a glow in the top-left corner and a bar along the left edge.
    parts.append(f'<rect x="{pad}" y="{pad}" width="{cw}" height="{ch}" rx="22" fill="url(#accentglow)"/>')
    parts.append(f'<rect x="{pad}" y="{pad + 26}" width="5" height="{ch - 52}" rx="2.5" fill="{p["accent"]}"/>')
    parts.append(icon)
    parts.append(f'<text x="{tx}" y="{title_y:.1f}" font-size="{L["title"]}" font-weight="800" fill="{t["text"]}" '
                 f'letter-spacing="-0.5">{esc(p["name"])}</text>')
    if layout == "wide":
        parts.append(f'<text x="{tx}" y="{tag_y:.1f}" font-size="{L["tag"]}" font-weight="600" fill="{p["accent"]}">'
                     f'{esc(p["tagline"])}</text>')
    else:
        for i, line in enumerate(tag_lines):
            parts.append(f'<text x="{x0}" y="{tag_y + i * (L["tag"] + 10):.1f}" font-size="{L["tag"]}" font-weight="600" '
                         f'fill="{p["accent"]}">{esc(line)}</text>')
    for i, line in enumerate(body_lines):
        parts.append(f'<text x="{text_x}" y="{body_y + i * L["lead"]:.1f}" font-size="{L["body"]}" fill="{t["muted"]}">'
                     f'{esc(line)}</text>')
    parts.append(chips)

    defs = (f'<defs>'
            f'<linearGradient id="cardfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["card0"]}"/>'
            f'<stop offset="1" stop-color="{t["card1"]}"/></linearGradient>'
            f'<radialGradient id="accentglow" cx="0" cy="0" r="0.75" gradientTransform="scale(0.6 1)">'
            f'<stop offset="0" stop-color="{p["accent"]}" stop-opacity="{0.16 if theme == "dark" else 0.09}"/>'
            f'<stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></radialGradient>'
            f'<filter id="lift" x="-5%" y="-8%" width="110%" height="125%">'
            f'<feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="{t["shadow"]}" flood-opacity="{t["shadow_op"]}"/>'
            f'</filter></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="{esc(p["name"])}: {esc(p["tagline"])}">'
            f'<title>{esc(p["name"])}</title><desc>{esc(p["tagline"] + " " + p["body"])}</desc>'
            f'{defs}<g font-family="{FONT}">{"".join(parts)}</g></svg>\n'), H


# ---------------------------------------------------------------- banner

def banner(theme):
    """One banner for every screen: large type only, so it stays legible at phone width (about 27%)."""
    dark = theme == "dark"
    bg = ("#0b0b2b", "#16154d", "#1f1d66") if dark else ("#ffffff", "#f6f6ff", "#ecebff")
    title = "#ffffff" if dark else "#1c1b5a"
    sub = "#c7c9f5" if dark else "#45457a"
    dots = ("#ffffff", 0.05) if dark else ("#1c1b5a", 0.06)
    rung = ("#ffffff", 0.12) if dark else ("#1c1b5a", 0.15)
    strand2 = ("#6d6bff", "#a5b4fc") if dark else ("#3f3db8", "#1c1b5a")
    W, H = 1280, 440
    mid = 372
    helix = f"M-40 {mid} C80 {mid-46} 240 {mid-46} 320 {mid} S560 {mid+46} 640 {mid} S880 {mid-46} 960 {mid} S1200 {mid+46} 1320 {mid}"
    helix2 = f"M-40 {mid} C80 {mid+46} 240 {mid+46} 320 {mid} S560 {mid-46} 640 {mid} S880 {mid+46} 960 {mid} S1200 {mid-46} 1320 {mid}"
    rungs = [x for x in range(40, 1280, 80) if x % 320 not in (0,)]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
           '<title id="t">BioDream LLC</title>',
           '<desc id="d">Private, on-device AI and open-source software for healthcare and public safety.</desc>',
           f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg[0]}"/>'
           f'<stop offset="0.6" stop-color="{bg[1]}"/><stop offset="1" stop-color="{bg[2]}"/></linearGradient>'
           f'<linearGradient id="orange" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f58220"/><stop offset="1" stop-color="#ffb347"/></linearGradient>'
           f'<linearGradient id="indigo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{strand2[0]}"/><stop offset="1" stop-color="{strand2[1]}"/></linearGradient>'
           f'<radialGradient id="glow" cx="0.85" cy="0.2" r="0.6"><stop offset="0" stop-color="#f58220" stop-opacity="0.16"/>'
           f'<stop offset="1" stop-color="#f58220" stop-opacity="0"/></radialGradient>'
           f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{dots[0]}" fill-opacity="{dots[1]}"/></pattern>'
           f'<clipPath id="inside"><rect width="{W}" height="{H}" rx="28"/></clipPath></defs>',
           f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"' + ('' if dark else ' stroke="#d8d8f0" stroke-width="3"') + '/>',
           f'<rect width="{W}" height="{H}" rx="28" fill="url(#dots)"/><rect width="{W}" height="{H}" rx="28" fill="url(#glow)"/>',
           f'<g clip-path="url(#inside)" fill="none" stroke-linecap="round"><g stroke="{rung[0]}" stroke-opacity="{rung[1]}" stroke-width="3">']
    out += [f'<path d="M{x} {mid-30} V{mid+30}"/>' for x in rungs]
    out.append(f'</g><path d="{helix}" stroke="url(#orange)" stroke-width="14"/><path d="{helix2}" stroke="url(#indigo)" stroke-width="14"/></g>')
    out.append(f'<g font-family="{FONT}" text-anchor="middle">'
               f'<text x="{W/2}" y="160" font-size="124" font-weight="800" fill="{title}" letter-spacing="-2">BioDream <tspan fill="#f58220">LLC</tspan></text>'
               f'<text x="{W/2}" y="232" font-size="46" fill="{sub}">Private, on-device AI and open-source software</text>'
               f'<text x="{W/2}" y="290" font-size="46" fill="{sub}">for healthcare and public safety.</text>'
               '</g></svg>\n')
    return "".join(out)


def standalone_icon(inner, name, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" role="img" aria-label="{name}">'
            f'<title>{name}</title><desc>{desc}</desc>'
            f'<rect x="4" y="4" width="88" height="88" rx="20" fill="#0f172a"/>'
            f'<rect x="4.75" y="4.75" width="86.5" height="86.5" rx="19.25" fill="none" stroke="#1e293b" stroke-width="1.5"/>'
            f'{inner}</svg>\n')


ROWS = [("biodream", "perfuse"), ("bitvoice", "bitdispatcher")]


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    by_key = {p["key"]: p for p in PRODUCTS}
    for theme in THEMES:
        with open(os.path.join(OUT, f"banner-{theme}.svg"), "w") as f:
            f.write(banner(theme))
        for row in ROWS:
            h = max(card(by_key[k], theme, "narrow")[1] for k in row)
            for k in row:
                with open(os.path.join(OUT, f"card-{k}-{theme}.svg"), "w") as f:
                    f.write(card(by_key[k], theme, "narrow", h)[0])
    with open(os.path.join(HERE, "assets", "bitvoice.svg"), "w") as f:
        f.write(standalone_icon(BITVOICE_INNER, "BitVoice", "A voice waveform inside a rounded square."))
    with open(os.path.join(HERE, "assets", "bitdispatcher.svg"), "w") as f:
        f.write(standalone_icon(BITDISPATCHER_INNER, "bitdispatcher",
                                "A map pin at the centre of expanding rings inside a rounded square."))
    print("wrote", len(os.listdir(OUT)), "files to assets/gen")


if __name__ == "__main__":
    main()
