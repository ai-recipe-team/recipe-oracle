from ultralytics import YOLO

# Load YOLOv8 model 
model = YOLO("yolov8n.pt")

def detect_objects(image_path):
    """
    Uses YOLOv8 to detect objects in an image.
    Returns a list of dictionaries with 'class' and 'confidence' keys.
    """
    results = model(image_path)
    detected_items = []

    for box in results[0].boxes:
        class_id = int(box.cls[0].item())
        class_name = results[0].names[class_id]
        confidence = float(box.conf[0].item())
        detected_items.append({
            "class": class_name,
            "confidence": confidence
        })

    return detected_items
