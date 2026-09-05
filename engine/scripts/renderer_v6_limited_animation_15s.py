from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, shutil, math

ROOT = Path(r"C:\ModernLifeInc")
EP = ROOT/"episodes"/"MLI-001"
POSES = ROOT/"assets"/"characters"/"dave"/"poses"
AUDIO = EP/"03_audio"/"narration.wav"
OUT = EP/"06_renders"/"tests"/"MLI-001_V6_LIMITED_ANIMATION_15s.mp4"
CONTACT = EP/"06_renders"/"tests"/"MLI-001_V6_LIMITED_ANIMATION_15s_contact.jpg"
TMP = ROOT/"temp"/"MLI001_v6_15s"

W,H,FPS,DUR = 1920,1080,30,15.0

def run(cmd):
    print(" ".join(str(x) for x in cmd))
    subprocess.run(cmd,check=True)

def font(sz,bold=False):
    cands = [
        Path(r"C:\Windows\Fonts\arialbd.ttf") if bold else Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf") if bold else Path(r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for p in cands:
        if p.exists(): return ImageFont.truetype(str(p),sz)
    return ImageFont.load_default()

def clamp(v,a=0,b=1): return max(a,min(b,v))
def ease(t): t=clamp(t); return 1-(1-t)*(1-t)
def back(t):
    t=clamp(t); c1=1.70158; c3=c1+1
    return 1+c3*(t-1)**3+c1*(t-1)**2

def load_pose(name,max_h=900):
    im=Image.open(POSES/name).convert("RGBA")
    bb=im.getbbox()
    if bb: im=im.crop(bb)
    scale=max_h/im.height
    return im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)

N=load_pose("dave_v6_neutral.png")
HAPPY=load_pose("dave_v6_happy_paycheck.png")
PANIC=load_pose("dave_v6_panic_bills.png")
EXH=load_pose("dave_v6_exhausted_coffee.png")

def simple_bg(kind):
    if kind=="office":
        base=Image.new("RGBA",(W,H),(240,245,245,255))
        d=ImageDraw.Draw(base)
        d.rectangle((0,760,W,H),fill=(205,215,220,255))
        d.rectangle((160,150,760,540),fill=(224,238,244,255),outline=(65,85,95,255),width=8)
        d.line((460,150,460,540),fill=(65,85,95,255),width=8)
        d.line((160,345,760,345),fill=(65,85,95,255),width=8)
        d.rectangle((1100,560,1810,770),fill=(180,130,95,255),outline=(60,45,35,255),width=8)
        return base
    if kind=="home":
        base=Image.new("RGBA",(W,H),(248,239,219,255))
        d=ImageDraw.Draw(base)
        d.rectangle((0,785,W,H),fill=(214,194,164,255))
        d.rectangle((1390,170,1760,700),fill=(205,223,230,255),outline=(70,75,70,255),width=8)
        d.rectangle((250,460,720,785),fill=(187,129,91,255),outline=(60,45,35,255),width=8)
        return base
    base=Image.new("RGBA",(W,H),(247,243,226,255))
    return base

def paste(base,im,x,y):
    a=im.getchannel("A")
    sh=Image.new("RGBA",im.size,(0,0,0,255))
    sh.putalpha(a.point(lambda p:int(p*.22)))
    sh=sh.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(sh,(x+14,y+18))
    base.alpha_composite(im,(x,y))

def draw_paycheck(base,x,y,scale=1.0):
    w,h=int(440*scale),int(235*scale)
    d=ImageDraw.Draw(base)
    d.rounded_rectangle((x,y,x+w,y+h),radius=26,fill=(239,250,230,255),outline=(55,95,65,255),width=7)
    d.text((x+28,y+20),"PAYCHECK",font=font(int(46*scale),True),fill=(40,70,55,255))
    d.text((x+28,y+100),"+7%",font=font(int(74*scale),True),fill=(55,145,75,255))

def draw_rent(base,x,y,scale=1.0):
    w,h=int(420*scale),int(520*scale)
    d=ImageDraw.Draw(base)
    d.rounded_rectangle((x,y,x+w,y+h),radius=24,fill=(255,248,235,255),outline=(90,65,55,255),width=8)
    d.rectangle((x+35,y+32,x+w-35,y+135),fill=(218,58,46,255))
    d.text((x+w/2,y+80),"RENT",font=font(int(70*scale),True),fill="white",anchor="mm")
    d.text((x+w/2,y+230),"$2,450",font=font(int(66*scale),True),fill=(45,45,45,255),anchor="mm")
    d.text((x+w/2,y+390),"DUE",font=font(int(76*scale),True),fill=(210,45,45,255),anchor="mm")

def draw_grocery_receipt(base,x,y,scale=1.0):
    w,h=int(390*scale),int(560*scale)
    d=ImageDraw.Draw(base)
    d.rectangle((x,y,x+w,y+h),fill=(255,255,248,255),outline=(75,75,75,255),width=6)
    d.text((x+w/2,y+40),"GROCERY",font=font(int(50*scale),True),fill=(45,85,55,255),anchor="ma")
    items=["MILK   $3.49","BREAD  $2.89","EGGS   $4.29","CHICKEN $7.99","VEGGIES $3.49"]
    yy=y+125
    for item in items:
        d.text((x+28,yy),item,font=font(int(30*scale)),fill=(45,45,45,255))
        yy += int(62*scale)
    d.line((x+24,y+h-110,x+w-24,y+h-110),fill=(70,70,70,255),width=4)
    d.text((x+w/2,y+h-72),"$32.29",font=font(int(55*scale),True),fill=(210,55,45,255),anchor="mm")

def pop_text(base,text,xy,size,p):
    if p<=0: return
    s=.7+.3*back(p)
    d=ImageDraw.Draw(base)
    f=font(max(18,int(size*s)),True)
    d.text(xy,text,font=f,fill=(250,245,225,255),anchor="mm",stroke_width=7,stroke_fill=(25,25,25,255))

def frame(t):
    # Scene 1: 0-3.4 neutral -> paycheck -> happy pose
    if t < 3.4:
        l=t
        b=simple_bg("office")
        pose=N if l<1.05 else HAPPY
        paste(b,pose,170,H-pose.height+12)
        p=clamp((l-.45)/.28)
        if p>0:
            x=int(W+40+(1240-(W+40))*back(p))
            draw_paycheck(b,x,370,1.0)
        pop_text(b,"+7%!",(1470,220),102,clamp((l-1.05)/.22))
        return b

    # Scene 2: 3.4-6.4 happy at home -> giant rent slides in -> panic
    if t < 6.4:
        l=t-3.4
        b=simple_bg("home")
        pose=HAPPY if l<1.0 else PANIC
        paste(b,pose,125,H-pose.height+12)
        p=clamp((l-.25)/.45)
        x=int(W+50+(1180-(W+50))*back(p))
        draw_rent(b,x,240,1.0)
        return b

    # Scene 3: 6.4-9.4 grocery receipt rises at checkout
    if t < 9.4:
        l=t-6.4
        b=simple_bg("plain")
        paste(b,PANIC,W-PANIC.width-120,H-PANIC.height+12)
        p=clamp((l-.2)/.45)
        y=int(H+80+(190-(H+80))*back(p))
        draw_grocery_receipt(b,170,y,1.0)
        return b

    # Scene 4: 9.4-12.3 rent + grocery close in
    if t < 12.3:
        l=t-9.4
        b=simple_bg("plain")
        paste(b,PANIC,(W-PANIC.width)//2,H-PANIC.height+12)
        lp=clamp((l-.1)/.45)
        rp=clamp((l-.45)/.45)
        rx=int(-460+(70+460)*back(lp)-460)
        gx=int(W+40+((W-440)-(W+40))*back(rp))
        draw_rent(b,rx,260,.92)
        draw_grocery_receipt(b,gx,240,.86)
        return b

    # Scene 5: 12.3-15 exhausted beat, bills still present
    l=t-12.3
    b=simple_bg("office")
    paste(b,EXH,170,H-EXH.height+10)
    draw_rent(b,1210,255,.78)
    p=clamp((l-.4)/.3)
    if p>0:
        draw_grocery_receipt(b,1510,370,.58+.08*ease(p))
    return b

def main():
    if TMP.exists():
        shutil.rmtree(TMP)
    frdir=TMP/"frames"
    frdir.mkdir(parents=True,exist_ok=True)
    total=int(DUR*FPS)
    for i in range(total):
        frame(i/FPS).convert("RGB").save(frdir/f"f_{i:05d}.jpg",quality=93,subsampling=0)
        if i%90==0: print("frame",i,"/",total)

    silent=TMP/"silent.mp4"
    run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(frdir/"f_%05d.jpg"),
         "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",str(silent)])

    run(["ffmpeg","-y","-i",str(silent),"-i",str(AUDIO),"-t",str(DUR),
         "-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000",
         "-af","loudnorm=I=-16:TP=-1.5:LRA=11","-movflags","+faststart",str(OUT)])

    run(["ffmpeg","-y","-i",str(OUT),"-vf","fps=1/1.5,scale=320:-1,tile=5x2",
         "-frames:v","1","-update","1",str(CONTACT)])

    print("DONE:",OUT)
    print("CONTACT:",CONTACT)

if __name__=="__main__":
    main()
