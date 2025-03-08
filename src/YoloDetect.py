# Ultralytics YOLO 🚀, AGPL-3.0 license

import argparse
import os.path

import cv2.dnn
import numpy as np

from ok import Box

CLASSES = {0: 'tree'}
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    """
    Draws bounding boxes on the input image based on the provided arguments.

    Args:
        img (numpy.ndarray): The input image to draw the bounding box on.
        class_id (int): Class ID of the detected object.
        confidence (float): Confidence score of the detected object.
        x (int): X-coordinate of the top-left corner of the bounding box.
        y (int): Y-coordinate of the top-left corner of the bounding box.
        x_plus_w (int): X-coordinate of the bottom-right corner of the bounding box.
        y_plus_h (int): Y-coordinate of the bottom-right corner of the bounding box.
    """
    label = f"{CLASSES[class_id]} ({confidence:.2f})"
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def predict(onnx_model, input_image):
    """
    Main function to load ONNX model, perform inference, draw bounding boxes, and display the output image.

    Args:
        onnx_model (str): Path to the ONNX model.
        input_image (ndarray): Path to the input image.

    Returns:
        list: List of dictionaries containing detection information such as class_id, class_name, confidence, etc.
    """
    # Load the ONNX model
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnx_model)

    # Read the input image
    # original_image: np.ndarray = cv2.imread(input_image)
    original_image: np.ndarray = input_image
    [height, width, _] = original_image.shape

    # Prepare a square image for inference
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image

    # Calculate scale factor
    scale = length / 640

    # Preprocess the image and prepare blob for model
    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
    model.setInput(blob)

    # Perform inference
    outputs = model.forward()

    # Prepare output array
    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []

    # Iterate through output to collect bounding boxes, confidence scores, and class IDs
    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= 0.25:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]),
                outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2],
                outputs[0][i][3],
            ]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)

    # Apply NMS (Non-maximum suppression)
    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

    detections = []

    # Iterate through NMS results to draw bounding boxes and labels
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        my_box = Box(box[0], box[1], box[2], box[3], box[4])
        my_box.name = CLASSES[class_ids[index]]
        my_box.confidence = scores[index]
        detections.append(my_box)


    return detections


# if __name__ == "__main__":
#     print("hello")
#     parser = argparse.ArgumentParser()
#     from myutils.configutils import resource_path
#     bgi_tree_path = os.path.join(resource_path, 'model','bgi_tree.onnx')
#     parser.add_argument("--model", default=bgi_tree_path, help="Input your ONNX model.")
#     # parser.add_argument("--img", default=str(ASSETS / "bus.jpg"), help="Path to input image.")
#     parser.add_argument("--img", default="screenshot1.jpg", help="Path to input image.")
#     args = parser.parse_args()
#     from capture.windowcapture3 import WindowCapture
#     wc = WindowCapture()
#     while True:
#         img = wc.get_screenshot(use_alpha=False)
#         results = predict(args.model, img)
#         for result in results:
#             print(result)
#             box = result.get("box")
#             scale = result.get("scale")
#             x1 = round(box[0] * scale)
#             x2 = round(box[1] * scale)
#             y1 = round((box[0] + box[2]) * scale)
#             y2 = round((box[1] + box[3]) * scale)
#             print(x1,x2,y1,y2)

if __name__ == "__main__":
    # Create an argument parser to handle command-line arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--model", type=str, default="yolov8n.onnx", help="Input your ONNX model.")
    # parser.add_argument("--img", type=str, default=str(ASSETS / "bus.jpg"), help="Path to input image.")
    # parser.add_argument("--conf-thres", type=float, default=0.5, help="Confidence threshold")
    # parser.add_argument("--iou-thres", type=float, default=0.5, help="NMS IoU threshold")
    # args = parser.parse_args()

    # Check the requirements and select the appropriate backend (CPU or GPU)
    # check_requirements("onnxruntime-gpu" if torch.cuda.is_available() else "onnxruntime")

    # Create an instance of the YOLOv8 class with the specified arguments
    # detection = YOLOv8("assets/yolo/big_tree.onnx", , 0.01, 0.01)
    img = cv2.imread('tests/images/tree.png')
    results = predict("assets/yolo/big_tree.onnx", img)
    print(results)
    # Display the output image in a window
    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
    cv2.imshow("Output", img)
    #
    # # Wait for a key press to exit
    cv2.waitKey(0)

