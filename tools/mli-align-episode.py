#!/usr/bin/env python3
"""Real episode word alignment, with validated reuse before loading WhisperX."""
import argparse,hashlib,json,math,pathlib,re,subprocess,sys

def probe(path):
 p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr)
 return float(p.stdout.strip())

def stamp(sec):
 n=round(sec*1000);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,ms=divmod(n,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'

def normalize(text):return re.sub(r'[^a-z0-9]','',text.lower())

def validate_alignment(data,contract,manifest,work):
 scenes=contract['scenes'];clips=manifest['scenes']
 if data.get('episode')!=contract['episode_id'] or not data.get('word_aligned'):raise ValueError('Wrong episode or non-word-aligned input')
 ids=[s['id'] for s in scenes]
 if ids!=[s['scene'] for s in clips] or ids!=[s['scene'] for s in data['scenes']]:raise ValueError('Alignment scene order mismatch')
 if not data.get('words') or any(w.get('scene') not in ids for w in data['words']):raise ValueError('Missing/unknown word scene')
 for scene,clip,aligned in zip(scenes,clips,data['scenes']):
  sid=scene['id'];wav=work/'audio'/(sid+'.wav');duration=probe(wav);digest=hashlib.sha256(wav.read_bytes()).hexdigest()
  if abs(duration-clip['audio_seconds'])>0.02 or abs(duration-aligned['audio_duration'])>0.02:raise ValueError('Audio duration mismatch: '+sid)
  for recorded in [clip.get('audio_sha256'),aligned.get('audio_sha256')]:
   if recorded and recorded!=digest:raise ValueError('Audio hash mismatch: '+sid)
  if abs(aligned['offset']-clip['timeline_start'])>0.04:raise ValueError('Timeline mismatch: '+sid)
  words=[w for w in data['words'] if w['scene']==sid]
  if normalize(' '.join(w['word'] for w in words))!=normalize(scene['beat']):raise ValueError('Transcript mismatch: '+sid)
  for w in words:
   start=w.get('start');end=w.get('end')
   if not isinstance(start,(int,float)) or not isinstance(end,(int,float)) or not math.isfinite(start) or not math.isfinite(end) or not clip['timeline_start']-0.0001<=start<end<=clip['timeline_start']+duration+0.25:raise ValueError('Invalid aligned word: '+sid)
 return True

def write_alignment(folder,data):
 target=folder/'alignment.json';temp=folder/'alignment.pending.json'
 temp.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');temp.replace(target)
 lines=[f"{i}\n{stamp(w['start'])} --> {stamp(w['end'])}\n{w['word']}\n\n" for i,w in enumerate(data['words'],1)]
 (folder/'captions_words.srt').write_text(''.join(lines),encoding='utf-8')

def reuse_alignment(source,folder,contract,manifest,work):
 data=json.loads(source.read_text(encoding='utf-8-sig'))
 validate_alignment(data,contract,manifest,work)
 source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
 # Keep real word stamps unchanged; reuse provenance is a separate sidecar.
 write_alignment(folder,data)
 (folder/'alignment_reuse.json').write_text(json.dumps({'source':str(source),'source_sha256':source_sha,'word_count':len(data['words']),'word_times_unchanged':True,'legacy_input_without_audio_hashes':any(not s.get('audio_sha256') for s in data['scenes'])},indent=2)+'\n',encoding='utf-8')
 print('REUSED REAL ALIGNMENT',source,len(data['words']),'words')
 return data

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--work',required=True);parser.add_argument('--render-folder',required=True);parser.add_argument('--reuse-from')
 args=parser.parse_args();work=pathlib.Path(args.work).resolve();folder=pathlib.Path(args.render_folder).resolve()
 contract=json.loads((work/'contract.json').read_text(encoding='utf-8'));manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
 scenes=contract['scenes']
 if [s['id'] for s in scenes]!=[s['scene'] for s in manifest['scenes']]:raise ValueError('Scene order mismatch')
 source=pathlib.Path(args.reuse_from).expanduser().resolve() if args.reuse_from else folder/'alignment.json'
 if source.is_file():
  reuse_alignment(source,folder,contract,manifest,work)
  return
 if args.reuse_from:raise FileNotFoundError(source)
 try:import whisperx
 except ImportError as error:raise RuntimeError('WhisperX not installed in selected Python environment') from error
 model,meta=whisperx.load_align_model(language_code='en',device='cpu');words=[];report=[]
 for scene,clip in zip(scenes,manifest['scenes']):
  sid=scene['id'];wav=work/'audio'/(sid+'.wav');length=probe(wav);sound=whisperx.load_audio(str(wav))
  result=whisperx.align([{'start':0,'end':length,'text':scene['beat']}],model,meta,sound,'cpu',return_char_alignments=False)
  segment_words=[w for w in result['word_segments'] if w.get('word','').strip()]
  if not segment_words:raise ValueError('Missing aligned words: '+sid)
  for w in segment_words:
   start=w.get('start');end=w.get('end')
   if not isinstance(start,(int,float)) or not isinstance(end,(int,float)) or not math.isfinite(start) or not math.isfinite(end) or not 0<=start<end<=length+0.25:raise ValueError(f'Unaligned word for {sid}: {w}')
   words.append({'scene':sid,'word':w['word'].strip(),'start':round(start+clip['timeline_start'],4),'end':round(end+clip['timeline_start'],4)})
  report.append({'scene':sid,'word_count':len(segment_words),'audio_duration':length,'offset':clip['timeline_start'],'audio_sha256':hashlib.sha256(wav.read_bytes()).hexdigest()})
  print('ALIGNED',sid,len(segment_words),'words',flush=True)
 data={'episode':contract['episode_id'],'word_aligned':True,'scenes':report,'words':words,'publication_approved':False}
 validate_alignment(data,contract,manifest,work);write_alignment(folder,data)
 print('ALIGNED TOTAL',len(words),'words')
if __name__=='__main__':
 try:main()
 except Exception as error:print('FAILED:',error,file=sys.stderr);sys.exit(1)
