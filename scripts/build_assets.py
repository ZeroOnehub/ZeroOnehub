"""生成 GitHub 主页的图片（每张浅色 / 深色两版）：python3 scripts/build_assets.py

主页只做简洁的自我介绍；项目交给 GitHub 自带的 Pinned / Popular repositories 展示。
- 改个人信息：PROFILE
- 改头图右侧的三个浮动标签：ORBIT_TAGS
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

PROFILE = dict(
    name="樊烨",
    role="AI 产品经理",
    tagline="善用 AI 提效，搭建工作流",
    handles="github.com/ZeroOnehub  ·  zeroonehub.github.io",
)
ORBIT_TAGS = ["AI 提效", "工作流搭建", "产品落地"]

SANS = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',system-ui,-apple-system,'Segoe UI',sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "light": dict(bg1="#F6FAFF", bg2="#F1FBF7", blob1="#CFE0FF", blob2="#C8F1E1", border="#E2EAF3",
                  ink="#0F1B2D", ink2="#46546A", muted="#7C8AA0", blue="#2F6BFF", mint="#14B892", lilac="#8B7CF6",
                  orbit="#D3DFEE", chip="#FFFFFF", chipline="#E2EAF3", shadow="#1E3A5F", shadow_op="0.08"),
    "dark": dict(bg1="#0F1626", bg2="#0D1B1F", blob1="#1E3A8A", blob2="#0F766E", border="#223047",
                 ink="#E8EEF8", ink2="#AEBBD0", muted="#7F8CA3", blue="#6EA2FF", mint="#4FE0BE", lilac="#A99BFF",
                 orbit="#2A3A55", chip="#152035", chipline="#26354F", shadow="#000000", shadow_op="0.35"),
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


# ---------------------------------------------------------------- 头图
def header(t):
    W, H = 1200, 380
    P = PROFILE
    cx, cy = 935, 190
    defs = (f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>'
            f'<radialGradient id="b1"><stop offset="0" stop-color="{t["blob1"]}" stop-opacity="0.75"/><stop offset="1" stop-color="{t["blob1"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="b2"><stop offset="0" stop-color="{t["blob2"]}" stop-opacity="0.7"/><stop offset="1" stop-color="{t["blob2"]}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="core" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["blue"]}"/><stop offset="1" stop-color="{t["mint"]}"/></linearGradient>'
            f'<clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28"/></clipPath>'
            f'<filter id="sh" x="-20%" y="-40%" width="140%" height="200%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="{t["shadow"]}" flood-opacity="{t["shadow_op"]}"/></filter>')
    style = (f'.o1{{transform-origin:{cx}px {cy}px;animation:spin 22s linear infinite}}'
             f'.o2{{transform-origin:{cx}px {cy}px;animation:spin 36s linear infinite reverse}}'
             f'.o3{{transform-origin:{cx}px {cy}px;animation:spin 54s linear infinite}}'
             '@keyframes spin{to{transform:rotate(360deg)}}'
             '.f1{animation:bob 5s ease-in-out infinite}.f2{animation:bob 6s ease-in-out -2s infinite}.f3{animation:bob 7s ease-in-out -4s infinite}'
             '@keyframes bob{50%{transform:translateY(-6px)}}')
    b = [f'<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
         f'<circle cx="1060" cy="40" r="300" fill="url(#b1)"/><circle cx="760" cy="400" r="260" fill="url(#b2)"/>'
         f'<circle cx="80" cy="-40" r="200" fill="url(#b1)" opacity="0.5"/></g>',
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>']

    # 左侧文字
    b.append(f'<text x="76" y="118" font-size="24" fill="{t["muted"]}">你好，我是</text>')
    b.append(f'<text x="72" y="214" font-size="92" font-weight="700" letter-spacing="6" fill="{t["ink"]}">{esc(P["name"])}</text>')
    dot_x = 72 + tw(P["name"], 92) + 6 * len(P["name"]) + 10
    b.append(f'<circle cx="{dot_x:.0f}" cy="200" r="9" fill="url(#core)"/>')
    role_w = tw(P["role"], 26)
    b.append(f'<text x="76" y="270" font-size="26" font-weight="600" fill="{t["blue"]}">{esc(P["role"])}</text>')
    b.append(f'<line x1="{76 + role_w + 18:.0f}" y1="252" x2="{76 + role_w + 18:.0f}" y2="274" stroke="{t["border"]}" stroke-width="2"/>')
    b.append(f'<text x="{76 + role_w + 36:.0f}" y="270" font-size="26" fill="{t["ink2"]}">{esc(P["tagline"])}</text>')
    b.append(f'<text x="76" y="322" class="m" font-size="15" fill="{t["muted"]}">{esc(P["handles"])}</text>')

    # 右侧星轨
    for r, dash in ((70, ""), (112, ' stroke-dasharray="2 7"'), (150, "")):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["orbit"]}" stroke-width="1.6"{dash}/>')
    b.append(f'<g class="o1"><circle cx="{cx + 70}" cy="{cy}" r="8" fill="{t["mint"]}"/></g>')
    b.append(f'<g class="o2"><circle cx="{cx}" cy="{cy - 112}" r="7" fill="{t["blue"]}"/></g>')
    b.append(f'<g class="o3"><circle cx="{cx - 150}" cy="{cy}" r="6" fill="{t["lilac"]}"/></g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="url(#core)"/>')
    b.append(f'<g transform="translate({cx - 13} {cy - 13}) scale(1.08)" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round">{ICONS["spark"]}</g>')

    # 浮动标签
    spots = [(cx - 190, cy - 118, t["mint"]), (cx + 92, cy - 30, t["blue"]), (cx - 120, cy + 104, t["lilac"])]
    for i, (tag, (x, y, c)) in enumerate(zip(ORBIT_TAGS, spots), 1):
        w = tw(tag, 16) + 44
        b.append(f'<g class="f{i}"><rect x="{x}" y="{y}" width="{w:.0f}" height="38" rx="19" fill="{t["chip"]}" stroke="{t["chipline"]}" stroke-width="1.2" filter="url(#sh)"/>'
                 f'<circle cx="{x + 19}" cy="{y + 19}" r="5" fill="{c}"/>'
                 f'<text x="{x + 32}" y="{y + 25}" font-size="16" font-weight="500" fill="{t["ink2"]}">{esc(tag)}</text></g>')

    return svg(W, H, b, f'你好，我是{P["name"]} · {P["role"]} · {P["tagline"]}', defs, style)


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
        (OUT / f"header-{mode}.svg").write_text(header(t), encoding="utf-8")
        (OUT / f"pill-site-{mode}.svg").write_text(pill("globe", "个人网站", t), encoding="utf-8")
        (OUT / f"pill-mail-{mode}.svg").write_text(pill("mail", "邮件联系", t), encoding="utf-8")
    print("done:", len(list(OUT.glob("*.svg"))), "files")
