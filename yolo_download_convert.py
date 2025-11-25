from ultralytics import YOLO

print("Downloading YOLO11n model...")
model = YOLO('yolo11n.pt')  # This will auto-download if not present

print("Exporting to ONNX format...")
model.export(format="onnx", imgsz=320)

print("Export complete! yolo11n.onnx created")
