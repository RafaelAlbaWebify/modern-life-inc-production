#!/usr/bin/env python3
"""Prepare/check a reviewable YouTube handoff. Never uploads or publishes."""
import argparse,datetime,hashlib,importlib.util,json,math,pathlib,re,shutil,subprocess,sys

def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(p,data):pathlib.Path(p).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def digest(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def normalize(s):return re.sub('[^a-z0-9]','',s.lower())
def probe(p):
    r=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)],capture_output=True,text=True,check=True)
    return json.loads(r.stdout)
def safe(root,name):
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError('Package path escapes root')
    return p
def validate_text(plan):
    if plan.get('format')!='MLI_PUBLISH_PLAN_V1':raise ValueError('Wrong plan format')
    title=plan.get('title','').strip();body=plan.get('description','').strip()
    if not title or len(title)>100 or any(c in title for c in '<>'):raise ValueError('Invalid title')
    if not body or len(body)>5000 or any(c in body for c in '<>'):raise ValueError('Invalid description')
    if not plan.get('thumbnail_source'):raise ValueError('Thumbnail source missing')
    return title,body
def chapters(plan,manifest,duration):
    rows=plan.get('chapters',[])
    if not rows:
        if not plan.get('chapters_omission_reason'):raise ValueError('Chapters or explicit omission reason required')
        return []
    if len(rows)<3:raise ValueError('Chapters require at least three entries')
    offsets={x['scene']:x['timeline_start'] for x in manifest['scenes']};out=[]
    for row in rows:
        if row['scene'] not in offsets or not row.get('title','').strip():raise ValueError('Unknown chapter scene or empty title')
        sec=math.floor(offsets[row['scene']]+1e-6)
        if sec<0 or sec>=duration or (out and sec-out[-1]['seconds']<10):raise ValueError('Invalid chapter order/spacing')
        out.append({'seconds':sec,'title':row['title'].strip(),'scene':row['scene']})
    if out[0]['seconds']!=0 or duration-out[-1]['seconds']<10:raise ValueError('First chapter must start at zero; final chapter >=10s')
    return out
def timecode(sec):
    n=int(sec);h,n=divmod(n,3600);m,s=divmod(n,60)
    return f'{h}:{m:02}:{s:02}' if h else f'{m:02}:{s:02}'
def srt_stamp(sec):
    n=round(sec*1000);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,ms=divmod(n,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
def validate_thumbnail(p):
    if p.stat().st_size>2*1024*1024:raise ValueError('Thumbnail exceeds project portable 2MiB budget')
    info=probe(p);v=next(x for x in info['streams'] if x['codec_type']=='video')
    if v['codec_name'] not in ('png','mjpeg'):raise ValueError('Thumbnail must decode as PNG/JPEG')
    w,h=v['width'],v['height']
    if w<1280 or h<720 or abs(w/h-16/9)>.01:raise ValueError('Project thumbnail profile requires >=1280x720 near 16:9')
    return {'width':w,'height':h,'codec':v['codec_name'],'bytes':p.stat().st_size}
def alignment_words(alignment,contract,manifest,duration):
    if alignment.get('episode')!=contract['episode_id'] or not alignment.get('word_aligned'):raise ValueError('Wrong/non-word alignment')
    ids=[s['id'] for s in contract['scenes']]
    if ids!=[x['scene'] for x in manifest['scenes']] or ids!=[x['scene'] for x in alignment['scenes']]:raise ValueError('Alignment scene mismatch')
    words=alignment.get('words',[])
    if not words or any(w.get('scene') not in ids for w in words):raise ValueError('Unknown/missing aligned word scene')
    for s in contract['scenes']:
        ws=[w for w in words if w['scene']==s['id']]
        if normalize(' '.join(w['word'] for w in ws))!=normalize(s['beat']):raise ValueError('Alignment transcript mismatch')
    last=-1
    for w in words:
        start,end=w['start'],w['end']
        if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in (start,end)) or not 0<=start<end<=duration+.05 or start<last-.02:raise ValueError('Invalid word timing/order')
        last=start
    return words
def prepare(a):
    work=pathlib.Path(a.work).resolve();folder=pathlib.Path(a.render_folder).resolve();plan_path=pathlib.Path(a.plan).resolve()
    plan=read(plan_path);title,body=validate_text(plan);contract=read(work/'contract.json');m=read(folder/'manifest.json');f=read(folder/'finishing_manifest.json');qc=read(folder/'technical_qc.json')
    if plan.get('episode')!=contract['episode_id'] or m['episode_id']!=contract['episode_id'] or f['episode']!=contract['episode_id']:raise ValueError('Episode mismatch')
    if not qc.get('technical_pass') or qc.get('issues'):raise ValueError('Technical QC not passed')
    video=safe(folder,f['final_video'])
    if digest(video)!=f['sha256']:raise ValueError('Final video hash mismatch')
    duration=float(probe(video)['format']['duration'])
    if abs(duration-m['duration'])>.5:raise ValueError('Final timeline differs from master')
    alignment=read(folder/'alignment.json');words=alignment_words(alignment,contract,m,duration);chs=chapters(plan,m,duration)
    chapter_text='\n'.join(timecode(x['seconds'])+' '+x['title'] for x in chs)
    description=body+('\n\nCHAPTERS\n'+chapter_text if chs else '')
    if len(description)>5000:raise ValueError('Description plus chapters exceeds 5000 characters')
    thumb=pathlib.Path(plan['thumbnail_source']);thumb=thumb if thumb.is_absolute() else plan_path.parent/thumb
    thumb_info=validate_thumbnail(thumb)
    out=pathlib.Path(a.out).resolve() if a.out else work/'publication'
    if out.exists() and any(out.iterdir()):raise ValueError('Use an empty/new output folder; previous package preserved')
    out.mkdir(parents=True,exist_ok=True)
    name='thumbnail'+thumb.suffix.lower();shutil.copy2(thumb,out/name)
    module=pathlib.Path(__file__).with_name('mli-caption-styles.py');spec=importlib.util.spec_from_file_location('mli_caption_styles',module);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    lines=[]
    for i,g in enumerate(mod.groups(words),1):
        split=mod.split_line(g);parts=[w['word'] for w in g];text=' '.join(parts) if split is None else ' '.join(parts[:split])+'\n'+' '.join(parts[split:])
        lines.append(f'{i}\n{srt_stamp(g[0]["start"])} --> {srt_stamp(g[-1]["end"])}\n{text}\n\n')
    (out/'captions.en.srt').write_text(''.join(lines),encoding='utf-8')
    (out/'title.txt').write_text(title+'\n',encoding='utf-8');(out/'description.txt').write_text(description+'\n',encoding='utf-8');(out/'pinned_comment.txt').write_text(plan.get('pinned_comment','').strip()+'\n',encoding='utf-8')
    write(out/'chapters.json',chs)
    upload={'episode':contract['episode_id'],'title':title,'description':description,'tags':plan.get('tags',[]),'language':'en','category_proposal':plan.get('category_proposal','Education'),'playlist_proposal':plan.get('playlist_proposal'),'thumbnail':name,'captions':'captions.en.srt','settings_to_confirm':plan.get('settings_to_confirm',{}),'end_screen_plan':plan.get('end_screen_plan',{}),'upload_performed':False,'publication_approved':False}
    write(out/'youtube_upload.json',upload)
    checklist='# Publication handoff\n\nPrepared, not uploaded or published. Review title/thumbnail together.\n\n- [ ] Confirm target channel and exact title/thumbnail.\n- [ ] Confirm audience, AI disclosure (including narrator), paid promotion, rights and monetization eligibility in Studio.\n- [ ] Upload initially as private; attach thumbnail and English SRT.\n- [ ] Confirm playlist; preview chapters, captions and mobile thumbnail.\n- [ ] Inspect platform checks and processing; preview end screen without covering faces/captions.\n- [ ] Choose visibility/schedule explicitly and authorize publication.\n- [ ] Verify actual public URL, thumbnail, title, audio and captions after publication.\n- [ ] Post prepared pinned comment only when authorized.\n- [ ] Record 24h, 72h and 7d analytics when available; no automatic reminders created.\n\nA website/shop is optional and never blocks the episode. Do not insert invented channel/shop/video URLs.\n'
    (out/'PUBLISH_CHECKLIST.md').write_text(checklist,encoding='utf-8')
    (out/'POST_PUBLICATION.md').write_text('# After publication\n\nRecord actual video ID/URL, publication time, chosen title/thumbnail and audience settings. Check impressions, CTR, first-30-second retention, average minutes viewed, traffic sources and subscribers at comparable ages. Revenue/RPM only if available. Do not attribute performance to packaging alone. A website episode card uses only the real published URL; optional short-form clips need their own framing/caption review.\n',encoding='utf-8')
    shutil.copy2(plan_path,out/'publish_plan.json')
    files={p.name:digest(p) for p in out.iterdir() if p.is_file()}
    write(out/'package_manifest.json',{'format':'MLI_PUBLISH_PACKAGE_V1','episode':contract['episode_id'],'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'video_source':str(video),'video_sha256':f['sha256'],'duration_seconds':duration,'thumbnail_info':thumb_info,'files':files,'source_plan_sha256':digest(plan_path),'source_alignment_sha256':digest(folder/'alignment.json'),'upload_performed':False,'publication_approved':False})
    check_folder(out)
    print('PUBLICATION PACKAGE:',out,'NO UPLOAD OR PUBLICATION')
def check_folder(out):
    out=pathlib.Path(out).resolve();m=read(out/'package_manifest.json')
    if m.get('format')!='MLI_PUBLISH_PACKAGE_V1':raise ValueError('Wrong package format')
    for name,expected in m['files'].items():
        if digest(safe(out,name))!=expected:raise ValueError('Package file hash mismatch: '+name)
    u=read(out/'youtube_upload.json');thumb=safe(out,u['thumbnail']);validate_thumbnail(thumb)
    if u.get('episode')!=m['episode'] or not 1<=len(u['title'])<=100 or len(u['description'])>5000:raise ValueError('Invalid metadata')
    if u.get('upload_performed') or u.get('publication_approved'):raise ValueError('Preparation cannot claim publication')
    write(out/'publication_check.json',{'assets_ready_for_review':True,'release_authorized':False,'upload_performed':False,'publication_approved':False,'remaining':'Confirm exact packaging, channel/settings and publication instruction; then verify actual upload.'})
    print('ASSET CHECK PASS; RELEASE NOT AUTHORIZED')
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','check']);p.add_argument('--work');p.add_argument('--render-folder');p.add_argument('--plan');p.add_argument('--out');a=p.parse_args()
    if a.command=='prepare':
        if not all([a.work,a.render_folder,a.plan]):p.error('prepare requires --work --render-folder --plan')
        prepare(a)
    else:
        if not a.out:p.error('check requires --out')
        check_folder(a.out)
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAILED:',e,file=sys.stderr);sys.exit(1)
