import re
s=open('professional.html',encoding='utf-8').read()
def R(a,b,n=1):
    global s
    c=s.count(a); assert c==n,(c,a[:80]); s=s.replace(a,b)
# Gehirn: Windungen neu, etwas groesser
old=re.search(r'<g stroke="#f8f4eb" stroke-width="3.2".*?</g>',s,flags=re.S).group(0)
new='''<g stroke="#f8f4eb" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M80 0 C70 30 76 56 66 80 C60 96 62 110 54 170"/>
        <path d="M112 14 C104 28 116 38 106 52 C98 62 108 72 98 90"/>
        <path d="M60 102 C78 92 96 100 112 92 C126 85 138 90 150 82"/>
        <path d="M84 120 C98 112 112 120 126 112 C136 107 146 112 158 106"/>
        <path d="M80 42 C88 36 94 46 102 40"/>
        <path d="M76 68 C84 62 90 72 99 66"/>
        <path d="M126 36 C138 28 152 32 158 44 C163 54 156 62 166 70"/>
        <path d="M118 62 C128 56 136 66 148 60"/>
        <path d="M178 58 C170 68 180 78 172 90"/>
        <path d="M38 62 C46 68 54 58 64 64"/>
        <path d="M34 86 C42 90 50 82 58 88"/>
        <path d="M50 38 C56 46 62 40 70 44"/>
      </g>'''
s=s.replace(old,new)
R(".badge svg{position:absolute;left:13px;top:21px;width:118px;height:100px}",".badge svg{position:absolute;left:8px;top:16px;width:128px;height:109px}")
# Auge statt Scheinwerfer
old=re.search(r'<symbol id="i-spot".*?</symbol>',s,flags=re.S).group(0)
s=s.replace(old,'''<symbol id="i-spot" viewBox="0 0 48 48">
      <path d="M2 24 C9 13 16 8.5 24 8.5 C32 8.5 39 13 46 24 C39 35 32 39.5 24 39.5 C16 39.5 9 35 2 24 Z" fill="#2d4d79"/>
      <path d="M2 24 H46 C39 35 32 39.5 24 39.5 C16 39.5 9 35 2 24 Z" fill="#1a3356"/>
      <circle cx="24" cy="24" r="11" fill="#f8f4eb"/>
      <circle cx="24" cy="24" r="8" fill="#e8762f"/>
      <circle cx="24" cy="24" r="3.8" fill="#1a3356"/>
      <circle cx="27" cy="20.6" r="1.8" fill="#f8f4eb"/>
    </symbol>''')
# 02 Aussagen vertikal mittig
R(".col p{margin-top:12px;font-size:16.5px;line-height:1.36;hyphens:manual}",".col p{margin:auto 0;padding-top:8px;font-size:16.5px;line-height:1.36;hyphens:manual}")
open('professional.html','w',encoding='utf-8').write(s); print('ok')
