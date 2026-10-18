import math
cx,cy,Rx,Ry=186,92,130,68
names=["Aufschieben","Deadline naht","Stress","Arbeitsphase","Erleichterung"]
angs=[-90,-18,54,126,198]
pw,ph=112,30
nodes=[(cx+Rx*math.cos(math.radians(a)), cy+Ry*math.sin(math.radians(a))) for a in angs]
def inside(p,c,pad=7): return abs(p[0]-c[0])<=pw/2+pad and abs(p[1]-c[1])<=ph/2+pad
out=[]
for i in range(5):
    a0=angs[i]; a1=angs[i+1] if i<4 else angs[0]+360
    pts=[]
    for k in range(600):
        a=a0+(a1-a0)*k/599; t=math.radians(a)
        p=(cx+Rx*math.cos(t), cy+Ry*math.sin(t))
        if not inside(p,nodes[i]) and not inside(p,nodes[(i+1)%5]): pts.append(p)
    pts=pts[::8]+[pts[-1]]
    out.append("M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts))
for n,(x,y) in zip(names,nodes): print(f'<rect x="{x-pw/2:.1f}" y="{y-ph/2:.1f}" width="{pw}" height="{ph}" rx="15"/> <text x="{x:.1f}" y="{y+5:.1f}">{n}</text>')
for d in out: print(d)
