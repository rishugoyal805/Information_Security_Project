from fastapi import APIRouter, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from crypto_utils import encrypt_message, decrypt_message

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 🔐 Hardcoded users
users = {"user1": "pass1", "user2": "pass2"}

# 📨 In-memory message store
chat_store = {
    "user1": [],
    "user2": []
}

# ✅ Login page
@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 🔐 Login form handler
@router.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if users.get(username) == password:
        return RedirectResponse(f"/chat/{username}", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

# 💬 Chat page for user
@router.get("/chat/{username}", response_class=HTMLResponse)
def chat_interface(request: Request, username: str):
    if username not in users:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("chat.html", {"request": request, "username": username, "other": "user2" if username == "user1" else "user1"})

# 📤 Send message (text)
@router.post("/send")
async def send_message(sender: str = Form(...), receiver: str = Form(...), message: str = Form(...)):
    encrypted = encrypt_message(message)
    chat_store[receiver].append(encrypted)
    return {"status": "sent"}

# 📤 Send image message
@router.post("/send-image")
async def send_image(sender: str = Form(...), receiver: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    filename = f"{sender}_to_{receiver}_{file.filename}"
    path = f"static/{filename}"
    with open(path, "wb") as f:
        f.write(contents)
    encrypted = encrypt_message(f"[IMAGE]{filename}")
    chat_store[receiver].append(encrypted)
    print("🔐 Encrypted Image Msg to Send:", encrypted)
    return {"status": "image_sent", "url": f"/static/{filename}"}

# 📥 Receive & decrypt all messages
@router.get("/receive")
async def receive_messages(user: str):
    messages = chat_store[user]
    chat_store[user] = []
    decrypted = []
    for m in messages:
        msg = decrypt_message(m)
        if msg.startswith("[IMAGE]"):
            decrypted.append({"type": "image", "content": msg[7:]})
        else:
            decrypted.append({"type": "text", "content": msg})
    return {"messages": decrypted}

@router.get("/decrypt-image")
async def decrypt_image(msg: str):
    try:
        # If message is already decrypted (i.e., just a filename), return as-is
        if msg.endswith(".jpg") or msg.endswith(".png") or "/" in msg:
            return {"path": msg}

        # Otherwise, decrypt
        decrypted = decrypt_message(msg)
        if decrypted.startswith("[IMAGE]"):
            return {"path": decrypted[7:]}
        return {"path": "placeholder.png"}
    except Exception as e:
        print("❌ Decrypt Error:", e)
        return {"path": "placeholder.png"}

