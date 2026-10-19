"""生成 GitHub 主页的全部图片（每张浅色 / 深色两版）：python3 scripts/build_assets.py

视觉与个人网站 https://zeroonehub.github.io 一致：整个主页是一条工作流。
- 改个人信息：PROFILE
- 每周更新"正在研究"：NOW + UPDATED
- 改项目：PROJECTS（最多 6 个），重新运行后同步 README 里的链接
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

PROFILE = dict(
    name="樊烨",
    seal="樊",
    role="AI 产品经理",
    tagline="善用 AI 提效，搭建工作流",
    tags=["AI 产品经理", "AI 提效", "工作流搭建"],
    site="zeroonehub.github.io",
    email="j567564345@gmail.com",
)

UPDATED = "2026-10-19"
NOW = [
    ("DeepSeek Harness 插件架构", "Skill 加载只是开始，治理才是难题"),
    ("SKILL.md 工作流", "让 Agent 稳定调用，也把进度交还给人"),
    ("AI + 非遗数字化", "用 3D 和视频生成，让传统手艺可参与"),
]

# slug, 分类, 名称, 两行描述, 语言, 状态（None 则按是否有演示显示"已上线"/"开源"）, 演示链接文字
PROJECTS = [
    ("aipm-workbench", "AGENT", "AIPM 工坊",
     ["基于 DeepSeek Harness 二次开发的", "个人 AI 产品经理工作台，按阶段推进项目"],
     "TypeScript", "进行中", None),
    ("aipm-skills", "SKILL", "AIPM Skills",
     ["产品经理全流程 Skill 合集：总控分派", "+ 六站立项教练，PRD / 评测陆续接入"],
     "HTML", "进行中", None),
    ("chengyi", "AI × 非遗", "承艺 · 山河入坊",
     ["非遗数字手作交互原型：青绿山水地图", "+ 陶瓷剪纸手作，大模型讲解非遗"],
     "JavaScript", None, "在线体验 ↗"),
    ("chengyi-3", "AI × 非遗", "承艺 3.0",
     ["可探索、可参与创作的非遗数字世界：", "八幕陶瓷篇章 + 3D 工作台 + AI 助手"],
     "JavaScript", "陶瓷篇初版", None),
    ("bilibili-promo", "交互叙事", "哔哩哔哩产品宣传页",
     ["整页就是一支 B 站视频：滚动即播放、", "章节即分 P，可发弹幕、选互动结局"],
     "JavaScript", None, "在线预览 ↗"),
    ("juanxincai-ai-site", "AI 服务", "卷心菜 · AI 工坊",
     ["AI 自由职业者个人站：首屏实时演示", "+ 可试玩的文案、Prompt、流程设计工具"],
     "JavaScript", None, None),
]

SANS = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',system-ui,-apple-system,'Segoe UI',sans-serif"
SERIF = "'Songti SC','STSong','Noto Serif SC','Source Han Serif SC','SimSun',serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
LANG_COLOR = {"TypeScript": "#3178C6", "JavaScript": "#F1E05A", "HTML": "#E34C26", "Python": "#3572A5"}

THEMES = {
    "light": dict(canvas="#F4F7FC", dot="#D3DCEA", node="#FFFFFF", node2="#F7F9FD", ink="#0E1A2F", ink2="#3C4A61",
                  muted="#7A879C", line="#DDE5F0", strong="#B9C6D8", accent="#1F5FE0", accent2="#4F8BFF",
                  soft="#E6EEFD", ok="#16A34A", warn="#D97706", warnsoft="#FDF1DC", teal="#0E9384", tealsoft="#DEF5F1",
                  rose="#D9406A", rosesoft="#FDE8EE", violet="#6D5BD0", violetsoft="#EEEBFB",
                  shadow="#0E1A2F", shadow_op="0.08"),
    "dark": dict(canvas="#0A1120", dot="#1C2840", node="#111A2C", node2="#0E1626", ink="#E7EEFA", ink2="#B6C3D8",
                 muted="#7D8AA1", line="#22304A", strong="#3A4D72", accent="#5B95FF", accent2="#8DB6FF",
                 soft="#16264A", ok="#34D399", warn="#FBBF24", warnsoft="#2A210C", teal="#2DD4BF", tealsoft="#0D2A27",
                 rose="#FB7199", rosesoft="#33141F", violet="#A495FF", violetsoft="#1F1B3D",
                 shadow="#000000", shadow_op="0.45"),
}
BUTTON_BLUE = "#1F5FE0"  # "联系我"标题栏和按钮在浅色 / 深色下都用同一个蓝
CAT_COLOR = {"AGENT": ("accent", "soft"), "SKILL": ("teal", "tealsoft"), "AI × 非遗": ("rose", "rosesoft"),
             "交互叙事": ("violet", "violetsoft"), "AI 服务": ("warn", "warnsoft")}

ICONS = {
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z" stroke-linejoin="round"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.5 2.5M15.2 15.2l2.5 2.5M6.3 17.7l2.5-2.5M15.2 8.8l2.5-2.5"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "flask": '<path d="M9 3h6M10 3v6L4.5 18.5A2 2 0 0 0 6.2 21.5h11.6a2 2 0 0 0 1.7-3L14 9V3"/><path d="M7 15h10"/>',
    "send": '<path d="M22 2 11 13"/><path d="m22 2-7 20-4-9-9-4z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "flag": '<path d="M5 21V4h11l-2 4 2 4H5"/>',
}


def tw(s, size, mono=False):
    """粗略估算文字宽度（中文按全角，其余按半角）"""
    return sum(size if ord(c) > 0x2E80 else size * (0.6 if mono else 0.56) for c in s)


def esc(s):
    return escape(str(s), quote=True)


def svg(w, h, body, label, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}"><style>text{{font-family:{SANS}}}.m{{font-family:{MONO}}}.s{{font-family:{SERIF}}}'
            f'.flow{{stroke-dasharray:3 9;animation:d 1s linear infinite}}@keyframes d{{to{{stroke-dashoffset:-12}}}}'
            f'.pulse{{animation:p 1.4s ease-in-out infinite}}@keyframes p{{50%{{opacity:.3}}}}'
            f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
            f'<defs>{defs}</defs>{"".join(body)}</svg>\n')


def shadow_def(t):
    return (f'<filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="8" '
            f'stdDeviation="12" flood-color="{t["shadow"]}" flood-opacity="{t["shadow_op"]}"/></filter>')


def icon(x, y, name, color, bg, size=28):
    k = size * 0.6 / 24
    off = size * 0.2
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.28:.0f}" fill="{bg}"/>'
            f'<g transform="translate({x + off:.1f} {y + off:.1f}) scale({k:.3f})" fill="none" stroke="{color}" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def node(x, y, w, h, t, head=None, stroke=None):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["node"]}" stroke="{stroke or t["line"]}" '
           f'stroke-width="1.5" filter="url(#sh)"/>']
    if head:
        out.append(f'<line x1="{x}" y1="{y + head}" x2="{x + w}" y2="{y + head}" stroke="{t["line"]}" stroke-width="1.5"/>')
    return "".join(out)


def port(x, y, t, filled=True):
    fill = t["accent"] if filled else t["node"]
    stroke = t["accent"] if filled else t["strong"]
    return f'<circle cx="{x}" cy="{y}" r="7" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'


def wire(x1, y1, x2, y2):
    dx = max(30, abs(x2 - x1) / 2)
    return f"M{x1} {y1} C{x1 + dx} {y1} {x2 - dx} {y2} {x2} {y2}"


# ---------------------------------------------------------------- 头图
def header(t):
    W, H = 1200, 440
    P = PROFILE
    CYCLE = "6s"  # 起止都是"运行完成"状态，不播放动画的环境也能看到完整画面
    defs = (shadow_def(t) +
            f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{t["dot"]}"/></pattern>'
            f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient>')
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="{t["canvas"]}"/>',
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="url(#dots)" stroke="{t["line"]}" stroke-width="1.5"/>']

    # 顶部元信息
    b.append(f'<text x="40" y="50" class="m" font-size="14" fill="{t["muted"]}">github.com/ZeroOnehub · profile.flow · '
             f'<tspan fill="{t["ok"]}">● 运行中</tspan></text>')
    b.append(f'<text x="{W - 40}" y="50" class="m" font-size="14" text-anchor="end" fill="{t["accent"]}">▶ 点击头图，打开个人网站</text>')

    # 连线
    outs_y = [96, 206, 316]
    o_h = 92
    edges = [wire(260, 234, 320, 234)] + [wire(840, 234, 900, y + o_h / 2) for y in outs_y]
    for d in edges:
        b.append(f'<path d="{d}" fill="none" stroke="{t["strong"]}" stroke-width="2"/>')
        b.append(f'<path d="{d}" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-linecap="round" class="flow"/>')

    # 触发器
    b.append(node(40, 164, 220, 140, t, head=44))
    b.append(f'<rect x="40" y="164" width="220" height="140" rx="14" fill="none" stroke="{t["warn"]}" stroke-width="2" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.35;0.39;0.49;1" dur="{CYCLE}" repeatCount="indefinite"/></rect>')
    b.append(icon(54, 172, "bolt", t["warn"], t["warnsoft"]))
    b.append(f'<text x="92" y="192" font-size="16" font-weight="600" fill="{t["ink"]}">触发器</text>')
    b.append(f'<text x="58" y="242" font-size="18" font-weight="600" fill="{t["ink"]}">有人打开了</text>')
    b.append(f'<text x="58" y="268" font-size="18" font-weight="600" fill="{t["ink"]}">我的 GitHub 主页</text>')
    b.append(f'<text x="58" y="292" class="m" font-size="13" fill="{t["warn"]}">on: profile_view</text>')

    # Agent 节点
    b.append(node(320, 84, 520, 300, t, head=44))
    b.append(f'<rect x="320" y="84" width="520" height="300" rx="14" fill="none" stroke="{t["accent"]}" stroke-width="2" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.469;0.47;0.67;0.671;1" dur="{CYCLE}" repeatCount="indefinite"/></rect>')
    b.append(icon(334, 92, "spark", t["accent"], t["soft"]))
    b.append(f'<text x="372" y="112" font-size="17" font-weight="600" fill="{t["ink"]}">{esc(P["role"])}</text>')
    b.append(f'<text x="820" y="111" class="m" font-size="13" text-anchor="end" fill="{t["muted"]}">Agent</text>')
    b.append(f'<text x="350" y="222" class="s" font-size="82" font-weight="900" letter-spacing="4" fill="{t["ink"]}">{esc(P["name"])}</text>')
    b.append(f'<rect x="736" y="148" width="80" height="80" rx="18" fill="url(#g)"/>'
             f'<text x="776" y="202" class="s" font-size="42" font-weight="900" text-anchor="middle" fill="#FFFFFF">{esc(P["seal"])}</text>')
    b.append(f'<text x="352" y="270" font-size="24" font-weight="700" fill="{t["ink"]}">{esc(P["tagline"])}</text>')
    x = 352
    for tag in P["tags"]:
        w = tw(tag, 15) + 22
        b.append(f'<rect x="{x}" y="288" width="{w:.0f}" height="30" rx="7" fill="{t["soft"]}"/>'
                 f'<text x="{x + w / 2:.0f}" y="308" font-size="15" font-weight="600" text-anchor="middle" fill="{t["accent"]}">{esc(tag)}</text>')
        x += w + 8
    b.append(f'<line x1="320" y1="336" x2="840" y2="336" stroke="{t["line"]}" stroke-width="1.5"/>')
    b.append(f'<rect x="352" y="356" width="300" height="6" rx="3" fill="{t["line"]}"/>')
    b.append(f'<rect x="352" y="356" width="300" height="6" rx="3" fill="url(#g)">'
             f'<animate attributeName="width" values="300;300;0;300;300" keyTimes="0;0.469;0.47;0.67;1" dur="{CYCLE}" repeatCount="indefinite"/></rect>')
    b.append(f'<text x="820" y="364" class="m" font-size="14" text-anchor="end" fill="{t["accent"]}" opacity="0">生成主页中…'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.469;0.47;0.67;0.671;1" dur="{CYCLE}" repeatCount="indefinite"/></text>')
    b.append(f'<text x="820" y="364" class="m" font-size="14" text-anchor="end" fill="{t["ok"]}">✓ 成功 · 1.65s'
             f'<animate attributeName="opacity" values="1;1;0;0;1;1" keyTimes="0;0.469;0.47;0.67;0.671;1" dur="{CYCLE}" repeatCount="indefinite"/></text>')

    # 输出节点
    outs = [("输出 · 项目", f"{len(PROJECTS)} 个项目", "向下滚动查看"),
            ("输出 · 网站", "个人网站", P["site"]),
            ("输出 · 联系", "联系我", P["email"])]
    for (typ, title, sub), y in zip(outs, outs_y):
        b.append(node(900, y, 260, o_h, t, head=34))
        b.append(f'<text x="916" y="{y + 23}" font-size="13" fill="{t["muted"]}">{esc(typ)}</text>')
        b.append(f'<text x="916" y="{y + 61}" font-size="19" font-weight="700" fill="{t["ink"]}">{esc(title)}</text>')
        b.append(f'<text x="1142" y="{y + 61}" font-size="19" text-anchor="end" fill="{t["accent"]}">→</text>')
        b.append(f'<text x="916" y="{y + 81}" font-size="13" fill="{t["muted"]}">{esc(sub)}</text>')

    # 端口
    for px, py in [(260, 234), (320, 234), (840, 234)] + [(900, y + o_h / 2) for y in outs_y]:
        b.append(port(px, py, t))

    # 数据包
    def packet(d, times, points, op_vals, op_times):
        return (f'<g opacity="0"><circle r="13" fill="{t["accent"]}" opacity="0.18"/><circle r="6" fill="{t["accent"]}"/>'
                f'<animateMotion path="{d}" keyPoints="{points}" keyTimes="{times}" calcMode="linear" dur="{CYCLE}" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="{op_vals}" keyTimes="{op_times}" dur="{CYCLE}" repeatCount="indefinite"/></g>')
    b.append(packet(edges[0], "0;0.35;0.47;1", "0;0;1;1", "0;0;1;1;0;0", "0;0.349;0.35;0.47;0.471;1"))
    for d in edges[1:]:
        b.append(packet(d, "0;0.67;0.8;1", "0;0;1;1", "0;0;1;1;0;0", "0;0.669;0.67;0.8;0.801;1"))

    label = f'{P["name"]} · {P["role"]} · {P["tagline"]}。点击打开个人网站 {P["site"]}'
    return svg(W, H, b, label, defs)


# ---------------------------------------------------------------- 板块标题
SECTIONS = [
    ("projects", "layers", "项目", "Group · #01", f"{len(PROJECTS)} 个节点", f"✓ {len(PROJECTS)} / {len(PROJECTS)} 已公开", False),
    ("now", "flask", "正在研究", "Loop · #02", "每周更新", f"↻ 更新于 {UPDATED}", False),
    ("contact", "send", "联系我", "Output · #03", "最终输出", "✓ 欢迎来信", True),
]


def section(sec, t):
    _, ico, title, typ, count, status, solid = sec
    W, H = 1200, 104
    b = [f'<line x1="600" y1="0" x2="600" y2="34" stroke="{t["strong"]}" stroke-width="2"/>',
         f'<line x1="600" y1="0" x2="600" y2="34" stroke="{t["accent"]}" stroke-width="2" class="flow"/>']
    fill = BUTTON_BLUE if solid else t["node"]
    fg, fg2 = ("#FFFFFF", "#FFFFFF") if solid else (t["ink"], t["muted"])
    b.append(f'<rect x="1" y="40" width="{W - 2}" height="62" rx="14" fill="{fill}" stroke="{BUTTON_BLUE if solid else t["line"]}" stroke-width="1.5"/>')
    b.append(icon(22, 57, ico, "#FFFFFF" if solid else t["accent"], "rgba(255,255,255,.18)" if solid else t["soft"]))
    b.append(f'<text x="64" y="79" font-size="22" font-weight="700" fill="{fg}">{esc(title)}</text>')
    x = 64 + tw(title, 22) + 14
    pw = tw(typ, 13, mono=True) + 16
    b.append(f'<rect x="{x:.0f}" y="60" width="{pw:.0f}" height="24" rx="6" fill="none" stroke="{"rgba(255,255,255,.45)" if solid else t["line"]}" stroke-width="1.2"/>'
             f'<text x="{x + 8:.0f}" y="77" class="m" font-size="13" fill="{fg2}">{esc(typ)}</text>')
    b.append(f'<text x="{x + pw + 12:.0f}" y="78" font-size="15" fill="{fg2}">{esc(count)}</text>')
    b.append(f'<text x="{W - 24}" y="78" class="m" font-size="14" text-anchor="end" fill="{"#FFFFFF" if solid else t["ok"]}">{esc(status)}</text>')
    b.append(port(600, 40, t))
    return svg(W, H, b, f"{title}")


# ---------------------------------------------------------------- 项目卡片
def card(p, t):
    slug, cat, name, desc, lang, status, demo = p
    W, H = 600, 236
    c, cs = (t[k] for k in CAT_COLOR.get(cat, ("accent", "soft")))
    defs = (f'<linearGradient id="hg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{cs}"/>'
            f'<stop offset="0.85" stop-color="{cs}" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="top"><rect x="9" y="1" width="{W - 18}" height="60"/></clipPath>')
    b = [f'<rect x="9" y="1" width="{W - 18}" height="{H - 2}" rx="14" fill="{t["node"]}" stroke="{t["line"]}" stroke-width="1.5"/>',
         f'<g clip-path="url(#top)"><rect x="10" y="2" width="{W - 20}" height="70" rx="13" fill="url(#hg)"/></g>',
         f'<line x1="9" y1="60" x2="{W - 9}" y2="60" stroke="{t["line"]}" stroke-width="1.5"/>',
         f'<text x="32" y="37" class="m" font-size="14" font-weight="600" letter-spacing="1.5" fill="{c}">{esc(cat)}</text>']
    chip = status or ("已上线" if demo else "开源")
    chip_c = t["warn"] if status else t["ok"]
    cw = tw(chip, 14)
    pulse = ' class="pulse"' if status else ""
    b.append(f'<circle cx="{W - 32 - cw - 12:.0f}" cy="32" r="4.5" fill="{chip_c}"{pulse}/>'
             f'<text x="{W - 32}" y="37" font-size="14" text-anchor="end" fill="{chip_c}">{esc(chip)}</text>')
    b.append(f'<text x="32" y="106" font-size="27" font-weight="700" fill="{t["ink"]}">{esc(name)}</text>')
    for i, line in enumerate(desc):
        b.append(f'<text x="32" y="{144 + i * 28}" font-size="19" fill="{t["ink2"]}">{esc(line)}</text>')
    b.append(f'<line x1="9" y1="{H - 50}" x2="{W - 9}" y2="{H - 50}" stroke="{t["line"]}" stroke-width="1.5" stroke-dasharray="4 5"/>')
    b.append(f'<circle cx="38" cy="{H - 25}" r="6" fill="{LANG_COLOR.get(lang, t["muted"])}"/>'
             f'<text x="52" y="{H - 19}" font-size="15" fill="{t["muted"]}">{esc(lang)}</text>')
    b.append(f'<text x="{W - 32}" y="{H - 19}" font-size="15" font-weight="600" text-anchor="end" fill="{c}">{esc(demo or "查看源码 ↗")}</text>')
    b.append(f'<circle cx="9" cy="31" r="6" fill="{t["node"]}" stroke="{t["strong"]}" stroke-width="2.2"/>'
             f'<circle cx="{W - 9}" cy="31" r="6" fill="{c}" stroke="{c}" stroke-width="2.2"/>')
    return svg(W, H, b, f'{name}：{"".join(desc)}', defs)


# ---------------------------------------------------------------- 正在研究
def now(t):
    W = 1200
    row_h = 66
    H = 28 + row_h * len(NOW) + 52
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{t["node"]}" stroke="{t["line"]}" stroke-width="1.5"/>']
    for i, (title, note) in enumerate(NOW):
        y = 28 + i * row_h
        b.append(f'<text x="32" y="{y + 40}" class="m" font-size="15" fill="{t["accent"]}">#{i + 1:02d}</text>')
        b.append(f'<text x="96" y="{y + 40}" font-size="21" font-weight="700" fill="{t["ink"]}">{esc(title)}</text>')
        b.append(f'<text x="560" y="{y + 40}" font-size="18" fill="{t["ink2"]}">{esc(note)}</text>')
        b.append(f'<line x1="32" y1="{y + row_h}" x2="{W - 32}" y2="{y + row_h}" stroke="{t["line"]}" stroke-width="1.2"/>')
    b.append(f'<text x="32" y="{H - 20}" class="m" font-size="13" fill="{t["muted"]}">更新于 {UPDATED} · 每周更新</text>')
    return svg(W, H, b, "这两周在研究：" + "；".join(f"{a}：{c}" for a, c in NOW))


# ---------------------------------------------------------------- 联系按钮
def button(ico, label, sub, arrow, t):
    W, H = 580, 96
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{BUTTON_BLUE}"/>',
         icon(24, 22, ico, "#FFFFFF", "rgba(255,255,255,.18)", size=52),
         f'<text x="96" y="49" font-size="23" font-weight="700" fill="#FFFFFF">{esc(label)}</text>',
         f'<text x="96" y="75" class="m" font-size="15" fill="#FFFFFF" opacity="0.85">{esc(sub)}</text>',
         f'<text x="{W - 30}" y="60" font-size="28" text-anchor="end" fill="#FFFFFF">{arrow}</text>']
    return svg(W, H, b, f"{label} {sub}")


# ---------------------------------------------------------------- 页脚
def footer(t):
    W, H = 1200, 150
    text = "流程结束 · 感谢浏览"
    pw = tw(text, 16, mono=True) + 64
    b = [f'<line x1="600" y1="0" x2="600" y2="50" stroke="{t["strong"]}" stroke-width="2"/>',
         f'<line x1="600" y1="0" x2="600" y2="50" stroke="{t["accent"]}" stroke-width="2" class="flow"/>',
         f'<rect x="{600 - pw / 2:.0f}" y="50" width="{pw:.0f}" height="46" rx="23" fill="{t["node"]}" stroke="{t["ok"]}" stroke-opacity="0.5" stroke-width="1.5"/>',
         f'<g transform="translate({600 - pw / 2 + 24:.0f} 64) scale(0.75)" fill="none" stroke="{t["ok"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ICONS["flag"]}</g>',
         f'<text x="{600 + 12}" y="79" class="m" font-size="16" text-anchor="middle" fill="{t["ok"]}">{text}</text>',
         port(600, 50, t),
         f'<text x="600" y="134" font-size="14" text-anchor="middle" fill="{t["muted"]}">© 2026 {esc(PROFILE["name"])} · 在个人网站点 ▶ 运行，可以把这条工作流完整跑一遍</text>']
    return svg(W, H, b, "流程结束，感谢浏览")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for mode, t in THEMES.items():
        (OUT / f"header-{mode}.svg").write_text(header(t), encoding="utf-8")
        for sec in SECTIONS:
            (OUT / f"sec-{sec[0]}-{mode}.svg").write_text(section(sec, t), encoding="utf-8")
        for p in PROJECTS:
            (OUT / f"card-{p[0]}-{mode}.svg").write_text(card(p, t), encoding="utf-8")
        (OUT / f"now-{mode}.svg").write_text(now(t), encoding="utf-8")
        (OUT / f"footer-{mode}.svg").write_text(footer(t), encoding="utf-8")
    t = THEMES["light"]
    (OUT / "btn-site.svg").write_text(button("globe", "个人网站", PROFILE["site"], "↗", t), encoding="utf-8")
    (OUT / "btn-mail.svg").write_text(button("mail", "发邮件", PROFILE["email"], "→", t), encoding="utf-8")
    print("done:", len(list(OUT.glob("*.svg"))), "files")
