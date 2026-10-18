s=open('professional.html',encoding='utf-8').read()
def R(a,b,n=1):
    global s
    c=s.count(a)
    assert c==n,(c,a[:70])
    s=s.replace(a,b)
# Raster/Positionen
R(".kern{position:absolute;left:32px;top:190px;",".kern{position:absolute;left:32px;top:186px;")
R(".grid{position:absolute;left:32px;top:290px;width:704px;height:992px;",".grid{position:absolute;left:32px;top:284px;width:704px;height:982px;")
R("grid-template-rows:210px 244px 226px 1fr}","grid-template-rows:234px 236px 226px 1fr}")
R(".pt{flex:1;font:700 16px/1.2 'Montserrat';color:var(--navy);padding-top:3px}",".pt{flex:1;font:700 16px/1.2 'Montserrat';color:var(--navy);padding-top:3px;text-wrap:balance}")
# 01 Merksatz wie 05
R('<div class="merk"><span class="lbl">Merksatz</span><span class="mt">Dasselbe Gehirn, andere Aktivierung.</span></div>','<div class="merk2"><span class="lbl">Merksatz</span><span class="mt">Dasselbe Gehirn, andere Aktivierung.</span></div>')
R(".merk2{margin-top:auto;border-left:4px solid var(--orange);padding:4px 0 2px 12px}",".merk2{margin-top:auto;border-left:4px solid var(--orange);padding:5px 0 3px 12px;background:linear-gradient(90deg,rgba(232,118,47,.10),rgba(232,118,47,0) 85%)}")
# 02 Karten
R(""".mvr{display:grid;grid-template-columns:1fr 30px 1fr;flex:1;min-height:0}""",""".mvr{display:grid;grid-template-columns:minmax(0,1fr) 34px minmax(0,1fr);flex:1;min-height:0}
.col{display:flex;flex-direction:column;border-radius:5px;padding:10px 11px 12px}
.myth{background:#e7decb}
.real{background:var(--navy)}""")
R(".myth .tag{background:#e3d9c5;color:var(--grey)}",".myth .tag{background:#f6f1e6;color:var(--grey)}")
R(".real .tag{background:var(--navy);color:var(--paper-l)}",".real .tag{background:#2d4d79;color:var(--paper-l)}")
R(".col .tag{display:inline-flex;",".col .tag{align-self:flex-start;display:inline-flex;")
R(".col p{margin-top:10px}",".col p{margin-top:12px;font-size:16.5px;line-height:1.36}")
R(".myth p{color:var(--grey)}",".myth p{color:#4f4a42}")
R(".real p{color:var(--navy);font-weight:600}",".real p{color:var(--paper-l);font-weight:600}")
R(".vs::before{content:\"\";position:absolute;top:0;bottom:0;left:50%;border-left:1px solid var(--sand)}",".vs::before{content:\"\";position:absolute;top:10px;bottom:10px;left:50%;border-left:1px dashed var(--sand-m)}")
R(".vs span{position:relative;margin-top:38px;",".vs span{position:relative;align-self:center;")
# 04 KPI
R(".kpi{flex:none;width:96px;border-right:1px solid var(--sand);padding-right:12px}",".kpi{flex:none;width:118px;border-right:1px solid var(--sand);padding-right:12px}")
R(".kl{margin-top:6px;font:600 13px/1.25 'Montserrat';color:var(--navy)}",".kl{margin-top:6px;font:600 14px/1.25 'Source Sans 3';color:var(--navy)}")
R(".tasks li{display:flex;align-items:center;gap:10px;height:25px;",".tasks li{display:flex;align-items:center;gap:10px;height:24px;")
# 06
R(".kpirow{display:flex;align-items:center;gap:12px;padding-bottom:9px;border-bottom:1px dotted var(--sand-m)}",".kpirow{display:flex;align-items:center;gap:12px;padding-bottom:6px;border-bottom:1px dotted var(--sand-m)}")
R(".kpirow .big{font-size:46px}",".kpirow .big{font-size:42px}\n.kpirow .kl{font-size:15px}")
R(".trig{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}",".trig{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin-top:9px}")
R("padding:7px 8px;\n  font:600 14.5px/1.15 'Source Sans 3';color:var(--navy);min-height:44px}","padding:6px 8px;\n  font:600 14.5px/1.15 'Source Sans 3';color:var(--navy);min-height:42px}")
# 07
R(".cyc{display:block;width:372px;height:206px;margin:auto 0}",".cyc{display:block;width:372px;height:178px;margin:auto 0}")
# Fuss
R(".foot{position:absolute;left:0;bottom:0;width:768px;height:80px;background:var(--navy);color:#d9cfbb;padding:13px 32px 0}",".foot{position:absolute;left:0;bottom:0;width:768px;height:88px;background:var(--navy);color:#d9cfbb;padding:13px 32px 0}")
R(""".frow{display:flex;align-items:center;gap:12px;font:400 13.5px/1.3 'Source Sans 3';color:#ece4d3}
.frow .lbl{color:#f0a066;flex:none}
.frow svg{width:16px;height:16px;flex:none}
.frow i{font-style:normal;color:#8d9ab0}""",""".frow{display:flex;align-items:flex-start;gap:10px;font:400 13.5px/1.3 'Source Sans 3';color:#ece4d3}
.frow .lbl{color:#f0a066;flex:none;width:92px;padding-top:2px}
.frow svg{width:16px;height:16px;flex:none}
.frow ul{list-style:none;flex:1}
.frow li{position:relative;padding-left:12px}
.frow li::before{content:"";position:absolute;left:0;top:7px;width:5px;height:5px;background:#e8762f}""")
R('<div class="frow"><svg><use href="#g-info"/></svg><span class="lbl">Hinweise</span><span>Kein Hirnscan kann ADHS diagnostizieren, es gibt nur Gruppenunterschiede.</span><i>|</i><span>Die Diagnose gehört zu Fachleuten.</span></div>',
  '<div class="frow"><svg><use href="#g-info"/></svg><span class="lbl">Hinweise</span><ul><li>Kein Hirnscan kann ADHS diagnostizieren, es gibt nur Gruppenunterschiede.</li><li>Die Diagnose gehört zu Fachleuten.</li></ul></div>')
R(".src{margin-top:9px;padding-top:8px;",".src{margin-top:7px;padding-top:7px;")
open('professional.html','w',encoding='utf-8').write(s)
print("ok")
