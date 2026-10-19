"""生成 GitHub 主页的图片（每张浅色 / 深色两版）：python3 scripts/build_assets.py

主页只负责"不单调"：一张氛围插画横幅 + 三张"最近在研究"小卡片 + 两个链接按钮。
姓名和基本信息已经在 GitHub 左侧边栏，这里不重复；项目交给 Pinned repositories 展示。
- 横幅底部的一行字：TAGLINE
- 横幅两侧的关键词：INPUTS（左，流入）/ OUTPUTS（右，流出）
- 每周更新：NOW + UPDATED
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

TAGLINE = "善用 AI 提效，搭建工作流"
INPUTS = ["需求", "文档", "数据"]
OUTPUTS = ["PRD", "Skill", "Agent"]

UPDATED = "2026-10-19"
NOW = [
    ("DeepSeek Harness 插件架构", "Skill 加载只是开始，治理才是难题"),
    ("SKILL.md 工作流", "让 Agent 稳定调用，也把进度交还给人"),
    ("AI + 非遗数字化", "用 3D 和视频生成，让传统手艺可参与"),
]

SANS = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',system-ui,-apple-system,'Segoe UI',sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "light": dict(bg1="#F6FAFF", bg2="#F1FBF7", blob1="#D6E5FF", blob2="#CFF3E6", blob3="#E6E1FF", border="#E2EAF3",
                  ink="#0F1B2D", ink2="#46546A", muted="#7C8AA0", blue="#2F6BFF", mint="#14B892", lilac="#8B7CF6",
                  sky="#38BDF8", chip="#FFFFFF", chipline="#E2EAF3", shadow="#1E3A5F", shadow_op="0.08",
                  tile=("#EEF4FF", "#E9F8F2", "#F1EEFF"), tileline=("#DCE7FB", "#D3F0E4", "#E2DCFB")),
    "dark": dict(bg1="#0F1626", bg2="#0D1B1F", blob1="#1E3A8A", blob2="#0F766E", blob3="#4C1D95", border="#223047",
                 ink="#E8EEF8", ink2="#AEBBD0", muted="#7F8CA3", blue="#6EA2FF", mint="#4FE0BE", lilac="#A99BFF",
                 sky="#7DD3FC", chip="#152035", chipline="#26354F", shadow="#000000", shadow_op="0.35",
                 tile=("#131F36", "#10231F", "#1A1833"), tileline=("#22345A", "#1C3D35", "#2E2A55")),
}

ICONS = {
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "spark": '<path d="M12 4v4M12 16v4M4 12h4M16 12h4"/>',
}


def tw(s, size, mono=False):
    """粗略估算文字宽度（中文按全角，其余按半角）"""
    return sum(size if ord(c) > 0x2E80 else size * (0.6 if mono else 0.56) for c in s)


def esc(s):
    return escape(str(s), quote=True)


def svg(w, h, body, label, defs="", style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}"><style>text{{font-family:{SANS}}}.m{{font-family:{MONO}}}{style}'
            f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
            f'<defs>{defs}</defs>{"".join(body)}</svg>\n')


def chip(x, y, label, color, t, cls=""):
    w = tw(label, 16) + 44
    return (f'<g class="{cls}"><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="36" rx="18" fill="{t["chip"]}" '
            f'stroke="{t["chipline"]}" stroke-width="1.2" filter="url(#sh)"/>'
            f'<circle cx="{x + 18:.0f}" cy="{y + 18}" r="5" fill="{color}"/>'
            f'<text x="{x + 31:.0f}" y="{y + 24}" font-size="16" font-weight="500" fill="{t["ink2"]}">{esc(label)}</text></g>'), w


# ---------------------------------------------------------------- 横幅
def banner(t):
    W, H = 1200, 300
    cx, cy = 600, 140
    colors = [t["blue"], t["mint"], t["lilac"], t["sky"], t["blue"]]
    left_y = [52, 98, 140, 182, 228]
    right_y = [60, 104, 140, 176, 220]
    defs = (f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>'
            + "".join(f'<radialGradient id="b{i}"><stop offset="0" stop-color="{t[k]}" stop-opacity="0.75"/><stop offset="1" stop-color="{t[k]}" stop-opacity="0"/></radialGradient>'
                      for i, k in enumerate(("blob1", "blob2", "blob3"), 1)) +
            f'<radialGradient id="glow"><stop offset="0" stop-color="{t["blue"]}" stop-opacity="0.35"/><stop offset="1" stop-color="{t["blue"]}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="core" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["blue"]}"/><stop offset="1" stop-color="{t["mint"]}"/></linearGradient>'
            f'<clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24"/></clipPath>'
            f'<filter id="sh" x="-20%" y="-40%" width="140%" height="200%"><feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="{t["shadow"]}" flood-opacity="{t["shadow_op"]}"/></filter>')
    style = (f'.halo{{transform-origin:{cx}px {cy}px;animation:breathe 3.6s ease-in-out infinite}}'
             '@keyframes breathe{50%{transform:scale(1.35);opacity:.35}}'
             '.f1{animation:bob 5s ease-in-out infinite}.f2{animation:bob 6s ease-in-out -2s infinite}'
             '.f3{animation:bob 7s ease-in-out -4s infinite}'
             '@keyframes bob{50%{transform:translateY(-5px)}}')
    b = [f'<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
         f'<circle cx="160" cy="20" r="240" fill="url(#b1)"/><circle cx="1080" cy="290" r="260" fill="url(#b2)"/>'
         f'<circle cx="640" cy="-30" r="220" fill="url(#b3)" opacity="0.6"/>']

    # 汇聚 → 发散的细流
    paths = []
    for i, (ly, ry, c) in enumerate(zip(left_y, right_y, colors)):
        d = f"M-20 {ly} C260 {ly} 380 {cy} {cx} {cy} S940 {ry} 1220 {ry}"
        paths.append(d)
        b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" stroke-opacity="0.45" stroke-linecap="round"/>')
        dur = 7 + i * 1.3
        b.append(f'<circle r="4" fill="{c}"><animateMotion path="{d}" dur="{dur:.1f}s" begin="-{i * 1.7:.1f}s" repeatCount="indefinite"/></circle>')
    b.append("</g>")
    b.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>')

    # 中心 AI 核心
    b.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="url(#glow)"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{t["blue"]}" stroke-opacity="0.5" stroke-width="1.5" class="halo"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="url(#core)"/>')
    b.append(f'<g transform="translate({cx - 11} {cy - 11}) scale(0.92)" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round">{ICONS["spark"]}</g>')

    # 两侧关键词
    for i, (label, y) in enumerate(zip(INPUTS, (34, 122, 210)), 1):
        g, _ = chip(48 + (i % 2) * 70, y, label, colors[i], t, f"f{i}")
        b.append(g)
    for i, (label, y) in enumerate(zip(OUTPUTS, (42, 122, 202)), 1):
        w = tw(label, 16) + 44
        g, _ = chip(W - 48 - w - ((i + 1) % 2) * 70, y, label, colors[-i], t, f"f{(i % 3) + 1}")
        b.append(g)

    # 底部一行字
    b.append(f'<text x="{cx}" y="262" font-size="19" text-anchor="middle" fill="{t["ink2"]}" letter-spacing="1">{esc(TAGLINE)}</text>')
    return svg(W, H, b, f"插画：需求、文档、数据经过 AI 汇聚，流向 PRD、Skill、Agent。{TAGLINE}", defs, style)


# ---------------------------------------------------------------- 最近在研究
def now(t):
    W, H = 1200, 168
    accents = (t["blue"], t["mint"], t["lilac"])
    b = [f'<text x="4" y="22" class="m" font-size="14" fill="{t["muted"]}">NOW · 最近在研究 · 更新于 {UPDATED}</text>']
    tile_w, gap, y0 = 384, 24, 44
    for i, (title, note) in enumerate(NOW):
        x = i * (tile_w + gap)
        b.append(f'<rect x="{x + 1}" y="{y0}" width="{tile_w - 2}" height="{H - y0 - 2}" rx="18" fill="{t["tile"][i]}" stroke="{t["tileline"][i]}" stroke-width="1.5"/>')
        b.append(f'<text x="{x + 26}" y="{y0 + 34}" class="m" font-size="14" font-weight="600" fill="{accents[i]}">0{i + 1}</text>')
        b.append(f'<circle cx="{x + tile_w - 30}" cy="{y0 + 29}" r="5" fill="{accents[i]}"/>')
        b.append(f'<text x="{x + 26}" y="{y0 + 70}" font-size="21" font-weight="700" fill="{t["ink"]}">{esc(title)}</text>')
        b.append(f'<text x="{x + 26}" y="{y0 + 100}" font-size="16" fill="{t["ink2"]}">{esc(note)}</text>')
    return svg(W, H, b, "最近在研究：" + "；".join(f"{a}：{c}" for a, c in NOW))


# ---------------------------------------------------------------- 链接按钮
def pill(icon, label, t):
    W, H = 300, 64
    defs = f'<linearGradient id="core" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["blue"]}"/><stop offset="1" stop-color="{t["mint"]}"/></linearGradient>'
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="31" fill="{t["chip"]}" stroke="{t["chipline"]}" stroke-width="1.5"/>',
         f'<circle cx="33" cy="32" r="21" fill="url(#core)"/>',
         f'<g transform="translate(23 22) scale(0.84)" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>',
         f'<text x="68" y="39" font-size="19" font-weight="600" fill="{t["ink"]}">{esc(label)}</text>',
         f'<text x="{W - 26}" y="40" font-size="20" text-anchor="end" fill="{t["blue"]}">→</text>']
    return svg(W, H, b, label, defs)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for mode, t in THEMES.items():
        (OUT / f"banner-{mode}.svg").write_text(banner(t), encoding="utf-8")
        (OUT / f"now-{mode}.svg").write_text(now(t), encoding="utf-8")
        (OUT / f"pill-site-{mode}.svg").write_text(pill("globe", "个人网站", t), encoding="utf-8")
        (OUT / f"pill-mail-{mode}.svg").write_text(pill("mail", "邮件联系", t), encoding="utf-8")
    print("done:", len(list(OUT.glob("*.svg"))), "files")
