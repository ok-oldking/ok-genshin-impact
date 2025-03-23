import cv2
from rapidocr import RapidOCR

engine = RapidOCR(params={"Global.lang_det": "ch_mobile", "Global.lang_rec": "ch_mobile", "Global.use_cls": False,
                          "EngineConfig.onnxruntime.use_dml": True})

img = cv2.imread('tests/images/end_battle.png')
img = cv2.resize(img, (1280, 720))
for i in range(20):
    result = engine(img, use_cls=False)
    print(result.elapse)
# print(result)
