from pathlib import Path
from PIL import Image, UnidentifiedImageError
import os

dataset_root = Path("vehicle_dataset/train")

bad_images = []

for class_dir in dataset_root.iterdir():
    if not class_dir.is_dir():
        continue
    for img_path in class_dir.glob("*"):
        try:
            with Image.open(img_path) as img:
                img.verify()  # checking the file integrity
                if img.size[0] == 0 or img.size[1] == 0:
                    raise ValueError("Zero-dimension image")
        except (UnidentifiedImageError, OSError, ValueError) as e:
            print(f"Bad image: {img_path} | Error: {e}")
            bad_images.append(img_path)

for path in bad_images:
    os.remove(path)
    print(f"Deleted: {path}")
