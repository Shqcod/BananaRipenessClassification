from fastapi import FastAPI, UploadFile, File
from PIL import Image
from pathlib import Path
import io

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn.functional as F

app = FastAPI()

# =========================
# DEVICE
# =========================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# =========================
# LABEL
# =========================

CLASS_NAMES = [
    "overripe",
    "ripe",
    "rotten",
    "unripe"
]

# =========================
# MODEL PATH
# =========================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR /
    "model" /
    "banana_ripeness_resnet18.pt"
)

# =========================
# BUILD RESNET18
# =========================

model = models.resnet18(weights=None)

for param in model.parameters():
    param.requires_grad = False

num_ftrs = model.fc.in_features

model.fc = nn.Linear(
    num_ftrs,
    4
)

# =========================
# LOAD WEIGHTS
# =========================

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.to(device)
model.eval()

# =========================
# TRANSFORM
# =========================

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# =========================
# API
# =========================

@app.get("/")
def home():
    return {
        "message":
        "Banana Ripeness Classification API"
    }

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    image_bytes = await file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)
    image_tensor = image_tensor.to(device)

    with torch.no_grad():

        outputs = model(image_tensor)

        probabilities = F.softmax(
            outputs,
            dim=1
        )

        confidence, predicted = torch.max(
            probabilities,
            dim=1
        )

    return {
        "label":
            CLASS_NAMES[predicted.item()],

        "confidence":
            round(
                confidence.item() * 100,
                2
            ),

        "probabilities": {
            CLASS_NAMES[i]:
                round(
                    probabilities[0][i].item() * 100,
                    2
                )
            for i in range(len(CLASS_NAMES))
        }
    }