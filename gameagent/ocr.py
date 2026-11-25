"""Optional offline OCR adapter; reads user-selected files only."""
from pathlib import Path

def read_text(path):
    from rapidocr import RapidOCR
    path=Path(path)
    if not path.is_file():
        raise ValueError("Image does not exist")
    output=RapidOCR()(str(path))
    texts=getattr(output,"txts",None)
    scores=getattr(output,"scores",None)
    if texts is None or scores is None:
        return []
    return [{"text":str(t),"confidence":float(s)} for t,s in zip(texts,scores)]
