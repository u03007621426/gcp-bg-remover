import io
from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image

app = FastAPI(title="Background Remover API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))
    output_image = remove(input_image, model_name="u2netp")  # lighter model
    bio = io.BytesIO()
    output_image.save(bio, format="PNG")
    bio.seek(0)
    return Response(
        content=bio.getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=no_bg.png"}
    )

@app.get("/")
async def root():
    return {"message": "GCP Background Remover API Ready!"}
