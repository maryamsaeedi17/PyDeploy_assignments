from fastapi import FastAPI , Form , File , UploadFile , HTTPException
from fastapi.responses import StreamingResponse , FileResponse
import cv2
import numpy as np
import io

app = FastAPI()

@app.post("/rgb2gray")
async def rgb2gray(input_file: UploadFile = File(None)):
    if not input_file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail= "Unsupported file type!")
    
    contents = await input_file.read()
    np_array = np.frombuffer(contents, dtype=np.uint8)
    img_rgb = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

    # cv2.imwrite("test.jpg", img_rgb)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    _, encoded_img = cv2.imencode(".png", img_gray)
    img_bytes = encoded_img.tobytes()
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")