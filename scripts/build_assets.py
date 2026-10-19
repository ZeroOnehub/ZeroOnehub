"""生成 GitHub 主页用的全部 SVG。

每周更新"正在研究"：改下面的 NOW / NOW_UPDATED，然后运行
    python3 scripts/build_assets.py
再 git commit & push 即可。
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

# ───────────────────────── 内容（每周改这里） ─────────────────────────
NOW_UPDATED = "2026-10-19"
NOW = [
    ("DeepSeek Harness 的插件架构",
     "everything-is-a-plugin + Cordis：Skill 加载只是开始，治理才是难题",
     "拆源码中", 0.55),
    ("SKILL.md 工作流设计",
     "让 Skill 既能被 Agent 稳定调用，又能把进度和产出物交还给人",
     "在工坊里实践", 0.7),
    ("AI + 非遗数字化",
     "用 3D、视频生成模型和知识库 Agent，让传统手艺可探索、可参与",
     "做 3.0 陶瓷篇", 0.4),
]

# ───────────────────────── 设计基础 ─────────────────────────
BG0, BG1, LINE = "#0A0F1F", "#111833", "#1E2A4A"
TEXT, MUTED, SOFT = "#E8ECF7", "#8A93AD", "#A9B2CC"
BLUE, CYAN, GREEN, WARM, PINK = "#4D6BFE", "#38BDF8", "#34D399", "#F5B454", "#FB7299"
SANS = ("'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC',"
        "'Noto Sans SC',system-ui,-apple-system,'Segoe UI',sans-serif")
MONO = "'SF Mono','JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"
BASE_CSS = f".s{{font-family:{SANS}}}.m{{font-family:{MONO}}}"

random.seed(1019)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tw(s, size, mono=False):
    """粗略估算文字宽度。"""
    w = 0
    for c in s:
        if ord(c) > 0x2E80:
            w += size
        else:
            w += size * (0.61 if mono else 0.56)
    return w


def svg(w, h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title><style>{BASE_CSS}{css}</style>{body}</svg>\n')


def text(x, y, s, size, fill, cls="s", weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def pill(x, y, s, size, color, mono=True, solid=False):
    w = tw(s, size, mono) + size * 1.5
    h = size * 1.9
    bg = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" '
          f'fill="{color}" fill-opacity="{0.18 if solid else 0.08}" stroke="{color}" stroke-opacity="0.45"/>')
    t = text(f"{x + size*0.75:.1f}", f"{y + h*0.67:.1f}", s, size, color, "m" if mono else "s")
    return bg + t, w


def frame(w, h, rx, inner, grad=(BG1, BG0), stroke=LINE, uid="f"):
    return (f'<defs><linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{grad[0]}"/><stop offset="1" stop-color="{grad[1]}"/></linearGradient>'
            f'<clipPath id="{uid}clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath></defs>'
            f'<g clip-path="url(#{uid}clip)"><rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>{inner}</g>'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{stroke}"/>')


def vase_profile(cx, top, height, scale=1.0):
    """梅瓶轮廓：返回 (y, 半宽) 列表，从口到足。"""
    pts = [(0, 13), (5, 10), (22, 9), (36, 17), (56, 36), (78, 42),
           (100, 37), (118, 27), (132, 20), (140, 19)]
    k = height / 140
    return [(top + y * k, hw * k * scale) for y, hw in pts]


def vase_path(cx, prof):
    right = [(cx + hw, y) for y, hw in prof]
    left = [(cx - hw, y) for y, hw in reversed(prof)]
    pts = right + left

    def cr(p):  # catmull-rom → bezier
        d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
        for i in range(len(p) - 1):
            p0 = p[i - 1] if i > 0 else p[i]
            p1, p2 = p[i], p[i + 1]
            p3 = p[i + 2] if i + 2 < len(p) else p2
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return d
    return cr(right) + " L" + cr(left)[1:] + " Z"


# ───────────────────────── 头图 ─────────────────────────
def header():
    W, H = 1200, 520
    T = 10.0
    times = [0.8 + i * 1.3 for i in range(6)]
    css = [
        "@keyframes flow{to{stroke-dashoffset:-32}}",
        ".flow{animation:flow 1.1s linear infinite}",
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}",
        ".blink{animation:blink 1s steps(1) infinite}",
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}",
        ".pulse{animation:pulse 1.6s ease-in-out infinite}",
        "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}",
    ]
    def lit(i):
        p = times[i] / T
        return (f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" '
                f'values="0;0;1;1;0" keyTimes="0;{p:.3f};{p + 0.03:.3f};0.93;1"/>')
    for i, d in enumerate([1.1, 1.3, 1.5, 1.7, 1.9]):
        css.append(f".r{i}{{animation:rise .6s ease-out {d}s both}}")

    b = []
    # 背景
    b.append('<defs>'
             f'<radialGradient id="g1" cx="0.12" cy="0.05" r="0.7"><stop offset="0" stop-color="{BLUE}" stop-opacity="0.38"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="g2" cx="0.95" cy="1" r="0.55"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.2"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
             '<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="#fff" fill-opacity="0.07"/></pattern>'
             f'<linearGradient id="role" x1="0" x2="1"><stop offset="0" stop-color="#8EA2FF"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
             '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'
             '<clipPath id="type"><rect x="60" y="100" width="150" height="40"><animate attributeName="width" values="0;26;52;78;104;130;150" dur="0.9s" calcMode="discrete" fill="freeze"/></rect></clipPath>'
             '</defs>')
    inner = ('<rect width="1200" height="520" fill="url(#g1)"/><rect width="1200" height="520" fill="url(#g2)"/>'
             '<rect width="1200" height="520" fill="url(#dots)"/>')
    # 顶栏
    inner += ''.join(f'<circle cx="{x}" cy="30" r="7" fill="{c}"/>' for x, c in
                     [(34, "#FF5F57"), (58, "#FEBC2E"), (82, "#28C840")])
    inner += text(600, 36, "fanye@aipm-workbench: ~/career", 17, MUTED, "m", anchor="middle")
    inner += f'<circle class="pulse" cx="1066" cy="30" r="5" fill="{GREEN}"/>'
    inner += text(1164, 36, "running", 17, GREEN, "m", anchor="end")
    inner += f'<line x1="0" y1="60" x2="1200" y2="60" stroke="{LINE}"/>'
    b.append(frame(W, H, 28, inner, (BG1, BG0), uid="h"))

    # 左侧：自我介绍
    b.append(f'<g clip-path="url(#type)">{text(64, 130, "$ whoami", 22, CYAN, "m")}</g>')
    b.append(f'<rect class="blink" x="182" y="112" width="12" height="24" fill="{CYAN}"/>')
    b.append(f'<g class="r0">{text(60, 238, "樊烨", 88, "#F4F6FF", weight=700)}'
             f'{text(256, 238, "Fan Ye", 40, MUTED, weight=500)}</g>')
    b.append(f'<g class="r1">{text(64, 298, "AI 产品经理 · Agent 工作流", 34, "url(#role)", weight=600)}</g>')
    b.append(f'<g class="r2">{text(64, 358, "Agent 的价值不在能调用多少工具，", 22, SOFT)}'
             f'{text(64, 392, "而在能否把岗位工作流沉淀成可复用的 Skill。", 22, SOFT)}</g>')
    x, chips = 64, ""
    for s, c in [("DeepSeek Harness", BLUE), ("SKILL.md", CYAN), ("Human-in-the-loop", WARM)]:
        p, w = pill(x, 428, s, 16, c, solid=True)
        chips += p
        x += w + 12
    b.append(f'<g class="r3">{chips}</g>')

    # 右侧：工作流面板
    b.append(f'<rect x="640" y="92" width="524" height="400" rx="18" fill="#0C1330" fill-opacity="0.85" stroke="{LINE}"/>')
    b.append(text(664, 128, "aipm-hub ▸ pipeline", 17, MUTED, "m"))
    b.append(text(1140, 128, "run #1019", 17, "#5B6685", "m", anchor="end"))
    edge = "M722,190 L1062,190 C1124,190 1124,306 1062,306 L722,306"
    b.append(f'<path d="{edge}" fill="none" stroke="#24305A" stroke-width="2"/>')
    b.append(f'<path class="flow" d="{edge}" fill="none" stroke="{BLUE}" stroke-opacity="0.75" stroke-width="2" stroke-dasharray="6 10"/>')

    # 光点沿管线移动：计算各节点在路径上的位置比例
    def bez(t):
        p0, p1, p2, p3 = (1062, 190), (1124, 190), (1124, 306), (1062, 306)
        return tuple((1-t)**3*a + 3*(1-t)**2*t*b_ + 3*(1-t)*t**2*c + t**3*d
                     for a, b_, c, d in zip(p0, p1, p2, p3))
    curve = sum(math.dist(bez(i/200), bez((i+1)/200)) for i in range(200))
    seg = 1062 - 722
    total = seg * 2 + curve
    stops = [0, 140, 280, seg + curve + (1062 - 1002), seg + curve + (1062 - 862), total]
    fr = [s / total for s in stops]
    kp = ";".join(f"{v:.4f}" for v in [0] + fr + [1])
    kt = ";".join(f"{v:.4f}" for v in [0] + [t / T for t in times] + [1])
    motion = f'<animateMotion dur="{T}s" repeatCount="indefinite" calcMode="linear" keyPoints="{kp}" keyTimes="{kt}" path="{edge}"/>'
    fade = f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.9;0.93;1"/>'
    b.append(f'<g><circle r="13" fill="{CYAN}" fill-opacity="0.55" filter="url(#glow)"/>'
             f'<circle r="5" fill="#E0F6FF"/>{motion}{fade}</g>')

    nodes = [("立项", "project-init", 664, 160), ("PRD", "prd", 804, 160), ("原型", "prototype", 944, 160),
             ("人工确认", "human-gate", 944, 276), ("评测", "evaluation", 804, 276), ("上线", "launch", 664, 276)]
    for i, (lab, sid, nx, ny) in enumerate(nodes):
        gate = sid == "human-gate"
        acc = WARM if gate else BLUE
        dash = ' stroke-dasharray="5 4"' if gate else ""
        cx = nx + 58
        b.append(f'<rect x="{nx}" y="{ny}" width="116" height="60" rx="12" fill="#111A3A" stroke="{acc if gate else "#2A3768"}"{dash}/>')
        b.append(text(cx, ny + 30, lab, 20, "#7D88A8", weight=600, anchor="middle"))
        b.append(text(cx, ny + 50, sid, 13, "#4E5878", "m", anchor="middle"))
        lit_fill = "#3A2A12" if gate else "#1A2763"
        b.append(f'<g>{lit(i)}<rect x="{nx}" y="{ny}" width="116" height="60" rx="12" fill="{lit_fill}" stroke="{acc}" stroke-width="2"/>'
                 f'<rect x="{nx-4}" y="{ny-4}" width="124" height="68" rx="15" fill="none" stroke="{acc}" stroke-opacity="0.35" filter="url(#glow)"/>'
                 f'{text(cx, ny + 30, lab, 20, "#FFFFFF", weight=600, anchor="middle")}'
                 f'{text(cx, ny + 50, sid, 13, acc, "m", anchor="middle")}'
                 f'<circle cx="{nx+112}" cy="{ny+4}" r="10" fill="{GREEN}"/>'
                 f'<path d="M{nx+107},{ny+4} l3.5,3.5 l6,-7" fill="none" stroke="#06281C" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>')

    logs = [(0, "[hub]  ", "新建项目 → 01 立项", CYAN),
            (1, "[skill]", "project-initiation ✓ 立项报告.html", "#C7D0F0"),
            (3, "[human]", "原型已出，等待你来拍板", WARM),
            (5, "[done] ", "workflow → reusable skills ✓", GREEN)]
    b.append(f'<line x1="664" y1="364" x2="1140" y2="364" stroke="{LINE}"/>')
    for row, (ni, tag, msg, c) in enumerate(logs):
        y = 396 + row * 28
        b.append(f'<g>{lit(ni)}{text(664, y, tag, 16, c, "m", extra="xml:space=\"preserve\"")}'
                 f'{text(664 + tw(tag + " ", 16, True), y, msg, 16, "#C7D0F0" if c != "#C7D0F0" else c, "m")}</g>')
    return svg(W, H, "".join(b), "".join(css), "樊烨 Fan Ye · AI 产品经理 · Agent 工作流")


# ───────────────────────── 正在研究 ─────────────────────────
def now_card():
    W, H = 1200, 340
    css = ("@keyframes sh{from{transform:translateX(-160px)}to{transform:translateX(160px)}}"
           ".sh{animation:sh 2.4s ease-in-out infinite}")
    inner = (f'<rect width="{W}" height="{H}" fill="url(#ng)"/>')
    b = [f'<defs><radialGradient id="ng" cx="0" cy="0" r="0.8"><stop offset="0" stop-color="{BLUE}" stop-opacity="0.18"/>'
         f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
         f'<stop offset="0.5" stop-color="#fff" stop-opacity="0.55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>']
    b.append(frame(W, H, 24, inner, uid="n"))
    b.append(text(40, 54, "~/now", 20, BLUE, "m", weight=600))
    b.append(text(118, 54, "这两周在研究", 21, TEXT, weight=600))
    b.append(text(1160, 54, f"updated {NOW_UPDATED} · 每周更新", 15, MUTED, "m", anchor="end"))
    b.append(f'<line x1="40" y1="76" x2="1160" y2="76" stroke="{LINE}"/>')
    for i, (topic, desc, status, prog) in enumerate(NOW):
        y = 96 + i * 80
        b.append(text(40, y + 32, f"0{i+1}", 24, BLUE, "m", weight=600))
        b.append(text(100, y + 30, topic, 22, TEXT, weight=600))
        b.append(text(100, y + 60, desc, 18, SOFT))
        p, w = pill(0, 0, status, 15, CYAN)
        b.append(f'<g transform="translate({1160 - w:.1f},{y + 4})">{p}</g>')
        bx = 1000
        b.append(f'<clipPath id="bar{i}"><rect x="{bx}" y="{y+48}" width="160" height="6" rx="3"/></clipPath>'
                 f'<rect x="{bx}" y="{y+48}" width="160" height="6" rx="3" fill="#1E2A4A"/>'
                 f'<g clip-path="url(#bar{i})"><rect x="{bx}" y="{y+48}" width="{160*prog:.0f}" height="6" fill="{CYAN}"/>'
                 f'<rect class="sh" x="{bx}" y="{y+48}" width="60" height="6" fill="url(#shine)" style="animation-delay:{i*0.5}s"/></g>')
        if i < 2:
            b.append(f'<line x1="100" y1="{y+78}" x2="1160" y2="{y+78}" stroke="{LINE}" stroke-dasharray="3 5"/>')
    return svg(W, H, "".join(b), css, "正在研究")


# ───────────────────────── 项目卡片 ─────────────────────────
def card(uid, label, title, desc, tags, status, accent, illus, illus_bg, href_hint=""):
    W, H = 600, 420
    inner = (f'<clipPath id="{uid}il"><rect width="{W}" height="196"/></clipPath>'
             f'<g clip-path="url(#{uid}il)"><rect width="{W}" height="196" fill="{illus_bg}"/>{illus}</g>')
    inner += f'<line x1="0" y1="196" x2="{W}" y2="196" stroke="{LINE}"/>'
    b = [frame(W, H, 24, inner, uid=uid)]
    b.append(text(36, 240, label, 16, accent, "m"))
    b.append(text(36, 284, title, 32, TEXT, weight=700))
    for i, line in enumerate(desc):
        b.append(text(36, 322 + i * 28, line, 20, SOFT))
    x = 36
    sp, sw = pill(0, 0, status[0], 15, status[1], mono=False, solid=True)
    for t in tags:
        p, w = pill(x, 366, t, 15, MUTED)
        b.append(p)
        x += w + 8
    b.append(f'<g transform="translate({W - 36 - sw:.1f},366)">{sp}</g>')
    return b


def card_workbench():
    css = ("@keyframes dot{0%,100%{opacity:.25}50%{opacity:1}}"
           ".d1{animation:dot 1.2s infinite}.d2{animation:dot 1.2s .2s infinite}.d3{animation:dot 1.2s .4s infinite}")
    il = [f'<rect x="40" y="26" width="520" height="210" rx="14" fill="{BG0}" stroke="#2A3A72"/>',
          f'<line x1="40" y1="52" x2="560" y2="52" stroke="#1E2A55"/>']
    il += [f'<circle cx="{x}" cy="39" r="4.5" fill="{c}"/>' for x, c in [(58, "#FF5F57"), (72, "#FEBC2E"), (86, "#28C840")]]
    il.append(text(300, 44, "AIPM 工坊", 13, MUTED, anchor="middle"))
    for i, (w, c) in enumerate([(72, BLUE), (58, "#24305A"), (66, "#24305A"), (50, "#24305A")]):
        il.append(f'<rect x="56" y="{70 + i*24}" width="{w}" height="12" rx="6" fill="{c}"/>')
    il.append(f'<line x1="146" y1="52" x2="146" y2="236" stroke="#1E2A55"/>')
    il.append(f'<line x1="414" y1="52" x2="414" y2="236" stroke="#1E2A55"/>')
    il.append(f'<rect x="232" y="66" width="168" height="30" rx="15" fill="{BLUE}"/>')
    il.append(text(316, 86, "/aipm-hub 新建项目", 14, "#fff", anchor="middle"))
    il.append(f'<rect x="160" y="108" width="200" height="66" rx="14" fill="#18224A"/>')
    il.append(text(176, 132, "好的，先进入 01 立项：", 14, "#C7D0F0"))
    il += [f'<circle class="d{i+1}" cx="{182 + i*14}" cy="156" r="4" fill="{CYAN}"/>' for i in range(3)]
    il.append(text(428, 78, "项目进度", 13, MUTED))
    for i, (lab, w) in enumerate([("立项", 74), ("PRD", None), ("原型", 0), ("评测", 0)]):
        y = 94 + i * 22
        il.append(text(428, y + 9, lab, 12, "#8A93AD", "m"))
        il.append(f'<rect x="470" y="{y}" width="74" height="8" rx="4" fill="#1E2A55"/>')
        if w is None:
            il.append(f'<rect x="470" y="{y}" width="0" height="8" rx="4" fill="{BLUE}">'
                      '<animate attributeName="width" values="0;56;56;0" keyTimes="0;0.6;0.9;1" dur="4s" repeatCount="indefinite"/></rect>')
        elif w:
            il.append(f'<rect x="470" y="{y}" width="{w}" height="8" rx="4" fill="{GREEN}"/>')
    b = card("wb", "skill://aipm-workbench", "AIPM 工坊",
             ["基于 DeepSeek Harness 二次开发的个人", "AI 产品经理工作台：按阶段推进每个项目"],
             ["Agent", "DeepSeek", "TypeScript"], ("进行中 · 私有", WARM), BLUE,
             "".join(il), "url(#wbill)")
    defs = (f'<defs><linearGradient id="wbill" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#172255"/>'
            f'<stop offset="1" stop-color="#0E1634"/></linearGradient></defs>')
    return svg(600, 420, defs + "".join(b), css, "AIPM 工坊")


def card_skills():
    css = "@keyframes flow{to{stroke-dashoffset:-28}}.flow{animation:flow 1s linear infinite}"
    il = []

    def file(x, y, w, h, lines, color, dashed=False):
        d = ' stroke-dasharray="6 5"' if dashed else ""
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BG0}" stroke="{color}"{d}/>'
        s += f'<path d="M{x+w-18},{y} l18,18" stroke="{color}" stroke-opacity="0.5"/>'
        for i, (t, c) in enumerate(lines):
            s += text(x + 14, y + 24 + i * 18, t, 13, c, "m")
        return s
    for p in ["M212,100 C270,100 270,58 330,58", "M212,100 C270,100 270,146 330,146"]:
        il.append(f'<path d="{p}" fill="none" stroke="#1F3A4A" stroke-width="2"/>')
        il.append(f'<path class="flow" d="{p}" fill="none" stroke="{CYAN}" stroke-width="2" stroke-dasharray="5 9"/>')
    il.append(f'<circle r="5" fill="{CYAN}"><animateMotion dur="2s" repeatCount="indefinite" path="M212,100 C270,100 270,58 330,58"/></circle>')
    il.append(file(40, 34, 172, 128, [("---", "#4E5878"), ("name: aipm-hub", CYAN), ("role: 总控/分派", "#C7D0F0"),
                                      ("---", "#4E5878"), ("# SKILL.md", MUTED)], CYAN))
    il.append(file(330, 22, 230, 72, [("name: project-initiation", "#C7D0F0"), ("stage: 01 立项  ✓", GREEN)], GREEN))
    il.append(file(330, 110, 230, 72, [("name: prd", "#7D88A8"), ("stage: 02 · 即将接入", "#7D88A8")], "#4E5878", True))
    b = card("sk", "skill://aipm-skills", "AIPM Skills",
             ["AI 产品经理全流程 Skill 合集：总控分派", "+ 六站立项教练，PRD / 原型 / 评测陆续接入"],
             ["Skill", "SKILL.md", "Workflow"], ("进行中 · 私有", WARM), CYAN,
             "".join(il), "url(#skill)")
    defs = (f'<defs><linearGradient id="skill" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0F2A36"/>'
            f'<stop offset="1" stop-color="#0B1626"/></linearGradient></defs>')
    return svg(600, 420, defs + "".join(b), css, "AIPM Skills")


def card_chengyi():
    il = []
    il.append('<circle cx="120" cy="58" r="26" fill="#E7B98A" fill-opacity="0.45"/>')
    il.append('<path d="M0,128 Q40,86 80,104 Q120,60 170,96 Q210,70 250,100 Q300,54 350,92 Q400,70 440,98 Q500,62 560,96 L600,90 L600,196 L0,196Z" fill="#A6C3B2" fill-opacity="0.75"/>')
    il.append('<path d="M0,160 Q50,112 100,138 Q150,96 205,146 Q250,120 300,156 Q350,104 405,146 Q450,124 500,156 Q550,136 600,148 L600,196 L0,196Z" fill="#4E8E7A"/>')
    il.append('<path d="M100,138 Q120,128 135,132 M205,146 Q195,120 172,114 M405,146 Q392,124 378,118" stroke="#2F5D52" stroke-width="2" fill="none" opacity="0.6"/>')
    il.append('<path d="M0,196 L0,176 Q60,146 120,180 Q170,158 230,196Z" fill="#2E6377"/>')
    il.append('<path d="M360,196 Q420,152 490,178 Q540,160 600,170 L600,196Z" fill="#2E6377"/>')
    il.append('<path d="M0,196 Q300,178 600,196Z" fill="#B98A5E" fill-opacity="0.55"/>')
    for cx, cy, rx, dur, dx in [(260, 92, 60, 14, 40), (470, 118, 50, 11, -34), (90, 150, 44, 16, 30)]:
        il.append(f'<g opacity="0.85"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="9" fill="#F7F1E3"/>'
                  f'<ellipse cx="{cx+rx*0.35}" cy="{cy-6}" rx="{rx*0.5}" ry="8" fill="#F7F1E3"/>'
                  f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} 0;0 0" dur="{dur}s" repeatCount="indefinite"/></g>')
    prof = vase_profile(470, 40, 140)
    il.append('<ellipse cx="478" cy="182" rx="40" ry="6" fill="#3B2F22" fill-opacity="0.35"/>')
    il.append(f'<path d="{vase_path(470, prof)}" fill="url(#celadon)"/>')
    il.append('<path d="M452,82 Q446,120 456,160" stroke="#fff" stroke-opacity="0.45" stroke-width="5" fill="none" stroke-linecap="round"/>')
    il.append('<rect x="34" y="26" width="34" height="34" rx="4" fill="#B03A2E"/>')
    il.append(text(51, 49, "承艺", 13, "#F7E9D7", weight=700, anchor="middle"))
    b = card("cy", "skill://chengyi", "承艺 · 山河入坊",
             ["非遗数字手作交互原型：青绿山水地图、", "陶瓷与剪纸手作流程，大模型讲解非遗"],
             ["WebGL", "Dify Agent", "交互原型"], ("在线体验 ↗", GREEN), "#6FBF9F",
             "".join(il), "url(#silk)")
    defs = ('<defs><linearGradient id="silk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2EAD6"/>'
            '<stop offset="1" stop-color="#E4D6B6"/></linearGradient>'
            '<linearGradient id="celadon" x1="0" x2="1"><stop offset="0" stop-color="#B7D3C3"/>'
            '<stop offset="0.45" stop-color="#D7E8DC"/><stop offset="1" stop-color="#8FB4A2"/></linearGradient></defs>')
    return svg(600, 420, defs + "".join(b), "", "承艺 · 山河入坊")


def card_chengyi3():
    il = ['<rect width="600" height="196" fill="url(#cy3glow)"/>']
    gold = "#E8C57A"

    def particles(cx, top, h, n, op, scale=1.0):
        prof = vase_profile(cx, top, h, scale)
        s = ""
        for _ in range(n):
            i = random.random() * (len(prof) - 1)
            a, b_ = prof[int(i)], prof[min(int(i) + 1, len(prof) - 1)]
            f = i - int(i)
            y = a[0] + (b_[0] - a[0]) * f
            hw = a[1] + (b_[1] - a[1]) * f
            side = random.choice([-1, 1])
            jitter = random.gauss(0, 1.4)
            x = cx + side * hw + jitter
            r = random.uniform(0.9, 2.2)
            d = random.uniform(1.6, 3.6)
            lo = op * random.uniform(0.2, 0.5)
            s += (f'<circle cx="{x:.1f}" cy="{y + random.gauss(0, 1):.1f}" r="{r:.1f}" fill="{gold}" opacity="{op}">'
                  f'<animate attributeName="opacity" values="{op};{lo:.2f};{op}" dur="{d:.1f}s" begin="-{random.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')
        return s
    prof = vase_profile(300, 24, 146)
    il.append(f'<path d="{vase_path(300, prof)}" fill="url(#ink)" stroke="{gold}" stroke-opacity="0.35"/>')
    il.append('<path d="M282,72 Q276,110 286,150" stroke="#9FD4C8" stroke-opacity="0.35" stroke-width="4" fill="none" stroke-linecap="round"/>')
    il.append(particles(300, 24, 146, 150, 0.95))
    il.append(particles(120, 70, 96, 70, 0.45, 0.85))
    il.append(particles(480, 70, 96, 70, 0.45, 1.1))
    for _ in range(26):
        x, y = random.uniform(20, 580), random.uniform(20, 190)
        d = random.uniform(5, 10)
        il.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(0.6, 1.4):.1f}" fill="{gold}" opacity="0.5">'
                  f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -18;0 0" dur="{d:.1f}s" repeatCount="indefinite"/></circle>')
    acts = ["择土", "练泥", "成形", "施釉", "入窑", "成器", "归土", "承艺"]
    for i, a in enumerate(acts):
        x = 552
        y = 34 + i * 19
        il.append(f'<circle cx="{x}" cy="{y}" r="{3.2 if i == 3 else 2.2}" fill="{gold}" opacity="{1 if i == 3 else 0.4}"/>')
        il.append(text(x - 10, y + 4, a, 11, gold, anchor="end", extra=f'opacity="{0.95 if i == 3 else 0.4}"'))
    b = card("c3", "skill://chengyi-3", "承艺 3.0",
             ["可探索、可参与创作的非遗数字世界：", "八幕陶瓷篇章 + 3D 工作台 + AI 助手"],
             ["Three.js", "即梦视频", "AI 助手"], ("陶瓷篇初版 · 私有", WARM), gold,
             "".join(il), "#0A1A1F")
    defs = ('<defs><radialGradient id="cy3glow" cx="0.5" cy="0.55" r="0.6"><stop offset="0" stop-color="#1C4A4E" stop-opacity="0.9"/>'
            '<stop offset="1" stop-color="#0A1A1F" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="ink" x1="0" x2="1"><stop offset="0" stop-color="#123A3D"/><stop offset="0.5" stop-color="#1D5552"/>'
            '<stop offset="1" stop-color="#0E2B2E"/></linearGradient></defs>')
    return svg(600, 420, defs + "".join(b), "", "承艺 3.0")


def card_bilibili():
    W, H = 1200, 220
    b = [f'<defs><clipPath id="screen"><rect x="640" y="24" width="524" height="172" rx="14"/></clipPath>'
         f'<linearGradient id="scr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A1530"/>'
         f'<stop offset="1" stop-color="#140B1C"/></linearGradient>'
         f'<radialGradient id="bg" cx="1" cy="0" r="0.7"><stop offset="0" stop-color="{PINK}" stop-opacity="0.2"/>'
         f'<stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient></defs>']
    b.append(frame(W, H, 24, f'<rect width="{W}" height="{H}" fill="url(#bg)"/>', uid="bl"))
    b.append(text(40, 52, "skill://bilibili-promo", 16, PINK, "m"))
    b.append(text(40, 96, "哔哩哔哩产品宣传页", 32, TEXT, weight=700))
    b.append(text(40, 132, "整页就是一支 B 站视频：滚动即播放，章节即分 P，", 20, SOFT))
    b.append(text(40, 160, "还能发弹幕、一键三连、选互动结局。", 20, SOFT))
    x = 40
    for t in ["原生 JS", "0 依赖", "课程作业"]:
        p, w = pill(x, 178, t, 14, MUTED)
        b.append(p)
        x += w + 8
    sp, sw = pill(0, 0, "在线预览 ↗", 14, GREEN, mono=False, solid=True)
    b.append(f'<g transform="translate({600 - sw:.1f},178)">{sp}</g>')
    b.append(f'<rect x="640" y="24" width="524" height="172" rx="14" fill="url(#scr)" stroke="#3A2440"/>')
    dm = [("前方高能！！！", "#FFFFFF", 60, 7, 0), ("一键三连 ✓✓✓", PINK, 90, 9, -3),
          ("这页面就是一支视频", "#9BE7FF", 120, 8, -5), ("互动结局我选 B", "#FFE08A", 60, 10, -6),
          ("UP 主做得好用心", "#FFFFFF", 150, 11, -2), ("滚动=播放 太妙了", "#FFFFFF", 120, 7.5, -1)]
    dmk = ""
    OP92 = 'opacity="0.92"'
    for s, c, y, d, beg in dm:
        dmk += (f'<g>{text(1180, y, s, 17, c, weight=600, extra=OP92)}'
                f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-760 0" dur="{d}s" begin="{beg}s" repeatCount="indefinite"/></g>')
    b.append(f'<g clip-path="url(#screen)">{dmk}</g>')
    b.append(f'<circle cx="902" cy="104" r="26" fill="{PINK}" fill-opacity="0.9"/><path d="M894,91 L894,117 L916,104Z" fill="#fff"/>')
    b.append(f'<rect x="660" y="174" width="484" height="5" rx="2.5" fill="#3A2A44"/>')
    b.append(f'<rect x="660" y="174" width="0" height="5" rx="2.5" fill="{PINK}"><animate attributeName="width" values="0;484" dur="12s" repeatCount="indefinite"/></rect>')
    for i in range(1, 4):
        b.append(f'<rect x="{660 + i*121 - 1}" y="172" width="2" height="9" fill="#fff" fill-opacity="0.7"/>')
    return svg(W, H, "".join(b), "", "哔哩哔哩产品宣传页")


# ───────────────────────── 分节标题 & 页脚（浅/深两套） ─────────────────────────
def section(idx, zh, en, dark):
    W, H = 1200, 80
    fg = "#E6EDF3" if dark else "#1F2328"
    sub = "#7D8590" if dark else "#656D76"
    b = [f'<defs><linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/>'
         f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient></defs>']
    b.append(text(4, 52, idx, 30, BLUE, "m", weight=700))
    b.append(text(58, 52, zh, 32, fg, weight=700))
    x = 58 + tw(zh, 32) + 18
    b.append(text(x, 50, en, 16, sub, "m", extra='letter-spacing="3"'))
    x2 = x + tw(en, 16, True) + len(en) * 3 + 24
    b.append(f'<rect x="{x2:.0f}" y="41" width="{1196 - x2:.0f}" height="2" fill="url(#ln)"/>')
    return svg(W, H, "".join(b), "", f"{idx} {zh}")


def footer(dark):
    W, H = 1200, 90
    fg = "#7D8590" if dark else "#656D76"
    css = "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1s steps(1) infinite}"
    s = "$ git push origin main   # 把 GitHub 当朋友圈维护，每天一次真实推送"
    w = tw(s, 18, True)
    x = (W - w) / 2
    b = [text(x, 50, s, 18, fg, "m"),
         f'<rect class="blink" x="{x + w + 6:.0f}" y="34" width="10" height="20" fill="{BLUE}"/>']
    return svg(W, H, "".join(b), css, "每天一次真实推送")


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "now.svg": now_card(),
        "card-aipm-workbench.svg": card_workbench(),
        "card-aipm-skills.svg": card_skills(),
        "card-chengyi.svg": card_chengyi(),
        "card-chengyi-3.svg": card_chengyi3(),
        "card-bilibili.svg": card_bilibili(),
    }
    for idx, zh, en, slug in [("01", "正在研究", "NOW", "now"), ("02", "精选项目", "PROJECTS", "projects"),
                              ("03", "联系我", "CONTACT", "contact")]:
        files[f"sec-{slug}-light.svg"] = section(idx, zh, en, False)
        files[f"sec-{slug}-dark.svg"] = section(idx, zh, en, True)
    files["footer-light.svg"] = footer(False)
    files["footer-dark.svg"] = footer(True)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print("\n".join(sorted(files)))


if __name__ == "__main__":
    main()
