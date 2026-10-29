"""Regenerate WY Wallet's original vector and raster app icons (requires Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw
import math

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" fill="none">
  <defs><linearGradient id="wy" x1="64" y1="0" x2="448" y2="512" gradientUnits="userSpaceOnUse"><stop stop-color="#254777"/><stop offset="1" stop-color="#0c1633"/></linearGradient></defs>
  <rect width="512" height="512" rx="128" fill="url(#wy)"/>
  <rect x="16" y="16" width="480" height="480" rx="116" stroke="#8ccaff" stroke-opacity=".22" stroke-width="2"/>
  <path d="m96 182 40 148 58-94 49 94 43-148" stroke="#fff" stroke-width="31" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="m307 182 54 75 55-75m-55 75v73" stroke="#64e7ee" stroke-width="31" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
for f in ('public/logo.svg','src/assets/logo.svg','src/assets/logoLight.svg','src/assets/logoMinimalistic.svg'):
    Path(f).write_text(SVG+'\n')
Path('src/util/injectedConnector/injectedIcon.ts').write_text('export const INJECTED_ICON = `'+SVG+'`;\n')
S=4; N=512*S
img=Image.new('RGBA',(N,N)); pix=img.load()
for y in range(N):
    for x in range(N):
        t=max(0,min(1,(x+y)/(2*N)))
        pix[x,y]=tuple(round(a+(b-a)*t) for a,b in zip((37,71,119),(12,22,51)))+(255,)
mask=Image.new('L',(N,N));ImageDraw.Draw(mask).rounded_rectangle((0,0,N-1,N-1),radius=128*S,fill=255);img.putalpha(mask)
d=ImageDraw.Draw(img);d.rounded_rectangle((16*S,16*S,496*S,496*S),radius=116*S,outline=(92,152,195,180),width=2*S)
def stroke(points,color):
    pts=[(x*S,y*S) for x,y in points];w=31*S
    d.line(pts,fill=color,width=w,joint='curve')
    r=w/2
    for x,y in pts:d.ellipse((x-r,y-r,x+r,y+r),fill=color)
stroke([(96,182),(136,330),(194,236),(243,330),(286,182)],'white')
stroke([(307,182),(361,257),(416,182)],'#64e7ee');stroke([(361,257),(361,330)],'#64e7ee')
def save(p,size):img.resize((size,size),Image.Resampling.LANCZOS).save(p)
for size in (16,32,128,192,384,512):save(f'public/icon-{size}x{size}.png',size)
for p,size in [('public/icon.png',1024),('public/apple-touch-icon.png',180),('public/mstile-150x150.png',150),('src/assets/logo.webp',320)]:save(p,size)
img.resize((256,256),Image.Resampling.LANCZOS).save('public/favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print('WY logo and app icons generated')
