import io
import os

import rembg
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image

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
