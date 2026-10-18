import math
# --- Kreislauf-Diagramm ---
W,H=372,206
cx,cy,Rx,Ry=186,104,118,74
names=["Aufschieben","Deadline naht","Stress","Arbeitsphase","Erleichterung"]
angs=[-90,-18,54,126,198]
pw,ph=116,30
nodes=[]
for a in angs:
    t=math.radians(a); nodes.append((cx+Rx*math.cos(t), cy+Ry*math.sin(t)))
for n,(x,y) in zip(names,nodes): print(n, round(x,1), round(y,1))
def inside(p,c,pad=7):
    return abs(p[0]-c[0])<=pw/2+pad and abs(p[1]-c[1])<=ph/2+pad
segs=[]
for i in range(5):
    a0=angs[i]; a1=angs[i+1] if i<4 else angs[0]+360
    pts=[]
    for k in range(400):
        a=a0+(a1-a0)*k/399; t=math.radians(a)
        p=(cx+Rx*math.cos(t), cy+Ry*math.sin(t))
        if not inside(p,nodes[i]) and not inside(p,nodes[(i+1)%5]): pts.append(p)
    pts=pts[::6]+[pts[-1]]
    d="M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts)
    segs.append(d)
for d in segs: print(d); print()
# --- Stern ---
def star(cx,cy,ro,ri):
    pts=[]
    for k in range(10):
        r=ro if k%2==0 else ri; a=math.radians(-90+36*k)
        pts.append(f"{cx+r*math.cos(a):.2f} {cy+r*math.sin(a):.2f}")
    return "M"+" L".join(pts)+" Z"
print("STAR",star(18.6,6.2,4.9,2.1))
# --- Kreislauf-Icon (48) ---
def arcpts(c,r,a0,a1,n=40):
    return [(c[0]+r*math.cos(math.radians(a)), c[1]-r*math.sin(math.radians(a))) for a in [a0+(a1-a0)*k/(n-1) for k in range(n)]]
def head(c,r,a,dirsign,size=6.5):
    # Pfeilspitze am Winkel a, Bewegungsrichtung CCW (dirsign=1) mathematisch
    t=math.radians(a)
    px,py=c[0]+r*math.cos(t), c[1]-r*math.sin(t)
    # Tangente math: (-sin, cos)*dirsign -> screen (x, -y)
    tx,ty=-math.sin(t)*dirsign, -math.cos(t)*dirsign
    nx,ny=-ty,tx
    tip=(px+tx*size,py+ty*size)
    b1=(px+nx*size*0.75,py+ny*size*0.75); b2=(px-nx*size*0.75,py-ny*size*0.75)
    return f"M{tip[0]:.1f} {tip[1]:.1f} L{b1[0]:.1f} {b1[1]:.1f} L{b2[0]:.1f} {b2[1]:.1f} Z"
c=(24,24); r=14
for a0,a1 in [(20,160),(200,340)]:
    pts=arcpts(c,r,a0,a1)
    print("ARC","M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts))
    print("HEAD",head(c,r,a1,1))
