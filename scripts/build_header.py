"""生成主页头图（浅色 / 深色两版）：python3 scripts/build_header.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = ("'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',"
        "system-ui,-apple-system,'Segoe UI',sans-serif")
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# (中文名, skill id, 状态)  done / current / gate / todo
PIPELINE = [
    ("立项", "project-initiation", "done"),
    ("PRD", "prd", "done"),
    ("原型", "prototype", "current"),
    ("人来拍板", "human-gate", "gate"),
    ("评测", "evaluation", "todo"),
    ("上线", "launch", "todo"),
]

THEMES = {
    "light": dict(bg="#F7FAF9", border="#E1E8E6", title="#1F2328", body="#57606A", faint="#8C959F",
                  line="#D8E0DE", accent="#0E9F8E", accent_soft="#D5F0EB"),
    "dark": dict(bg="#151B23", border="#2A313C", title="#E6EDF3", body="#9DA7B3", faint="#6E7781",
                 line="#2F3742", accent="#2DD4BF", accent_soft="#123A37"),
}


def header(t):
    W, H = 1200, 400
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="2"/>']

    # 左：身份
    x = 72
    b.append(f'<text x="{x}" y="112" class="m" font-size="16" letter-spacing="4" fill="{t["accent"]}">AI PRODUCT MANAGER</text>')
    b.append(f'<text x="{x}" y="174" font-size="46" font-weight="600" fill="{t["title"]}">樊烨'
             f'<tspan dx="16" font-size="24" font-weight="400" fill="{t["faint"]}">Fan Ye</tspan></text>')
    b.append(f'<text x="{x}" y="236" font-size="23" fill="{t["body"]}">把岗位工作流拆成可复用的 Skill，</text>')
    b.append(f'<text x="{x}" y="272" font-size="23" fill="{t["body"]}">在关键节点把决定权留给人。</text>')
    b.append(f'<text x="{x}" y="330" font-size="17" fill="{t["faint"]}">Agent 工作流　·　DeepSeek Harness　·　Human-in-the-loop</text>')

    # 分隔线
    b.append(f'<line x1="700" y1="64" x2="700" y2="336" stroke="{t["line"]}" stroke-width="1.5"/>')

    # 右：工作流步骤
    rx, top, step = 764, 104, 44
    b.append(f'<text x="{rx - 12}" y="76" class="m" font-size="14" letter-spacing="1" fill="{t["faint"]}">aipm-hub / pipeline</text>')
    n = len(PIPELINE)
    done_until = max(i for i, p in enumerate(PIPELINE) if p[2] in ("done", "current"))
    b.append(f'<line x1="{rx}" y1="{top}" x2="{rx}" y2="{top + step*(n-1)}" stroke="{t["line"]}" stroke-width="2"/>')
    b.append(f'<line x1="{rx}" y1="{top}" x2="{rx}" y2="{top + step*done_until}" stroke="{t["accent"]}" stroke-width="2"/>')
    for i, (zh, sid, st) in enumerate(PIPELINE):
        y = top + step * i
        if st == "done":
            b.append(f'<circle cx="{rx}" cy="{y}" r="7" fill="{t["accent"]}"/>')
        elif st == "current":
            b.append(f'<circle cx="{rx}" cy="{y}" r="12" fill="{t["accent_soft"]}"/>'
                     f'<circle cx="{rx}" cy="{y}" r="6" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="2.5"/>')
        elif st == "gate":
            b.append(f'<circle cx="{rx}" cy="{y}" r="7" fill="{t["bg"]}" stroke="{t["faint"]}" stroke-width="1.8" stroke-dasharray="3 3"/>')
        else:
            b.append(f'<circle cx="{rx}" cy="{y}" r="6" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="2"/>')
        strong = st in ("done", "current")
        b.append(f'<text x="{rx + 30}" y="{y + 7}" font-size="19" font-weight="{600 if st == "current" else 400}" '
                 f'fill="{t["title"] if strong else t["faint"]}">{zh}</text>')
        b.append(f'<text x="1128" y="{y + 6}" class="m" font-size="14" text-anchor="end" '
                 f'fill="{t["accent"] if st == "current" else t["faint"]}">{sid}</text>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="樊烨 Fan Ye · AI 产品经理：把岗位工作流拆成可复用的 Skill，在关键节点把决定权留给人。">'
            f'<style>text{{font-family:{SANS}}}.m{{font-family:{MONO}}}</style>{"".join(b)}</svg>\n')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(theme), encoding="utf-8")
