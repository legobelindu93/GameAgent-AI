import importlib.util
import json
import platform
import sys

def main():
    print(json.dumps({"python":sys.version,"platform":platform.platform(),"optional_modules":{x:importlib.util.find_spec(x) is not None for x in ["tkinter","cv2","numpy","gymnasium","stable_baselines3","rapidocr","onnxruntime"]}},indent=2))

if __name__=="__main__":
    main()
