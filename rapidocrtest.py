import platform

import cv2
from rapidocr import RapidOCR

cur_window_version_str = platform.release().split(".")[0]
cur_window_version = int(cur_window_version_str) if cur_window_version_str.isdigit() else 0
print(f'xxxxx cur_window_version_str="{cur_window_version_str}"')

engine = RapidOCR(params={"Global.lang_det": "ch_mobile", "Global.lang_rec": "ch_mobile", "Global.use_cls": False,
                          "EngineConfig.onnxruntime.use_dml": True})

img = cv2.imread('tests/images/end_battle.png')
# img = cv2.resize(img, (1280, 720))
for i in range(20):
    result = engine(img, use_cls=False)
    print(result.elapse)
# print(result)
