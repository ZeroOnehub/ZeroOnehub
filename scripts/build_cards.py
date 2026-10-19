"""生成主页项目卡片（每张浅色 / 深色两版）：python3 scripts/build_cards.py

改项目：编辑下面的 PROJECTS（最多 6 个），重新运行，再同步 README 里的链接。
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = ("'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',"
        "system-ui,-apple-system,'Segoe UI',sans-serif")
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

LANG_COLOR = {"TypeScript": "#3178C6", "JavaScript": "#F1E05A", "HTML": "#E34C26", "Python": "#3572A5"}

# slug, 分类, 名称, 两行描述, 语言, 状态, 是否公开, 在线演示文字
PROJECTS = [
    ("aipm-workbench", "AGENT", "AIPM 工坊",
     ["基于 DeepSeek Harness 二次开发的", "个人 AI 产品经理工作台，按阶段推进项目"],
     "TypeScript", "进行中", True, None),
    ("aipm-skills", "SKILL", "AIPM Skills",
     ["产品经理全流程 Skill 合集：总控分派", "+ 六站立项教练，PRD / 评测陆续接入"],
     "HTML", "进行中", True, None),
    ("chengyi", "AI × 非遗", "承艺 · 山河入坊",
     ["非遗数字手作交互原型：青绿山水地图", "+ 陶瓷剪纸手作，大模型讲解非遗"],
     "JavaScript", None, True, "在线体验 ↗"),
    ("chengyi-3", "AI × 非遗", "承艺 3.0",
     ["可探索、可参与创作的非遗数字世界：", "八幕陶瓷篇章 + 3D 工作台 + AI 助手"],
     "JavaScript", "陶瓷篇初版", True, None),
    ("bilibili-promo", "交互叙事", "哔哩哔哩产品宣传页",
     ["整页就是一支 B 站视频：滚动即播放、", "章节即分 P，可发弹幕、选互动结局"],
     "JavaScript", None, True, "在线预览 ↗"),
    ("juanxincai-ai-site", "AI 服务", "卷心菜 · AI 工坊",
     ["AI 自由职业者个人站：首屏实时演示", "+ 可试玩的文案、Prompt、流程设计工具"],
     "JavaScript", None, False, None),
]

THEMES = {
    "light": dict(bg="#FFFFFF", border="#D1D9E0", title="#1F2328", body="#59636E", faint="#818B98",
                  accent="#0E9F8E", link="#0969DA"),
    "dark": dict(bg="#0D1117", border="#3D444D", title="#F0F6FC", body="#9198A1", faint="#7D8590",
                 accent="#2DD4BF", link="#4493F8"),
}


def tw(s, size, mono=False):
    return sum(size if ord(c) > 0x2E80 else size * (0.6 if mono else 0.56) for c in s)


def card(p, t):
    slug, cat, name, desc, lang, status, public, demo = p
    W, H = 600, 216
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>']
    b.append(f'<text x="32" y="48" class="m" font-size="14" letter-spacing="2" fill="{t["accent"]}">{cat}</text>')
    vis = "Public" if public else "Private"
    vw = tw(vis, 14) + 22
    b.append(f'<rect x="{W - 32 - vw:.0f}" y="30" width="{vw:.0f}" height="26" rx="13" fill="none" stroke="{t["border"]}"/>'
             f'<text x="{W - 32 - vw/2:.0f}" y="48" font-size="14" text-anchor="middle" fill="{t["faint"]}">{vis}</text>')
    b.append(f'<text x="32" y="92" font-size="26" font-weight="600" fill="{t["title"]}">{name}</text>')
    for i, line in enumerate(desc):
        b.append(f'<text x="32" y="{130 + i*28}" font-size="19" fill="{t["body"]}">{line}</text>')
    b.append(f'<circle cx="38" cy="{H - 30}" r="6" fill="{LANG_COLOR.get(lang, t["faint"])}"/>')
    foot = lang + (f"　·　{status}" if status else "")
    b.append(f'<text x="52" y="{H - 24}" font-size="16" fill="{t["faint"]}">{foot}</text>')
    if demo:
        b.append(f'<text x="{W - 32}" y="{H - 24}" font-size="16" font-weight="600" text-anchor="end" fill="{t["link"]}">{demo}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{name}：{"".join(desc)}">'
            f'<style>text{{font-family:{SANS}}}.m{{font-family:{MONO}}}</style>{"".join(b)}</svg>\n')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for p in PROJECTS:
        for name, theme in THEMES.items():
            (OUT / f"card-{p[0]}-{name}.svg").write_text(card(p, theme), encoding="utf-8")
