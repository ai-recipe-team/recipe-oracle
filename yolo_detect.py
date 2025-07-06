import torch

def detect_objects(image_path):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    results = model(image_path)
    labels = results.xyxyn[0][:, -1].cpu().numpy()
    label_names = results.names
    detected_items = [label_names[int(label)] for label in labels]
    return [{"class": item, "confidence": 0.9} for item in detected_items]