import torch
import torch.onnx
import torch.nn as nn
from torchvision import models

# set image size, square image only
image_size = 224  
dummy_input = torch.randn(1, 3, image_size, image_size)

# load model architecture and weights
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 12)  # 12 classes
model.load_state_dict(torch.load("vehicle_classifier.pth", map_location=torch.device("cpu")))

model = torch.nn.Sequential(model, torch.nn.Softmax(dim=1))
model.eval()

torch.onnx.export(
    model,
    dummy_input,
    "vehicle_classifier.onnx",  # new export path
    verbose=True,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=11
)
