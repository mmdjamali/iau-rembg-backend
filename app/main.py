import io
import os

import rembg
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps

load_dotenv()

app = FastAPI()

cors = os.getenv("CORS_ALLOW_ORIGIN", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"success": True}


@app.post("/api/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))

    # Remove background
    output_image = rembg.remove(input_image)

    # Save the output image to a bytes buffer
    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.post("/api/grayscale")
async def grayscale(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents)).convert("RGBA")
    r, g, b, a = input_image.split()

    gray_image = Image.merge("RGB", (r, g, b)).convert("L")

    output_image = Image.merge("LA", (gray_image, a))

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.post("/api/posterize")
async def posterize(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents)).convert("RGBA")
    r, g, b, a = input_image.split()

    rgb_image = Image.merge("RGB", (r, g, b))

    posterize_image = ImageOps.posterize(rgb_image, bits=2)

    r, g, b = posterize_image.split()

    output_image = Image.merge("RGBA", (r, g, b, a))

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.post("/api/solarize")
async def solarize(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents)).convert("RGBA")
    r, g, b, a = input_image.split()

    rgb_image = Image.merge("RGB", (r, g, b))

    solarized_image = ImageOps.solarize(rgb_image, threshold=50)

    r, g, b = solarized_image.split()

    output_image = Image.merge("RGBA", (r, g, b, a))

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.post("/api/invert")
async def invert(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents)).convert("RGBA")
    r, g, b, a = input_image.split()

    rgb_image = Image.merge("RGB", (r, g, b))

    inverted_image = ImageOps.invert(rgb_image)

    r, g, b = inverted_image.split()

    output_image = Image.merge("RGBA", (r, g, b, a))

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
