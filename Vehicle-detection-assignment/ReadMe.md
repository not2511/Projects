
# Vehicle Classification Project

This project classifies vehicle images into 12 categories using a fine-tuned ResNet18 model.

##  Folder Structure

```
final_deliverables/
├── model/
│   ├── vehicle_classifier.pth
│   └── vehicle_classifier.onnx
│
├── scripts/
│   ├── train_model.py
│   ├── dataloader_setup.py
│   ├── evaluate_model.py
│   ├── export_onnx.py
│   └── verify_model.py
│
├── verification_images/
│   ├── autorickshaw.png
│   ├── car.png
│   └── van.png
│
├── outputs/
│   ├── loss_curve.png
│   ├── confusion_matrix.png
│   └── sample_predictions/
│       ├── pred_car.png
│       ├── pred_van.png
│       └── pred_autorickshaw.png
│
├── sample_classes.txt
├── README.md
└── Report.docx
```

##  Setup Instructions

### 1. Create virtual environment and activate it
```bash
python -m venv venv
venv\Scripts\activate   
```

### 2. Install required packages
```bash
pip install torch torchvision onnx onnxruntime scikit-learn matplotlib opencv-python tqdm
```

##  Training the Model
```bash
python scripts/train_model.py
```

##  Exporting to ONNX
```bash
python scripts/export_onnx.py
```

##  Verifying ONNX model
```bash
python scripts/verify_model.py -m model/vehicle_classifier.onnx -c sample_classes.txt -s 224
```

##  Evaluation
- Check `outputs/loss_curve.png` and `outputs/confusion_matrix.png`
- Check prediction outputs in `outputs/sample_predictions/`

---
**Author**: Ranjot Singh  
**GPU Used**: GTX 1650 Mobile  
**Model**: ResNet18 (Fine-tuned)
