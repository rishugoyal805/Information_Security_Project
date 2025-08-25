from fastapi import APIRouter, UploadFile, File, Form
from PIL import Image
import io

router = APIRouter()

@router.post("/stego/upload")
async def stego_upload(file: UploadFile = File(...), message: str = Form(...)):
    img = Image.open(io.BytesIO(await file.read()))
    binary_msg = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
    data = list(img.getdata())
    new_data, idx = [], 0
    for pixel in data:
        if idx < len(binary_msg):
            new_pixel = tuple((ch & ~1 | int(binary_msg[idx + i]) if idx + i < len(binary_msg) else ch) for i, ch in enumerate(pixel))
            new_data.append(new_pixel)
            idx += len(pixel)
        else:
            new_data.append(pixel)
    img.putdata(new_data)
    out_path = f"static/stego_{file.filename}"
    img.save(out_path)
    encrypted_path = f"[IMAGE]{out_path}"
    return {"url": f"/{out_path}", "encrypted": encrypted_path}

@router.post("/stego/decode")
async def decode_stego(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read()))
    binary = ''.join(str(ch & 1) for px in list(img.getdata()) for ch in px)
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        if c == '11111110': break
        message += chr(int(c, 2))
    return {"message": message}