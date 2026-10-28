import argparse,hashlib,json,pathlib,wave
p=argparse.ArgumentParser();p.add_argument('--audio-work',required=True);p.add_argument('--kit',required=True);a=p.parse_args()
work=pathlib.Path(a.audio_work);kit=pathlib.Path(a.kit)
contract=json.loads((work/'contract.json').read_text(encoding='utf-8-sig'))
expected=json.loads((kit/'contract.json').read_text(encoding='utf-8-sig'))
if contract!=expected:raise ValueError('Script contract mismatch')
m=json.loads((kit/'manifest.json').read_text(encoding='utf-8-sig'))
if [s['id'] for s in contract['scenes']] != [s['scene'] for s in m['scenes']]:raise ValueError('Scene order mismatch')
for row in m['scenes']:
    f=work/'audio'/(row['scene']+'.wav')
    if hashlib.sha256(f.read_bytes()).hexdigest()!=row['audio_sha256']:raise ValueError('Different audio: '+row['scene'])
    with wave.open(str(f),'rb') as w:
        if abs(w.getnframes()/w.getframerate()-row['audio_seconds'])>.02:raise ValueError('Audio length mismatch')
print('48 matching original WAVs and script verified; no media regenerated.')
