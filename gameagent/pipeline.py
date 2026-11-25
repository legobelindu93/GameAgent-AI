"""Declarative recognition-only pipelines for saved images."""
import json
from pathlib import Path

def inspect(image, config):
    from .vision import match_template
    from .ocr import read_text
    config=Path(config).resolve()
    rules=json.loads(config.read_text(encoding="utf-8"))
    if not isinstance(rules,list) or len(rules)>100:
        raise ValueError("Invalid rules")
    results={}
    for rule in rules:
        name=rule["id"]
        if name in results:
            raise ValueError("Duplicate rule id")
        if rule["type"]=="template":
            template=(config.parent / rule["template"]).resolve()
            if not template.is_relative_to(config.parent):
                raise ValueError("Template escapes profile")
            results[name]=match_template(image,template,float(rule.get("threshold",0.8)))
        elif rule["type"]=="ocr":
            results[name]=read_text(image)
        else:
            raise ValueError("Unsupported recognition type")
    return results
