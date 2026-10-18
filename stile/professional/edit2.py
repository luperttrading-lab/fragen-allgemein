import re
s=open('professional.html',encoding='utf-8').read()
cyc='''<svg class="cyc" viewBox="0 0 372 178">
      <ellipse cx="186" cy="92" rx="130" ry="68" fill="none" stroke="#cbbd9f" stroke-width="1" stroke-dasharray="2 4"/>
      <g fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
        <path stroke="#1a3356" marker-end="url(#ah)" d="M249.2 32.6 L253.0 33.7 L256.7 34.9 L260.3 36.2 L263.8 37.5 L267.3 38.9 L270.6 40.4 L273.9 41.9 L277.1 43.5 L280.1 45.1 L283.1 46.8 L285.9 48.5 L286.6 49.0"/>
        <path stroke="#1a3356" marker-end="url(#ah)" d="M316.0 93.0 L315.8 95.3 L315.6 97.6 L315.1 99.9 L314.6 102.1 L313.8 104.4 L313.0 106.6 L312.0 108.8 L310.8 111.0 L309.5 113.2 L308.1 115.4 L306.5 117.5 L304.8 119.6 L303.0 121.7 L301.0 123.7 L299.7 125.0"/>
        <path stroke="#1a3356" marker-end="url(#ah)" d="M199.2 159.6 L194.9 159.8 L190.5 160.0 L186.1 160.0 L181.8 160.0 L177.4 159.9 L172.8 159.6"/>
        <path stroke="#1a3356" marker-end="url(#ah)" d="M72.3 125.0 L70.2 123.0 L68.3 120.9 L66.5 118.8 L64.9 116.7 L63.4 114.6 L62.0 112.4 L60.7 110.2 L59.7 108.0 L58.7 105.8 L57.9 103.5 L57.2 101.3 L56.7 99.0 L56.3 96.7 L56.0 93.0"/>
        <path stroke="#e8762f" stroke-dasharray="5 4" marker-end="url(#aho)" d="M85.4 49.0 L88.2 47.2 L91.1 45.5 L94.1 43.9 L97.3 42.3 L100.5 40.8 L103.9 39.3 L107.3 37.9 L110.8 36.5 L114.4 35.2 L118.1 34.0 L122.8 32.6"/>
      </g>
      <use href="#i-clock" x="159" y="65" width="54" height="54"/>
      <g font-family="Source Sans 3" font-weight="600" font-size="14.5" text-anchor="middle">
        <rect x="130.0" y="9.0" width="112" height="30" rx="15" fill="#f8f4eb" stroke="#1a3356" stroke-width="1.5"/>
        <text x="186.0" y="29.0" fill="#1a3356">Aufschieben</text>
        <rect x="253.6" y="56.0" width="112" height="30" rx="15" fill="#f8f4eb" stroke="#1a3356" stroke-width="1.5"/>
        <text x="309.6" y="76.0" fill="#1a3356">Deadline naht</text>
        <rect x="206.4" y="132.0" width="112" height="30" rx="15" fill="#e8762f"/>
        <text x="262.4" y="152.0" fill="#fff">Stress</text>
        <rect x="53.6" y="132.0" width="112" height="30" rx="15" fill="#1a3356"/>
        <text x="109.6" y="152.0" fill="#f8f4eb">Arbeitsphase</text>
        <rect x="6.4" y="56.0" width="112" height="30" rx="15" fill="#f8f4eb" stroke="#1a3356" stroke-width="1.5"/>
        <text x="62.4" y="76.0" fill="#1a3356">Erleichterung</text>
      </g>
      <text x="122" y="20" font-family="Source Sans 3" font-weight="600" font-style="italic" font-size="14" fill="#c75d1e" text-anchor="end">wieder von vorn</text>
    </svg>'''
s,n=re.subn(r'<svg class="cyc".*?</svg>',cyc,s,flags=re.S); assert n==1
brain='''<div class="badge">
  <svg viewBox="0 0 200 170">
    <defs>
      <clipPath id="cb"><path id="bp" d="M52 112 C34 108 26 90 34 76 C26 60 36 40 54 36 C60 20 80 12 98 18 C112 8 136 10 148 22 C166 20 182 34 182 52 C194 62 194 82 184 92 C188 108 176 122 160 122 C154 132 140 136 128 130 C118 138 100 138 92 130 C80 136 62 130 58 120 C55 118 53 115 52 112 Z"/></clipPath>
      <clipPath id="cf"><path d="M0 0 H80 C70 30 76 56 66 80 C60 96 62 110 54 170 H0 Z"/></clipPath>
    </defs>
    <path d="M110 124 C116 140 118 152 121 164 L136 162 C132 150 132 138 135 124 Z" fill="#12243f"/>
    <ellipse cx="152" cy="131" rx="27" ry="17" fill="#2d4d79"/>
    <path d="M152 114 A27 17 0 0 1 152 148 Z" fill="#1a3356"/>
    <g stroke="#f8f4eb" stroke-width="2.6" fill="none" stroke-linecap="round"><path d="M134 138 C146 135 160 135 174 139"/><path d="M139 145 C148 143 158 143 167 145"/></g>
    <g clip-path="url(#cb)">
      <rect width="200" height="170" fill="#1a3356"/>
      <path d="M0 0 H200 V52 L0 88 Z" fill="#2d4d79"/>
      <g clip-path="url(#cf)">
        <rect width="200" height="170" fill="#c75d1e"/>
        <path d="M0 0 H200 V52 L0 88 Z" fill="#e8762f"/>
      </g>
      <g stroke="#f8f4eb" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M80 0 C70 30 76 56 66 80 C60 96 62 110 54 170"/>
        <path d="M60 104 C78 94 96 100 112 92 C124 86 136 90 148 84"/>
        <path d="M100 16 C92 30 104 40 96 54 C90 64 98 72 90 88"/>
        <path d="M118 26 C126 34 116 44 124 54"/>
        <path d="M146 24 C138 36 152 44 144 58 C140 66 148 72 142 82"/>
        <path d="M110 66 C118 60 128 68 136 62"/>
        <path d="M168 44 C160 56 172 64 164 76 C160 84 168 92 162 104"/>
        <path d="M84 120 C98 112 112 120 126 112 C134 108 142 112 150 108"/>
        <path d="M40 58 C48 64 56 54 66 60"/>
        <path d="M34 84 C42 88 50 80 60 86"/>
        <path d="M52 36 C58 44 64 38 72 42"/>
      </g>
    </g>
    <use href="#bp" fill="none" stroke="#f8f4eb" stroke-width="2.4"/>
  </svg>
</div>'''
s,n=re.subn(r'<div class="badge">.*?</div>',brain,s,count=1,flags=re.S); assert n==1
open('professional.html','w',encoding='utf-8').write(s)
print('ok')
