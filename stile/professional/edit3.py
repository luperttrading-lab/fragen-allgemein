s=open('professional.html',encoding='utf-8').read()
def R(a,b,n=1):
    global s
    c=s.count(a); assert c==n,(c,a[:80]); s=s.replace(a,b)
R(".head{position:absolute;left:0;top:0;width:768px;height:164px;",".head{position:absolute;left:0;top:0;width:768px;height:152px;")
R(".head-text{position:absolute;left:32px;top:34px;width:520px}",".head-text{position:absolute;left:32px;top:30px;width:520px}")
R("h1{font:700 54px/1 'Montserrat';",'h1{font:700 52px/1 \'Montserrat\';')
R(".sub{margin-top:14px;",".sub{margin-top:12px;")
R(".badge{position:absolute;left:574px;top:24px;width:156px;height:156px;",".badge{position:absolute;left:578px;top:14px;width:150px;height:150px;")
R(".badge svg{position:absolute;left:14px;top:22px;width:122px;height:104px}",".badge svg{position:absolute;left:13px;top:21px;width:118px;height:100px}")
R(".kern{position:absolute;left:32px;top:186px;",".kern{position:absolute;left:32px;top:174px;")
R("row-gap:12px;","row-gap:10px;")
R("padding:12px 14px 12px;overflow:hidden;","padding:11px 14px 11px;overflow:hidden;")
R("padding-bottom:9px;border-bottom:1px solid var(--sand);margin-bottom:10px;min-height:38px}","padding-bottom:7px;border-bottom:1px solid var(--sand);margin-bottom:8px;min-height:36px}")
R(".bl{list-style:none;margin-top:16px}",".bl{list-style:none;margin-top:13px}")
R(".tasks li{display:flex;align-items:center;gap:10px;height:24px;",".tasks li{display:flex;align-items:center;gap:10px;height:23px;")
R(".note{margin-top:8px;",".note{margin-top:7px;")
R(".qs li{display:flex;align-items:center;gap:9px;height:25px;",".qs li{display:flex;align-items:center;gap:9px;height:24px;")
R(".qhead{margin-top:12px}",".qhead{margin-top:9px}")
R(".state+.state{margin-top:7px}",".state+.state{margin-top:6px}")
R("height:88px;background:var(--navy);color:#d9cfbb;padding:13px 32px 0}","height:84px;background:var(--navy);color:#d9cfbb;padding:12px 32px 0}")
R('.cyc{display:block;width:372px;height:178px;margin:auto 0}','.cyc{display:block;width:372px;height:166px;margin:auto 0}')
R('<svg class="cyc" viewBox="0 0 372 178">','<svg class="cyc" viewBox="0 0 372 166">')
R(".scene+.scene{margin-top:8px;padding-top:8px;",".scene+.scene{margin-top:7px;padding-top:7px;")
# 02
R("grid-template-columns:minmax(0,1fr) 34px minmax(0,1fr);","grid-template-columns:minmax(0,5fr) 26px minmax(0,7fr);")
R(".myth p{color:#4f4a42}",".myth p{color:#4f4a42;font-size:15.5px}")
R(".col p{margin-top:12px;font-size:16.5px;line-height:1.36}",".col p{margin-top:12px;font-size:16.5px;line-height:1.36;hyphens:manual}")
R(".col{display:flex;flex-direction:column;border-radius:5px;padding:10px 11px 12px}",".col{display:flex;flex-direction:column;border-radius:5px;padding:10px 10px 12px}")
R(".vs span{position:relative;align-self:center;",".vs span{position:relative;z-index:1;align-self:center;")
# 06 als Liste
R('''    <div class="trig">
      <div><svg><use href="#r-new"/></svg>Neuheit</div>
      <div><svg><use href="#r-bolt"/></svg>Unmittelbare Konsequenzen</div>
      <div><svg><use href="#r-person"/></svg>Persönliches Interesse</div>
      <div><svg><use href="#r-hour"/></svg>Zeitdruck</div>
    </div>''','''    <ul class="tasks trig">
      <li><svg><use href="#r-new"/></svg>Neuheit</li>
      <li><svg><use href="#r-bolt"/></svg>Unmittelbare Konsequenzen</li>
      <li><svg><use href="#r-person"/></svg>Persönliches Interesse</li>
      <li><svg><use href="#r-hour"/></svg>Zeitdruck</li>
    </ul>''')
R(""".trig{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin-top:9px}
.trig div{display:flex;align-items:center;gap:8px;background:var(--paper-l);border:1px solid var(--sand);border-radius:4px;padding:6px 8px;
  font:600 14.5px/1.15 'Source Sans 3';color:var(--navy);min-height:42px}
.trig svg{width:22px;height:22px;flex:none}""",""".trig{flex:none;margin-top:6px}""")
open('professional.html','w',encoding='utf-8').write(s); print('ok')
