"""Transcribe authorized local footage and sample frames for manual annotation."""
from pathlib import Path
import json

def transcribe(video,model="small"):
    from faster_whisper import WhisperModel
    p=Path(video)
    if not p.is_file():raise ValueError("Missing media")
    engine=WhisperModel(model,device="cpu",compute_type="int8")
    segments,info=engine.transcribe(str(p),vad_filter=True)
    return {"language":info.language,"segments":[{"start":s.start,"end":s.end,"text":s.text.strip()} for s in segments]}

def frames(video,output,interval=2.0,limit=300):
    import cv2
    if interval<=0 or not 1<=limit<=3000:raise ValueError("Invalid sampling limits")
    out=Path(output)
    out.mkdir(parents=True,exist_ok=False)
    cap=cv2.VideoCapture(str(video))
    rows=[]
    try:
        fps=cap.get(cv2.CAP_PROP_FPS)
        if not cap.isOpened() or fps<=0:raise ValueError("Invalid video")
        stride=max(1,round(fps*interval))
        i=0
        while len(rows)<limit:
            ok,frame=cap.read()
            if not ok:break
            if i%stride==0:
                name=f"frame_{i:08d}.jpg"
                if not cv2.imwrite(str(out/name),frame):raise OSError("Cannot save frame")
                rows.append({"file":name,"time":i/fps,"action":None})
            i+=1
    finally:cap.release()
    (out/"annotations.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    return rows
