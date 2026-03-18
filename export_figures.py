#!/usr/bin/env python3
"""
Export tous les exercices avec figure géométrique.
Génère : audit_figures.md + audit_figures.html (importable Google Docs)
Les figures SVG sont rendues exactement comme dans l'app.
"""

import json, re, math
from sheets import sh

# ══════════════════════════════════════════════════════════════
# AUTO-DÉTECTION (port Python de autoDetectFigure JS)
# ══════════════════════════════════════════════════════════════

NON_GEO = re.compile(r'calcul_litt|fraction|statistiq|probabilit|nombre|puissance|algorith|suite|exponent|variable_al|probabilites_cond|notation_sci', re.I)

def auto_detect_figure(q, cat):
    if not q or not cat:
        return None
    t = (q + ' ' + cat).lower().replace('$','').replace('{,}','.').replace('\\,','')
    nums_raw = re.findall(r'\d+(?:[.,]\d+)?', t)
    n = [float(x.replace(',','.')) for x in nums_raw] if nums_raw else []

    if NON_GEO.search(cat):
        return None
    if re.search(r'cercle\s*trigono', t, re.I) and not re.search(r'trigono', cat, re.I):
        return None
    if re.search(r'triangle\s*de\s*pascal|inégalité\s*triangulaire', t, re.I) and not re.search(r'triangle|géomét|pythagore', cat, re.I):
        return None
    if re.search(r'python|algorithme|boucle\b|liste\b', t, re.I) and re.search(r'algorith', cat, re.I):
        return None

    # Points
    pts = []
    pt_match = re.findall(r'\b([A-Z])\b(?!\')', q)
    for p in pt_match:
        if p not in pts and (p not in ('I','J','L','O') or re.search(r'triangle|cercle|carré', q, re.I)):
            pts.append(p)

    # Triangle rectangle
    if re.search(r'triangle\s*rectangle|pythagore|hypoténuse', t, re.I):
        a,b = (n[0] if len(n)>0 else 3), (n[1] if len(n)>1 else 4)
        c = n[2] if len(n)>2 else None
        if re.search(r'prouver|montrer|démontrer|vérifier.*rectangle', t, re.I):
            return {'type':'triangle','a':a,'b':b,'c':c or 5,'cat':cat,'pts':pts}
        return {'type':'tri_rect','a':a,'b':b,'c':c,'cat':cat,'pts':pts}
    if re.search(r'trigono|sin\b|cos\b|tan\b|adjacent|opposé|angle.*triangle', t, re.I) and not re.search(r'théorème.*thalès', t, re.I):
        angle = None
        for x in n:
            if 10 < x < 90: angle = x
        return {'type':'tri_trigo','angle':angle or 35,'a':n[0] if n else 5,'b':n[1] if len(n)>1 else None,'cat':cat,'pts':pts}
    if re.search(r'thalès', t, re.I):
        if not re.search(r'droite|parallèle|point|triangle', t, re.I) and len(n)<2:
            return None
        return {'type':'thales','a':n[0] if n else 4,'b':n[1] if len(n)>1 else 6,'c':n[2] if len(n)>2 else 3,'d':n[3] if len(n)>3 else None,'cat':cat,'pts':pts}
    if re.search(r'cercle|rayon|diamètre|disque', t, re.I) and not re.search(r'demi.cercle', t, re.I):
        if re.search(r'cercle\s*trigono', t, re.I): return None
        r = n[0] if n else 5
        if re.search(r'diamètre', t, re.I) and r>2: r=r/2
        conf = 'high' if n else 'low'
        return {'type':'circle','r':r,'cat':cat,'pts':pts,'confidence':conf}
    if re.search(r'rectangle|longueur.*largeur|largeur.*longueur', t, re.I):
        return {'type':'rect','w':n[0] if n else 8,'h':n[1] if len(n)>1 else (n[0] if n else 5),'square':False,'cat':cat,'pts':pts}
    if re.search(r'carré|côté.*carré', t, re.I) and not re.search(r'racine', t, re.I):
        s = n[0] if n else 5
        return {'type':'rect','w':s,'h':s,'square':True,'cat':cat,'pts':pts}
    if re.search(r'angle|mesure.*°|degrés', t, re.I) and re.search(r'angle', cat, re.I):
        deg=None
        for v in n:
            if 5<v<180: deg=v
        if not deg and re.search(r'calcul|trouv|détermin', t, re.I): return None
        return {'type':'angle','deg':deg or 60,'cat':cat,'pts':pts}
    if re.search(r'parallèle|perpendiculaire', t, re.I) and re.search(r'géomét', cat, re.I):
        return {'type':'parallel','perp':bool(re.search(r'perpendiculaire', t, re.I)),'cat':cat,'pts':pts}
    if re.search(r'symétrie\s*axiale|axe\s*de\s*symétrie', t, re.I):
        return {'type':'sym_axial','cat':cat,'pts':pts}
    if re.search(r'symétrie\s*centrale|centre\s*de\s*symétrie', t, re.I):
        return {'type':'sym_central','cat':cat,'pts':pts}
    if re.search(r'cube|pavé|parallélépipède', t, re.I):
        return {'type':'cube','a':n[0] if n else 4,'b':n[1] if len(n)>1 else (n[0] if n else 3),'c':n[2] if len(n)>2 else (n[0] if n else 2),'isCube':bool(re.search(r'cube', t, re.I)),'cat':cat,'pts':pts}
    if re.search(r'cylindre', t, re.I):
        return {'type':'cylinder','r':n[0] if n else 3,'h':n[1] if len(n)>1 else 6,'cat':cat,'pts':pts}
    if re.search(r'cône', t, re.I):
        return {'type':'cone','r':n[0] if n else 3,'h':n[1] if len(n)>1 else 6,'cat':cat,'pts':pts}
    if re.search(r'pyramide', t, re.I):
        return {'type':'pyramid','a':n[0] if n else 4,'h':n[1] if len(n)>1 else 6,'cat':cat,'pts':pts}
    if re.search(r'sphère|boule', t, re.I):
        return {'type':'sphere','r':n[0] if n else 4,'cat':cat,'pts':pts}
    if re.search(r'section', t, re.I) and re.search(r'solide|section', cat, re.I):
        return {'type':'section_solid','cat':cat,'pts':pts}
    if re.search(r'homothétie|agrandissement|réduction|rapport.*k|k\s*=', t, re.I):
        k=None
        for v in n:
            if 0<v<10 and v!=1: k=v
        return {'type':'homothety','k':k or 2,'cat':cat,'pts':pts}
    if re.search(r'semblable|similaire', t, re.I):
        return {'type':'similar_tri','a':n[0] if n else 3,'b':n[1] if len(n)>1 else 4,'c':n[2] if len(n)>2 else 5,'cat':cat,'pts':pts}
    if re.search(r'périmètre|aire|surface', t, re.I) and n:
        if re.search(r'triangle', t, re.I):
            return {'type':'triangle','a':n[0] if n else 5,'b':n[1] if len(n)>1 else 4,'c':n[2] if len(n)>2 else 6,'cat':cat,'pts':pts}
    if re.search(r'volume', t, re.I) and not re.search(r'cube|pavé|cylindre|cône|pyramide|sphère', t, re.I):
        return {'type':'cube','a':n[0] if n else 4,'b':n[1] if len(n)>1 else 3,'c':n[2] if len(n)>2 else 2,'isCube':False,'cat':cat,'pts':pts,'confidence':'low'}
    if re.search(r'translation|rotation', t, re.I):
        return {'type':'transform','isRotation':bool(re.search(r'rotation', t, re.I)),'cat':cat,'pts':pts}
    if re.search(r'produit\s*scalaire|vecteur.*orthogon|orthogon.*vecteur', t, re.I) and re.search(r'produit_scal', cat, re.I):
        return {'type':'vectors','pts':pts,'cat':cat}
    if re.search(r'équation.*droite|droite.*équation|équation.*cercle|repère', t, re.I) and re.search(r'geometrie_repere', cat, re.I):
        return {'type':'repere','pts':pts,'cat':cat}
    if re.search(r'cercle\s*trigono|cos.*[θα]|sin.*[θα]|valeur.*remarquable.*cos|valeur.*remarquable.*sin', t, re.I) and re.search(r'trigono', cat, re.I):
        return {'type':'trigo_circle','pts':pts,'cat':cat}
    return None

# ══════════════════════════════════════════════════════════════
# RENDER FIG → SVG (port Python de renderFig JS)
# ══════════════════════════════════════════════════════════════

def render_fig(fig):
    if not fig: return ''
    W,H = 280,210
    t = fig.get('type','')
    pts = fig.get('pts',[])

    def p(i, default=''):
        return pts[i] if i < len(pts) else default

    if t == 'tri_rect':
        ax,ay,bx,by,cx,cy = 40,170,220,170,40,40
        sa,sb,sc = fig.get('a',3),fig.get('b',4),fig.get('c')
        p0,p1,p2 = p(0,'A'),p(1,'B'),p(2,'C')
        sc_txt = f'<text x="{(bx+cx)//2+14}" y="{(by+cy)//2}" class="geo-val">{sc}</text>' if sc else f'<text x="{(bx+cx)//2+14}" y="{(by+cy)//2}" class="geo-unknown">?</text>'
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<polygon points="{ax},{ay} {bx},{by} {cx},{cy}" class="geo-fill"/>
<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" class="geo-line"/><line x1="{bx}" y1="{by}" x2="{cx}" y2="{cy}" class="geo-line"/><line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" class="geo-line"/>
<rect x="{ax}" y="{ay-16}" width="16" height="16" class="geo-right"/>
<circle cx="{ax}" cy="{ay}" class="geo-dot"/><circle cx="{bx}" cy="{by}" class="geo-dot"/><circle cx="{cx}" cy="{cy}" class="geo-dot"/>
<text x="{ax-8}" y="{ay+16}" class="geo-label">{p0}</text><text x="{bx+6}" y="{by+16}" class="geo-label">{p1}</text><text x="{cx-12}" y="{cy-8}" class="geo-label">{p2}</text>
<text x="{(ax+bx)//2}" y="{ay+18}" text-anchor="middle" class="geo-val">{sa}</text>
<text x="{ax-18}" y="{(ay+cy)//2}" text-anchor="middle" class="geo-val">{sb}</text>
{sc_txt}</svg>'''

    if t == 'tri_trigo':
        ax,ay,bx,by,cx,cy = 40,170,220,170,40,50
        angle = fig.get('angle',35)
        p0,p1,p2 = p(0,'A'),p(1,'B'),p(2,'C')
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<polygon points="{ax},{ay} {bx},{by} {cx},{cy}" class="geo-fill"/>
<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" class="geo-line"/><line x1="{bx}" y1="{by}" x2="{cx}" y2="{cy}" class="geo-line"/><line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" class="geo-line"/>
<rect x="{ax}" y="{ay-16}" width="16" height="16" class="geo-right"/>
<path d="M {bx-30},{by} A 30,30 0 0,1 {bx-20},{by-22}" class="geo-angle"/>
<text x="{bx-44}" y="{by-10}" class="geo-val" style="font-size:11px">{angle}°</text>
<text x="{(ax+bx)//2}" y="{ay+18}" text-anchor="middle" class="geo-label" style="font-size:11px">adjacent</text>
<text x="{ax-10}" y="{(ay+cy)//2}" class="geo-label" style="font-size:11px">opposé</text>
<text x="{(bx+cx)//2+12}" y="{(by+cy)//2}" class="geo-label" style="font-size:11px">hyp.</text>
<circle cx="{ax}" cy="{ay}" class="geo-dot"/><circle cx="{bx}" cy="{by}" class="geo-dot"/><circle cx="{cx}" cy="{cy}" class="geo-dot"/>
</svg>'''

    if t == 'thales':
        p0,p1,p2,p3 = p(0,'A'),p(1,'B'),p(2,'M'),p(3,'N')
        ox,oy,ax,ay,bx,by,mx,my,nx,ny = 130,30,50,170,210,170,70,110,190,110
        a,b,c = fig.get('a',4),fig.get('b',6),fig.get('c',3)
        d = fig.get('d')
        d_txt = f'<text x="{(ax+bx)//2}" y="{ay+16}" text-anchor="middle" class="geo-val">{d}</text>' if d else f'<text x="{(ax+bx)//2}" y="{ay+16}" text-anchor="middle" class="geo-unknown">?</text>'
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<line x1="{ox}" y1="{oy}" x2="{ax}" y2="{ay}" class="geo-line"/><line x1="{ox}" y1="{oy}" x2="{bx}" y2="{by}" class="geo-line"/>
<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" class="geo-line"/>
<line x1="{mx}" y1="{my}" x2="{nx}" y2="{ny}" class="geo-line" style="stroke:#6366f1;stroke-dasharray:6 3"/>
<text x="{ox+4}" y="{oy-6}" class="geo-label">O</text>
<text x="{ax-16}" y="{ay+4}" class="geo-label">{p0}</text><text x="{bx+6}" y="{by+4}" class="geo-label">{p1}</text>
<text x="{mx-18}" y="{my+4}" class="geo-label">{p2}</text><text x="{nx+6}" y="{ny+4}" class="geo-label">{p3}</text>
<text x="{(ox+mx)//2-16}" y="{(oy+my)//2}" class="geo-val">{a}</text>
<text x="{(ox+nx)//2+8}" y="{(oy+ny)//2}" class="geo-val">{b}</text>
<text x="{(mx+nx)//2}" y="{my-6}" text-anchor="middle" class="geo-val">{c}</text>
{d_txt}
<circle cx="{ox}" cy="{oy}" class="geo-dot"/><circle cx="{ax}" cy="{ay}" class="geo-dot"/><circle cx="{bx}" cy="{by}" class="geo-dot"/><circle cx="{mx}" cy="{my}" class="geo-dot"/><circle cx="{nx}" cy="{ny}" class="geo-dot"/>
</svg>'''

    if t == 'circle':
        cx0,cy0,r0 = 140,110,70
        r = fig.get('r',5)
        isDiam = bool(re.search(r'diamètre', fig.get('cat',''), re.I))
        if isDiam:
            return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<circle cx="{cx0}" cy="{cy0}" r="{r0}" class="geo-fill"/>
<line x1="{cx0-r0}" y1="{cy0}" x2="{cx0+r0}" y2="{cy0}" style="stroke:#059669;stroke-width:2"/>
<circle cx="{cx0}" cy="{cy0}" class="geo-dot"/>
<text x="{cx0-8}" y="{cy0-10}" class="geo-label">O</text>
<text x="{cx0}" y="{cy0-r0-8}" text-anchor="middle" class="geo-val">d = {r*2}</text>
</svg>'''
        else:
            return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<circle cx="{cx0}" cy="{cy0}" r="{r0}" class="geo-fill"/>
<line x1="{cx0}" y1="{cy0}" x2="{cx0+r0}" y2="{cy0}" style="stroke:#059669;stroke-dasharray:5 3;stroke-width:2"/>
<circle cx="{cx0+r0}" cy="{cy0}" class="geo-dot"/>
<circle cx="{cx0}" cy="{cy0}" class="geo-dot"/>
<text x="{cx0-8}" y="{cy0-10}" class="geo-label">O</text>
<text x="{(cx0+cx0+r0)//2}" y="{cy0-10}" text-anchor="middle" class="geo-val">r = {r}</text>
</svg>'''

    if t == 'rect':
        rx,ry,rw,rh = 40,50,180,110
        sq = fig.get('square',False)
        if sq: rw=rh=140
        rxe,rye = rx+rw, ry+rh
        p0,p1,p2,p3 = p(0,'A'),p(1,'B'),p(2,'C'),p(3,'D')
        w,h = fig.get('w',8),fig.get('h',5)
        h_txt = '' if sq else f'<text x="{rxe+8}" y="{(ry+rye)//2+4}" class="geo-val">{h}</text>'
        sq_mark = f'<rect x="{rx}" y="{rye-12}" width="12" height="12" class="geo-right"/>' if sq else ''
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="2" class="geo-fill"/>
<circle cx="{rx}" cy="{ry}" class="geo-dot"/><circle cx="{rxe}" cy="{ry}" class="geo-dot"/><circle cx="{rxe}" cy="{rye}" class="geo-dot"/><circle cx="{rx}" cy="{rye}" class="geo-dot"/>
<text x="{(rx+rxe)//2}" y="{ry-8}" text-anchor="middle" class="geo-val">{w}</text>
{h_txt}
<text x="{rx-8}" y="{ry-4}" class="geo-label">{p0}</text><text x="{rxe+4}" y="{ry-4}" class="geo-label">{p1}</text>
<text x="{rxe+4}" y="{rye+14}" class="geo-label">{p2}</text><text x="{rx-8}" y="{rye+14}" class="geo-label">{p3}</text>
{sq_mark}</svg>'''

    if t == 'angle':
        ox2,oy2 = 70,170
        deg = fig.get('deg',60)
        rad = deg*math.pi/180
        ln = 140
        ex2,ey2 = ox2+ln, oy2
        fx2,fy2 = ox2+ln*math.cos(rad), oy2-ln*math.sin(rad)
        arcR = 45
        aex,aey = ox2+arcR, oy2
        afx,afy = ox2+arcR*math.cos(rad), oy2-arcR*math.sin(rad)
        lr = arcR*0.65
        large = 1 if deg>180 else 0
        p1a = p(1,'O')
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<line x1="{ox2}" y1="{oy2}" x2="{ex2}" y2="{ey2}" class="geo-line"/>
<line x1="{ox2}" y1="{oy2}" x2="{fx2:.1f}" y2="{fy2:.1f}" class="geo-line"/>
<path d="M {aex},{aey} A {arcR},{arcR} 0 {large},0 {afx:.1f},{afy:.1f}" class="geo-angle" style="stroke-width:2"/>
<text x="{ox2+lr*math.cos(rad/2):.0f}" y="{oy2-lr*math.sin(rad/2):.0f}" class="geo-val" text-anchor="middle">{deg}°</text>
<circle cx="{ox2}" cy="{oy2}" class="geo-dot"/>
<text x="{ox2-12}" y="{oy2+16}" class="geo-label">{p1a}</text>
</svg>'''

    if t == 'parallel':
        if fig.get('perp'):
            return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<line x1="30" y1="100" x2="230" y2="100" class="geo-line"/>
<line x1="130" y1="30" x2="130" y2="180" class="geo-line"/>
<rect x="130" y="86" width="14" height="14" class="geo-right"/>
<text x="235" y="104" class="geo-label">(d₁)</text><text x="134" y="26" class="geo-label">(d₂)</text>
<text x="148" y="92" class="geo-val" style="font-size:11px">⊥</text></svg>'''
        else:
            return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<line x1="30" y1="70" x2="230" y2="70" class="geo-line"/><line x1="30" y1="130" x2="230" y2="130" class="geo-line"/>
<text x="235" y="74" class="geo-label">(d₁)</text><text x="235" y="134" class="geo-label">(d₂)</text>
<text x="130" y="106" text-anchor="middle" class="geo-val" style="font-size:11px">∥</text></svg>'''

    if t == 'sym_axial':
        p0s,p1s,p2s = p(0,'A'),p(1,'B'),p(2,'C')
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<line x1="140" y1="10" x2="140" y2="200" class="geo-axis" style="stroke-dasharray:8 4;stroke-width:2"/>
<text x="144" y="20" class="geo-label" style="fill:#a855f7;font-size:11px">(d)</text>
<polygon points="55,60 95,150 75,150" class="geo-fill"/><polygon points="225,60 185,150 205,150" class="geo-fill2"/>
<line x1="55" y1="60" x2="225" y2="60" class="geo-dash"/><line x1="95" y1="150" x2="185" y2="150" class="geo-dash"/>
<circle cx="55" cy="60" class="geo-dot"/><circle cx="225" cy="60" class="geo-dot"/>
<text x="42" y="54" class="geo-label">{p0s}</text><text x="229" y="54" class="geo-label" style="fill:#22c55e">{p0s}'</text>
<text x="95" y="166" class="geo-label">{p1s}</text><text x="178" y="166" class="geo-label" style="fill:#22c55e">{p1s}'</text></svg>'''

    if t == 'sym_central':
        p0c,p1c,p2c = p(0,'A'),p(1,'B'),p(2,'C')
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<circle cx="140" cy="105" r="5" style="fill:#a855f7"/><text x="148" y="103" class="geo-label" style="fill:#a855f7">O</text>
<polygon points="55,50 105,80 75,115" class="geo-fill"/><polygon points="225,160 175,130 205,95" class="geo-fill2"/>
<line x1="55" y1="50" x2="225" y2="160" class="geo-dash"/><line x1="105" y1="80" x2="175" y2="130" class="geo-dash"/>
<circle cx="55" cy="50" class="geo-dot"/><circle cx="225" cy="160" class="geo-dot"/>
<text x="41" y="48" class="geo-label">{p0c}</text><text x="231" y="162" class="geo-label" style="fill:#22c55e">{p0c}'</text></svg>'''

    if t == 'cube':
        dx,dy = 30,20
        x0,y0,w3,h3 = 50,140,120,90
        if fig.get('isCube'): w3=h3=100
        a,b,c = fig.get('a',4),fig.get('b',3),fig.get('c',2)
        isCube = fig.get('isCube',False)
        b_txt = '' if isCube else f'<text x="{x0+w3+dx+8}" y="{(y0-h3+y0)//2}" class="geo-val">{b}</text>'
        c_txt = '' if isCube else f'<text x="{(x0+w3+x0+w3+dx)//2+4}" y="{y0-h3-dy-4}" text-anchor="middle" class="geo-val">{c}</text>'
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<rect x="{x0}" y="{y0-h3}" width="{w3}" height="{h3}" class="geo-3d-face"/>
<polygon points="{x0+w3},{y0-h3} {x0+w3+dx},{y0-h3-dy} {x0+w3+dx},{y0-dy} {x0+w3},{y0}" class="geo-3d-face" style="opacity:.35"/>
<polygon points="{x0},{y0-h3} {x0+dx},{y0-h3-dy} {x0+w3+dx},{y0-h3-dy} {x0+w3},{y0-h3}" class="geo-3d-face" style="opacity:.25"/>
<line x1="{x0}" y1="{y0}" x2="{x0+w3}" y2="{y0}" class="geo-3d-edge"/><line x1="{x0}" y1="{y0-h3}" x2="{x0+w3}" y2="{y0-h3}" class="geo-3d-edge"/>
<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-h3}" class="geo-3d-edge"/><line x1="{x0+w3}" y1="{y0}" x2="{x0+w3}" y2="{y0-h3}" class="geo-3d-edge"/>
<line x1="{x0+w3}" y1="{y0}" x2="{x0+w3+dx}" y2="{y0-dy}" class="geo-3d-edge"/>
<line x1="{x0+w3}" y1="{y0-h3}" x2="{x0+w3+dx}" y2="{y0-h3-dy}" class="geo-3d-edge"/>
<line x1="{x0}" y1="{y0-h3}" x2="{x0+dx}" y2="{y0-h3-dy}" class="geo-3d-edge"/>
<line x1="{x0+dx}" y1="{y0-h3-dy}" x2="{x0+w3+dx}" y2="{y0-h3-dy}" class="geo-3d-edge"/>
<line x1="{x0+w3+dx}" y1="{y0-h3-dy}" x2="{x0+w3+dx}" y2="{y0-dy}" class="geo-3d-edge"/>
<text x="{(x0+x0+w3)//2}" y="{y0+16}" text-anchor="middle" class="geo-val">{a}</text>
{b_txt}{c_txt}</svg>'''

    if t == 'cylinder':
        cx1,top,bot,rx1,ry1 = 130,40,155,60,18
        r,h = fig.get('r',3),fig.get('h',6)
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="{cx1}" cy="{bot}" rx="{rx1}" ry="{ry1}" class="geo-3d-face"/>
<line x1="{cx1-rx1}" y1="{top}" x2="{cx1-rx1}" y2="{bot}" class="geo-3d-edge"/><line x1="{cx1+rx1}" y1="{top}" x2="{cx1+rx1}" y2="{bot}" class="geo-3d-edge"/>
<ellipse cx="{cx1}" cy="{top}" rx="{rx1}" ry="{ry1}" class="geo-3d-face" style="opacity:.6"/>
<line x1="{cx1}" y1="{top}" x2="{cx1+rx1}" y2="{top}" style="stroke:#059669;stroke-dasharray:5 3"/>
<text x="{(cx1+cx1+rx1)//2}" y="{top-6}" text-anchor="middle" class="geo-val">r={r}</text>
<text x="{cx1+rx1+10}" y="{(top+bot)//2+4}" class="geo-val">h={h}</text></svg>'''

    if t == 'cone':
        cx2,tipY,baseY,rx2,ry2 = 130,35,160,60,16
        r,h = fig.get('r',3),fig.get('h',6)
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="{cx2}" cy="{baseY}" rx="{rx2}" ry="{ry2}" class="geo-3d-face"/>
<line x1="{cx2-rx2}" y1="{baseY}" x2="{cx2}" y2="{tipY}" class="geo-3d-edge"/><line x1="{cx2+rx2}" y1="{baseY}" x2="{cx2}" y2="{tipY}" class="geo-3d-edge"/>
<line x1="{cx2}" y1="{tipY}" x2="{cx2}" y2="{baseY}" style="stroke:#059669;stroke-dasharray:5 3"/>
<circle cx="{cx2}" cy="{tipY}" class="geo-dot"/>
<text x="{cx2+8}" y="{(tipY+baseY)//2}" class="geo-val">h={h}</text>
<text x="{(cx2+cx2+rx2)//2}" y="{baseY+16}" text-anchor="middle" class="geo-val">r={r}</text></svg>'''

    if t == 'pyramid':
        px0,ptip,pbl,pbr,pby = 130,30,60,200,170
        a,h = fig.get('a',4),fig.get('h',6)
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<polygon points="{pbl},{pby} {pbr},{pby} {pbr-15},{pby-25} {pbl+15},{pby-25}" class="geo-3d-face" style="opacity:.3"/>
<line x1="{pbl}" y1="{pby}" x2="{px0}" y2="{ptip}" class="geo-3d-edge"/><line x1="{pbr}" y1="{pby}" x2="{px0}" y2="{ptip}" class="geo-3d-edge"/>
<line x1="{pbl+15}" y1="{pby-25}" x2="{px0}" y2="{ptip}" class="geo-3d-hidden"/>
<line x1="{pbr-15}" y1="{pby-25}" x2="{px0}" y2="{ptip}" class="geo-3d-edge"/>
<line x1="{pbl}" y1="{pby}" x2="{pbr}" y2="{pby}" class="geo-3d-edge"/>
<line x1="{px0}" y1="{ptip}" x2="{px0}" y2="{pby}" style="stroke:#059669;stroke-dasharray:5 3"/>
<circle cx="{px0}" cy="{ptip}" class="geo-dot"/>
<text x="{px0+8}" y="{(ptip+pby)//2}" class="geo-val">h={h}</text>
<text x="{(pbl+pbr)//2}" y="{pby+16}" text-anchor="middle" class="geo-val">{a}</text></svg>'''

    if t == 'sphere':
        scx,scy,sr = 130,100,70
        r = fig.get('r',4)
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="sg" cx="40%" cy="35%"><stop offset="0%" stop-color="#c7d2fe"/><stop offset="100%" stop-color="#eef2ff"/></radialGradient></defs>
<circle cx="{scx}" cy="{scy}" r="{sr}" fill="url(#sg)" stroke="#6366f1" stroke-width="1.5"/>
<ellipse cx="{scx}" cy="{scy}" rx="{sr}" ry="{int(sr*0.3)}" style="stroke:#6366f1;opacity:.5;fill:none;stroke-dasharray:5 3"/>
<line x1="{scx}" y1="{scy}" x2="{scx+sr}" y2="{scy}" style="stroke:#059669;stroke-width:2"/>
<circle cx="{scx}" cy="{scy}" class="geo-dot"/>
<text x="{scx-8}" y="{scy-8}" class="geo-label">O</text>
<text x="{(scx+scx+sr)//2}" y="{scy-8}" text-anchor="middle" class="geo-val">r={r}</text></svg>'''

    if t == 'section_solid':
        dx3,dy3,x3,y3,w4,h4 = 30,20,50,150,110,95
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<rect x="{x3}" y="{y3-h4}" width="{w4}" height="{h4}" class="geo-3d-face"/>
<line x1="{x3+w4}" y1="{y3}" x2="{x3+w4+dx3}" y2="{y3-dy3}" class="geo-3d-edge"/>
<line x1="{x3+w4}" y1="{y3-h4}" x2="{x3+w4+dx3}" y2="{y3-h4-dy3}" class="geo-3d-edge"/>
<line x1="{x3}" y1="{y3-h4}" x2="{x3+dx3}" y2="{y3-h4-dy3}" class="geo-3d-edge"/>
<line x1="{x3+dx3}" y1="{y3-h4-dy3}" x2="{x3+w4+dx3}" y2="{y3-h4-dy3}" class="geo-3d-edge"/>
<line x1="{x3+w4+dx3}" y1="{y3-h4-dy3}" x2="{x3+w4+dx3}" y2="{y3-dy3}" class="geo-3d-edge"/>
<polygon points="{x3},{int(y3-h4*0.6)} {x3+w4},{int(y3-h4*0.3)} {x3+w4+dx3},{int(y3-h4*0.3-dy3)} {x3+dx3},{int(y3-h4*0.6-dy3)}" style="fill:#fde68a;stroke:#f59e0b;stroke-width:2;opacity:.45"/>
<text x="{(x3+x3+w4)//2+dx3//2}" y="{int(y3-h4*0.45-dy3/2-6)}" text-anchor="middle" class="geo-val" style="fill:#d97706;font-size:11px">section</text></svg>'''

    if t == 'homothety':
        p0 = p(0,'A')
        hox,hoy = 50,160
        hax,hay,hbx,hby,hcx,hcy = 100,100,140,100,120,60
        k = fig.get('k',2)
        k2 = k if k>1 else 1/k
        hax2,hay2 = hox+(hax-hox)*k2, hoy+(hay-hoy)*k2
        hbx2,hby2 = hox+(hbx-hox)*k2, hoy+(hby-hoy)*k2
        hcx2,hcy2 = hox+(hcx-hox)*k2, hoy+(hcy-hoy)*k2
        if max(hax2,hbx2,hcx2)>250:
            k2=1.5
            hax2,hay2 = hox+(hax-hox)*k2, hoy+(hay-hoy)*k2
            hbx2,hby2 = hox+(hbx-hox)*k2, hoy+(hby-hoy)*k2
            hcx2,hcy2 = hox+(hcx-hox)*k2, hoy+(hcy-hoy)*k2
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<polygon points="{hax},{hay} {hbx},{hby} {hcx},{hcy}" class="geo-fill"/>
<polygon points="{hax2:.0f},{hay2:.0f} {hbx2:.0f},{hby2:.0f} {hcx2:.0f},{hcy2:.0f}" class="geo-fill2"/>
<line x1="{hox}" y1="{hoy}" x2="{hax2:.0f}" y2="{hay2:.0f}" class="geo-dash"/>
<line x1="{hox}" y1="{hoy}" x2="{hbx2:.0f}" y2="{hby2:.0f}" class="geo-dash"/>
<line x1="{hox}" y1="{hoy}" x2="{hcx2:.0f}" y2="{hcy2:.0f}" class="geo-dash"/>
<circle cx="{hox}" cy="{hoy}" r="4" style="fill:#a855f7"/>
<text x="{hox-10}" y="{hoy+16}" class="geo-label" style="fill:#a855f7">O</text>
<text x="{hax}" y="{hay-6}" class="geo-label">{p0}</text>
<text x="{hax2:.0f}" y="{hay2-6}" class="geo-label" style="fill:#22c55e">{p0}'</text>
<text x="{hox+30}" y="{hoy-8}" class="geo-val" style="font-size:11px">k={k}</text></svg>'''

    if t == 'similar_tri':
        p0,p1,p2 = p(0,'A'),p(1,'B'),p(2,'C')
        a = fig.get('a',3)
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<polygon points="30,160 130,160 80,80" class="geo-fill"/><polygon points="150,160 230,160 190,110" class="geo-fill2"/>
<circle cx="30" cy="160" class="geo-dot"/><circle cx="130" cy="160" class="geo-dot"/><circle cx="80" cy="80" class="geo-dot"/>
<circle cx="150" cy="160" class="geo-dot"/><circle cx="230" cy="160" class="geo-dot"/><circle cx="190" cy="110" class="geo-dot"/>
<text x="22" y="176" class="geo-label">{p0}</text><text x="132" y="176" class="geo-label">{p1}</text><text x="74" y="74" class="geo-label">{p2}</text>
<text x="142" y="176" class="geo-label" style="fill:#22c55e">{p0}'</text><text x="232" y="176" class="geo-label" style="fill:#22c55e">{p1}'</text><text x="194" y="106" class="geo-label" style="fill:#22c55e">{p2}'</text>
<text x="80" y="176" text-anchor="middle" class="geo-val">{a}</text>
<text x="190" y="176" text-anchor="middle" class="geo-val" style="fill:#22c55e">?</text></svg>'''

    if t == 'triangle':
        p0,p1,p2 = p(0,'A'),p(1,'B'),p(2,'C')
        a = fig.get('a',5)
        b,c = fig.get('b'),fig.get('c')
        b_txt = f'<text x="180" y="100" class="geo-val">{b}</text>' if b else ''
        c_txt = f'<text x="76" y="100" class="geo-val">{c}</text>' if c else ''
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<polygon points="40,170 220,170 130,40" class="geo-fill"/>
<line x1="40" y1="170" x2="220" y2="170" class="geo-line"/><line x1="220" y1="170" x2="130" y2="40" class="geo-line"/><line x1="130" y1="40" x2="40" y2="170" class="geo-line"/>
<circle cx="40" cy="170" class="geo-dot"/><circle cx="220" cy="170" class="geo-dot"/><circle cx="130" cy="40" class="geo-dot"/>
<text x="32" y="186" class="geo-label">{p0}</text><text x="224" y="186" class="geo-label">{p1}</text><text x="124" y="34" class="geo-label">{p2}</text>
<text x="130" y="186" text-anchor="middle" class="geo-val">{a}</text>{b_txt}{c_txt}</svg>'''

    if t == 'transform':
        if fig.get('isRotation'):
            return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<circle cx="130" cy="110" r="4" style="fill:#a855f7"/><text x="138" y="114" class="geo-label" style="fill:#a855f7">O</text>
<polygon points="60,70 110,50 90,90" class="geo-fill"/><polygon points="150,150 200,130 180,170" class="geo-fill2"/>
<defs><marker id="arrowR" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#a855f7"/></marker></defs>
<path d="M 100,80 A 50,50 0 0,1 160,140" style="stroke:#a855f7;fill:none;stroke-dasharray:5 3" marker-end="url(#arrowR)"/>
<text x="170" y="100" class="geo-val" style="fill:#a855f7;font-size:11px">rotation</text></svg>'''
        else:
            return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<polygon points="40,60 100,40 80,100" class="geo-fill"/><polygon points="140,110 200,90 180,150" class="geo-fill2"/>
<defs><marker id="arrowT" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#6366f1"/></marker></defs>
<line x1="40" y1="60" x2="140" y2="110" style="stroke:#6366f1;stroke-dasharray:5 3" marker-end="url(#arrowT)"/>
<line x1="100" y1="40" x2="200" y2="90" style="stroke:#6366f1;stroke-dasharray:5 3" marker-end="url(#arrowT)"/>
<line x1="80" y1="100" x2="180" y2="150" style="stroke:#6366f1;stroke-dasharray:5 3" marker-end="url(#arrowT)"/>
<text x="120" y="70" class="geo-val" style="font-size:11px">vecteur</text></svg>'''

    if t == 'vectors':
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arrowV" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#6366f1"/></marker></defs>
<line x1="50" y1="160" x2="230" y2="160" class="geo-line" marker-end="url(#arrowV)"/>
<line x1="50" y1="160" x2="180" y2="60" class="geo-line" marker-end="url(#arrowV)"/>
<path d="M 90,160 A 45,45 0 0,0 82,135" class="geo-angle" style="stroke-width:2;stroke:#f59e0b"/>
<circle cx="50" cy="160" r="3" style="fill:#6366f1"/>
<text x="38" y="176" class="geo-label">O</text>
<text x="232" y="164" class="geo-label" style="font-style:italic">u⃗</text>
<text x="178" y="52" class="geo-label" style="font-style:italic">v⃗</text>
<text x="98" y="146" class="geo-val" style="font-size:12px;fill:#f59e0b">θ</text></svg>'''

    if t == 'repere':
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arrowAx" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#374151"/></marker></defs>
<line x1="20" y1="150" x2="260" y2="150" class="geo-line" style="stroke-width:1.5" marker-end="url(#arrowAx)"/>
<line x1="50" y1="195" x2="50" y2="15" class="geo-line" style="stroke-width:1.5" marker-end="url(#arrowAx)"/>
<text x="262" y="154" class="geo-label">x</text><text x="42" y="12" class="geo-label">y</text><text x="38" y="164" class="geo-label">O</text>
<line x1="30" y1="30" x2="240" y2="180" style="stroke:#6366f1;stroke-width:2"/>
<text x="242" y="180" class="geo-val" style="font-size:11px;fill:#6366f1">(d)</text></svg>'''

    if t == 'trigo_circle':
        tcx,tcy,tcr = 140,110,80
        tcAngle = 0.7
        tmx,tmy = tcx+tcr*math.cos(tcAngle), tcy-tcr*math.sin(tcAngle)
        return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arrowTC" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto"><path d="M0,0 L7,2.5 L0,5" fill="#374151"/></marker></defs>
<line x1="30" y1="{tcy}" x2="260" y2="{tcy}" class="geo-line" style="stroke-width:1" marker-end="url(#arrowTC)"/>
<line x1="{tcx}" y1="200" x2="{tcx}" y2="15" class="geo-line" style="stroke-width:1" marker-end="url(#arrowTC)"/>
<circle cx="{tcx}" cy="{tcy}" r="{tcr}" style="fill:none;stroke:#6366f1;stroke-width:2"/>
<line x1="{tcx}" y1="{tcy}" x2="{tmx:.1f}" y2="{tmy:.1f}" style="stroke:#059669;stroke-width:2"/>
<circle cx="{tmx:.1f}" cy="{tmy:.1f}" r="3" style="fill:#059669"/>
<text x="{tmx+6:.0f}" y="{tmy-8:.0f}" class="geo-label" style="fill:#059669">M</text>
<line x1="{tmx:.1f}" y1="{tmy:.1f}" x2="{tmx:.1f}" y2="{tcy}" style="stroke:#f59e0b;fill:none;stroke-dasharray:4 3"/>
<line x1="{tmx:.1f}" y1="{tmy:.1f}" x2="{tcx}" y2="{tmy:.1f}" style="stroke:#ef4444;fill:none;stroke-dasharray:4 3"/>
<text x="{tmx:.0f}" y="{tcy+14}" class="geo-val" text-anchor="middle" style="font-size:10px;fill:#f59e0b">cos θ</text>
<text x="{tcx-24}" y="{tmy:.0f}" class="geo-val" text-anchor="middle" style="font-size:10px;fill:#ef4444">sin θ</text>
<path d="M {tcx+25},{tcy} A 25,25 0 0,0 {tcx+25*math.cos(tcAngle):.1f},{tcy-25*math.sin(tcAngle):.1f}" class="geo-angle" style="stroke-width:2"/>
<text x="{tcx+34}" y="{tcy-10}" class="geo-val" style="font-size:11px">θ</text>
<circle cx="{tcx}" cy="{tcy}" r="2" style="fill:#374151"/>
<text x="{tcx-12}" y="{tcy+14}" class="geo-label">O</text>
<text x="{tcx+tcr+6}" y="{tcy+14}" class="geo-label">I</text>
<text x="{tcx+6}" y="{tcy-tcr-4}" class="geo-label">J</text></svg>'''

    # rect_square alias
    if t == 'rect_square':
        fig['type'] = 'rect'
        fig['square'] = True
        if 'w' not in fig: fig['w'] = fig.get('a',5)
        if 'h' not in fig: fig['h'] = fig.get('a',5)
        return render_fig(fig)

    return f'<div style="color:#999;font-style:italic">[Figure type: {t}]</div>'


def get_figure(exo, cat):
    """Retourne (fig_dict, svg_html) ou (None, None)."""
    fig = exo.get('fig')
    if fig and isinstance(fig, dict):
        svg = render_fig(fig)
        return fig, svg
    fig = auto_detect_figure(exo.get('q',''), cat)
    if fig:
        # Filter low confidence
        if fig.get('confidence') == 'low':
            return None, None
        svg = render_fig(fig)
        return fig, svg
    return None, None


# ══════════════════════════════════════════════════════════════
# LECTURE DONNÉES
# ══════════════════════════════════════════════════════════════

SHEETS_LIST = ['Curriculum_Officiel', 'DiagnosticExos', 'BoostExos', 'BrevetExos']
all_exos = []

for sheet_name in SHEETS_LIST:
    print(f"📖 Lecture {sheet_name}...")
    try:
        rows = sh.read(sheet_name)
    except Exception as e:
        print(f"   ⚠️ {e}")
        continue
    for row in rows:
        niveau = row.get('Niveau', '')
        categorie = row.get('Categorie', '')
        exos_json = row.get('ExosJSON', '')
        if not exos_json: continue
        try:
            exos = json.loads(exos_json)
        except: continue
        for idx, exo in enumerate(exos):
            fig, svg = get_figure(exo, categorie)
            if fig and svg:
                all_exos.append((sheet_name, niveau, categorie, idx+1, exo, fig, svg))

print(f"\n✅ {len(all_exos)} exercices avec figure\n")

# ══════════════════════════════════════════════════════════════
# CSS pour les SVG (reproduit depuis l'app)
# ══════════════════════════════════════════════════════════════

SVG_CSS = """
.geo-fig { max-width: 280px; margin: 8px 0; }
.geo-fig svg { width: 100%; height: auto; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; }
.geo-fill { fill: #eef2ff; stroke: #6366f1; stroke-width: 1.5; }
.geo-fill2 { fill: #dcfce7; stroke: #22c55e; stroke-width: 1.5; }
.geo-line { stroke: #374151; stroke-width: 1.5; fill: none; }
.geo-dash { stroke: #9ca3af; stroke-width: 1; stroke-dasharray: 5 3; fill: none; }
.geo-dot { r: 3; fill: #374151; }
.geo-label { font-size: 13px; font-weight: 600; fill: #374151; font-family: sans-serif; }
.geo-val { font-size: 12px; fill: #6366f1; font-weight: 600; font-family: sans-serif; }
.geo-unknown { font-size: 14px; fill: #ef4444; font-weight: 700; font-family: sans-serif; }
.geo-right { fill: none; stroke: #6366f1; stroke-width: 1; }
.geo-angle { fill: none; stroke: #f59e0b; stroke-width: 1.5; }
.geo-axis { stroke: #a855f7; fill: none; }
.geo-3d-face { fill: #eef2ff; stroke: #6366f1; stroke-width: 1; }
.geo-3d-edge { stroke: #374151; stroke-width: 1.5; fill: none; }
.geo-3d-hidden { stroke: #9ca3af; stroke-width: 1; stroke-dasharray: 4 3; fill: none; }
.geo-3d-face2 { fill: #eef2ff; stroke: #9ca3af; stroke-width: 1; stroke-dasharray: 4 3; opacity: .2; }
"""

# ══════════════════════════════════════════════════════════════
# GÉNÉRATION HTML (importable Google Docs + lisible navigateur)
# ══════════════════════════════════════════════════════════════

html_parts = [f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<title>Audit figures — Matheux ({len(all_exos)} exos)</title>
<style>
  body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; color: #1a1a1a; }}
  h1 {{ color: #4f46e5; border-bottom: 3px solid #4f46e5; padding-bottom: 8px; }}
  h2 {{ color: #6366f1; margin-top: 40px; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }}
  .exo {{ border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin: 12px 0; background: #fafbfc; page-break-inside: avoid; }}
  .exo-header {{ font-weight: 700; color: #4f46e5; margin-bottom: 8px; font-size: 14px; }}
  .field {{ margin: 4px 0; }}
  .label {{ font-weight: 600; color: #374151; }}
  .correct {{ color: #059669; font-weight: 700; }}
  .options {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 4px 0; }}
  .opt {{ padding: 4px 10px; border-radius: 4px; background: #f1f5f9; font-size: 13px; }}
  .opt.right {{ background: #dcfce7; color: #059669; font-weight: 600; border: 1px solid #86efac; }}
  .step {{ margin-left: 16px; color: #475569; }}
  .formula {{ background: #fef3c7; padding: 4px 8px; border-radius: 4px; display: inline-block; }}
  .meta {{ font-size: 12px; color: #9ca3af; margin-top: 4px; }}
  {SVG_CSS}
</style></head><body>
<h1>Audit figures géométriques — Matheux</h1>
<p><strong>{len(all_exos)} exercices avec figure</strong> — généré le 18 mars 2026</p>
<p>Sources : Curriculum_Officiel · DiagnosticExos · BoostExos · BrevetExos</p>
<hr>
"""]

current_key = None
for source, niveau, cat, idx, exo, fig, svg in all_exos:
    key = f"{niveau} / {cat}"
    if key != current_key:
        current_key = key
        html_parts.append(f'<h2>{niveau} — {cat}</h2>\n')

    q = exo.get('q','')
    a = exo.get('a','')
    options = exo.get('options',[])
    f = exo.get('f','')
    steps = exo.get('steps',[])
    lvl = exo.get('lvl','?')
    fig_type = fig.get('type','?')

    opts_html = ''
    for opt in options:
        cls = 'opt right' if opt.strip() == a.strip() else 'opt'
        opts_html += f'<span class="{cls}">{opt}</span> '

    steps_html = ''
    for i, step in enumerate(steps, 1):
        steps_html += f'<div class="step">{i}. {step}</div>'

    formula_html = f'<div class="field"><span class="label">Formule :</span> <span class="formula">{f}</span></div>' if f else ''

    html_parts.append(f'''<div class="exo">
<div class="exo-header">[{source}] Exo {idx} — {fig_type}</div>
<div class="field"><span class="label">Énoncé :</span> {q}</div>
<div class="field"><span class="label">Réponse :</span> <span class="correct">{a}</span></div>
<div class="field"><span class="label">Options :</span> <div class="options">{opts_html}</div></div>
{formula_html}
{f'<div class="field"><span class="label">Indices :</span>{steps_html}</div>' if steps else ''}
<div class="geo-fig">{svg}</div>
<div class="meta">Niveau {lvl} | Figure : {fig_type}</div>
</div>
''')

html_parts.append('</body></html>')

html_path = '/home/nicolas/Bureau/algebra live/algebra/audit_figures.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))
print(f"🌐 {html_path}")

# ══════════════════════════════════════════════════════════════
# GÉNÉRATION MD
# ══════════════════════════════════════════════════════════════

md = [f"# Audit figures géométriques — Matheux\n\n**{len(all_exos)} exercices avec figure**\n\n---\n"]
current_key = None
for source, niveau, cat, idx, exo, fig, svg in all_exos:
    key = f"{niveau} / {cat}"
    if key != current_key:
        current_key = key
        md.append(f"\n## {niveau} — {cat}\n")

    q = exo.get('q','')
    a = exo.get('a','')
    options = exo.get('options',[])
    f = exo.get('f','')
    steps = exo.get('steps',[])
    fig_type = fig.get('type','?')

    md.append(f"### [{source}] Exo {idx} — `{fig_type}`\n")
    md.append(f"**Énoncé :** {q}\n")
    md.append(f"**Réponse :** {a}\n")
    md.append(f"**Options :** {' | '.join(options)}\n")
    if f: md.append(f"**Formule :** {f}\n")
    if steps:
        md.append("**Indices :**\n")
        for i, s in enumerate(steps, 1):
            md.append(f"  {i}. {s}\n")
    md.append(f"*Figure : {fig_type}*\n\n---\n")

md_path = '/home/nicolas/Bureau/algebra live/algebra/audit_figures.md'
with open(md_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))
print(f"📝 {md_path}")

print(f"\n🎯 {len(all_exos)} exercices exportés avec figures SVG")
