"""Import only matching episode WAVs; preserve existing files and source audio."""
import argparse, hashlib, json, pathlib, shutil, wave

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',required=True)
    parser.add_argument('--audio-work',required=True)
    a=parser.parse_args();work=pathlib.Path(a.work).resolve();source=pathlib.Path(a.audio_work).resolve()
    contract=json.loads((work/'contract.json').read_text(encoding='utf-8-sig'))
    source_contract=json.loads((source/'contract.json').read_text(encoding='utf-8-sig'))
    if source_contract != contract:
        raise ValueError('Audio contract differs from this episode. No files copied.')
    out=work/'audio';pending=[]
    for scene in contract['scenes']:
        sid=scene['id'];file=source/'audio'/(sid+'.wav');dest=out/file.name
        with wave.open(str(file),'rb') as wav:
            if wav.getnchannels()!=1 or wav.getsampwidth() not in (2,4) or wav.getnframes()/wav.getframerate()<.3:
                raise ValueError('Invalid mono PCM WAV: '+sid)
        digest=hashlib.sha256(file.read_bytes()).hexdigest()
        if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()!=digest:
            raise ValueError('Conflicting existing audio, preserved: '+sid)
        pending.append((file,dest,digest))
    out.mkdir(exist_ok=True)
    for file,dest,digest in pending:
        if not dest.exists():shutil.copy2(file,dest)
    (work/'audio_import_receipt.json').write_text(json.dumps({'source_work':str(source),'episode':contract['episode_id'],'files':[{'scene':d.stem,'sha256':h} for _,d,h in pending],'source_unchanged':True},indent=2)+'\n')
    print('MATCHING AUDIO IMPORTED',len(pending))

if __name__=='__main__':main()
