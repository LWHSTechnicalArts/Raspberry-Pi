# Run this once to export
from ultralytics import YOLO

model = YOLO("yolo11n-pose.pt")
model.export(format="onnx", imgsz=320)
print("Export complete!")
