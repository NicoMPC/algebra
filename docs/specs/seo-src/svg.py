def graph(f, xmin, xmax, ymin, ymax, label, points=(), marks=(), unit=34, name='f'):
    """SVG d'une courbe sur quadrillage. points = [(x,y,'texte')] ; marks = pointillés [(x,y)]."""
    pad = 22
    W = (xmax - xmin) * unit + 2 * pad
    H = (ymax - ymin) * unit + 2 * pad
    X = lambda x: pad + (x - xmin) * unit
    Y = lambda y: pad + (ymax - y) * unit
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px;display:block;margin:0 auto 1rem;background:#fff;border:1px solid #E2E8F0;border-radius:12px" role="img" aria-label="{label}">']
    for x in range(xmin, xmax + 1):
        s.append(f'<line x1="{X(x)}" y1="{Y(ymin)}" x2="{X(x)}" y2="{Y(ymax)}" stroke="#E2E8F0" stroke-width="1"/>')
    for y in range(ymin, ymax + 1):
        s.append(f'<line x1="{X(xmin)}" y1="{Y(y)}" x2="{X(xmax)}" y2="{Y(y)}" stroke="#E2E8F0" stroke-width="1"/>')
    s.append(f'<line x1="{X(xmin)}" y1="{Y(0)}" x2="{X(xmax)}" y2="{Y(0)}" stroke="#475569" stroke-width="1.5"/>')
    s.append(f'<line x1="{X(0)}" y1="{Y(ymin)}" x2="{X(0)}" y2="{Y(ymax)}" stroke="#475569" stroke-width="1.5"/>')
    s.append(f'<text x="{X(1)-3}" y="{Y(0)+15}" font-size="12" fill="#475569" paint-order="stroke" stroke="#fff" stroke-width="3">1</text>')
    s.append(f'<text x="{X(0)-12}" y="{Y(1)+4}" font-size="12" fill="#475569" paint-order="stroke" stroke="#fff" stroke-width="3">1</text>')
    s.append(f'<text x="{X(0)-12}" y="{Y(0)+15}" font-size="12" fill="#475569" paint-order="stroke" stroke="#fff" stroke-width="3">0</text>')
    for (x, y) in marks:
        s.append(f'<path d="M{X(x)} {Y(0)} V{Y(y)} H{X(0)}" fill="none" stroke="#1E40AF" stroke-width="1.5" stroke-dasharray="4 3"/>')
    pts = []
    n = 200
    for i in range(n + 1):
        x = xmin + (xmax - xmin) * i / n
        y = f(x)
        if ymin - 0.5 <= y <= ymax + 0.5:
            pts.append(f'{X(x):.1f},{Y(y):.1f}')
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#059669" stroke-width="2.5"/>')
    for (x, y, t) in points:
        s.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="4" fill="#1E40AF"/><text x="{X(x)+7}" y="{Y(y)-7}" font-size="13" font-weight="700" fill="#0F172A" paint-order="stroke" stroke="#fff" stroke-width="4">{t}</text>')
    s.append('</svg>')
    return ''.join(s)
