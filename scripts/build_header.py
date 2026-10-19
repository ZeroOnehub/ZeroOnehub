"""生成主页头图（浅色 / 深色两版）：python3 scripts/build_header.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = ("'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',"
        "system-ui,-apple-system,'Segoe UI',sans-serif")
ACCENT = "#14B8A6"
STEPS = ["立项", "PRD", "原型", "确认", "评测", "上线"]
GATE = 3  # 人工确认节点画成空心圆


def tw(s, size):
    return sum(size if ord(c) > 0x2E80 else size * 0.56 for c in s)


def header(dark):
    fg, sub, faint = ("#E6EDF3", "#8B949E", "#30363D") if dark else ("#1F2328", "#656D76", "#D0D7DE")
    W, H = 1200, 330
    name, en = "樊烨", "Fan Ye"
    gap = 20
    total = tw(name, 76) + gap + tw(en, 32)
    x0 = (W - total) / 2
    b = [
        f'<text x="{x0:.0f}" y="132" font-size="76" font-weight="600" fill="{fg}">{name}</text>',
        f'<text x="{x0 + tw(name, 76) + gap:.0f}" y="132" font-size="32" font-weight="300" fill="{sub}">{en}</text>',
        f'<text x="600" y="190" font-size="26" fill="{sub}" text-anchor="middle" letter-spacing="2">'
        f'AI 产品经理  ·  Agent 工作流</text>',
    ]
    step, y = 76, 252
    sx = 600 - step * (len(STEPS) - 1) / 2
    b.append(f'<line x1="{sx}" y1="{y}" x2="{sx + step * (len(STEPS) - 1)}" y2="{y}" stroke="{faint}" stroke-width="1.5"/>')
    for i, s in enumerate(STEPS):
        cx = sx + step * i
        if i == GATE:
            b.append(f'<circle cx="{cx}" cy="{y}" r="6" fill="{"#0D1117" if dark else "#FFFFFF"}" stroke="{ACCENT}" stroke-width="2"/>')
        else:
            b.append(f'<circle cx="{cx}" cy="{y}" r="5" fill="{ACCENT}"/>')
        b.append(f'<text x="{cx}" y="{y + 34}" font-size="15" fill="{sub}" text-anchor="middle">{s}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="樊烨 Fan Ye · AI 产品经理 · Agent 工作流">'
            f'<style>text{{font-family:{SANS}}}</style>{"".join(b)}</svg>\n')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "header-light.svg").write_text(header(False), encoding="utf-8")
    (OUT / "header-dark.svg").write_text(header(True), encoding="utf-8")
