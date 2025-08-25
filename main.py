# # Secure Communication Suite (Minimal Single File Version for Two Users)

# from fastapi import FastAPI, Form, Request, UploadFile, File
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# from PIL import Image
# import base64, io, os

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# # In-memory message and file store
# chat_store = {
#     "user1": [],  # messages sent by user1 to user2
#     "user2": []   # messages sent by user2 to user1
# }

# # Hardcoded credentials
# USERS = {
#     "user1": "pass1",
#     "user2": "pass2"
# }

# # AES Key and IV
# KEY = b'ThisIsASecretKey'
# IV = b'ThisIsAnIV456789'

# def encrypt_message(msg):
#     cipher = AES.new(KEY, AES.MODE_CBC, IV)
#     return base64.b64encode(cipher.encrypt(pad(msg.encode(), AES.block_size))).decode()

# def decrypt_message(enc):
#     cipher = AES.new(KEY, AES.MODE_CBC, IV)
#     return unpad(cipher.decrypt(base64.b64decode(enc)), AES.block_size).decode()

# @app.post("/send-image")
# async def send_image(sender: str = Form(...), receiver: str = Form(...), file: UploadFile = File(...)):
#     contents = await file.read()
#     filename = f"{sender}_to_{receiver}_{file.filename}"
#     path = f"static/{filename}"
#     with open(path, "wb") as f:
#         f.write(contents)
#     # store image path as encrypted message
#     encrypted = encrypt_message(f"[IMAGE]{filename}")
#     chat_store[receiver].append(encrypted)
#     return {"status": "image_sent", "url": f"/static/{filename}"}

# @app.get("/receive")
# async def receive_messages(user: str):
#     messages = chat_store[user]
#     chat_store[user] = []
#     decrypted = []
#     for m in messages:
#         msg = decrypt_message(m)
#         if msg.startswith("[IMAGE]"):
#             decrypted.append({"type": "image", "content": msg[7:]})
#         else:
#             decrypted.append({"type": "text", "content": msg})
#     return {"messages": decrypted}

# @app.get("/", response_class=HTMLResponse)
# async def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @app.post("/login", response_class=HTMLResponse)
# async def login(request: Request, username: str = Form(...), password: str = Form(...)):
#     if USERS.get(username) == password:
#         return templates.TemplateResponse("chat.html", {"request": request, "user": username})
#     return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

# @app.post("/send")
# async def send_message(sender: str = Form(...), receiver: str = Form(...), message: str = Form(...)):
#     encrypted = encrypt_message(message)
#     chat_store[receiver].append(encrypted)
#     return {"status": "sent"}

# @app.get("/decrypt-image")
# async def decrypt_image(msg: str):
#     decrypted = decrypt_message(msg)
#     if decrypted.startswith("[IMAGE]"):
#         filename = decrypted[7:]
#         return {"path": filename}
#     return {"path": "placeholder.png"}

# @app.get("/receive")
# async def receive_messages(user: str):
#     messages = chat_store[user]
#     chat_store[user] = []
#     decrypted = [decrypt_message(m) for m in messages]
#     return {"messages": decrypted}

# @app.post("/stego/upload")
# async def stego_upload(file: UploadFile = File(...), message: str = Form(...)):
#     img = Image.open(io.BytesIO(await file.read()))
#     binary_msg = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
#     data = list(img.getdata())
#     new_data, idx = [], 0
#     for pixel in data:
#         if idx < len(binary_msg):
#             new_pixel = tuple((ch & ~1 | int(binary_msg[idx + i]) if idx + i < len(binary_msg) else ch) for i, ch in enumerate(pixel))
#             new_data.append(new_pixel)
#             idx += len(pixel)
#         else:
#             new_data.append(pixel)
#     img.putdata(new_data)
#     out_path = f"static/stego_{file.filename}"
#     img.save(out_path)
#     return {"url": f"/{out_path}"}

# @app.post("/stego/decode")
# async def decode_stego(file: UploadFile = File(...)):
#     img = Image.open(io.BytesIO(await file.read()))
#     binary = ''.join(str(ch & 1) for px in list(img.getdata()) for ch in px)
#     chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
#     message = ''
#     for c in chars:
#         if c == '11111110': break
#         message += chr(int(c, 2))
#     return {"message": message}

# # Create required folders
# os.makedirs("static", exist_ok=True)
# os.makedirs("templates", exist_ok=True)

# # Templates
# with open("templates/login.html", "w") as f:
#     f.write('''<!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8" />
#   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#   <title>Login</title>
#   <script src="https://cdn.tailwindcss.com"></script>
# </head>
# <body class="bg-gray-100 flex items-center justify-center min-h-screen">
#   <div class="w-full max-w-sm p-6 bg-white rounded-xl shadow-md">
#     <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>
#     <form method="post" action="/login" class="space-y-4">
#       <div>
#         <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
#         <input name="username" id="username" required class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"/>
#       </div>
#       <div>
#         <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
#         <input type="password" name="password" id="password" required class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"/>
#       </div>
#       <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition duration-200">
#         Login
#       </button>
#     </form>
#     {% if error %}
#       <p class="text-red-500 text-sm mt-4 text-center">{{ error }}</p>
#     {% endif %}
#   </div>
# </body>
# </html>''')


# # with open("templates/chat.html", "w") as f:
# #     f.write('''<!DOCTYPE html>
# # <html lang="en">
# # <head>
# #   <meta charset="UTF-8" />
# #   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
# #   <title>Chat</title>
# #   <script src="https://cdn.tailwindcss.com"></script>
# #   <script>
# #     function sendMessage() {
# #       const form = document.getElementById('chat-form');
# #       const formData = new FormData(form);

# #       fetch('/send', {
# #         method: 'POST',
# #         body: formData
# #       }).then(() => {
# #         form.reset();
# #       });
# #     }

# #     function receiveMessages() {
# #       fetch('/receive?user={{ user }}')
# #         .then(res => res.json())
# #         .then(data => {
# #           const box = document.getElementById('msgs');
# #           box.innerHTML = '';
# #           data.messages.forEach(msg => {
# #             box.innerHTML += '<div class="mb-2 px-3 py-2 bg-blue-100 rounded w-fit max-w-xs">' + msg + '</div>';
# #           });
# #           box.scrollTop = box.scrollHeight;
# #         });
# #     }

# #     setInterval(receiveMessages, 10000);
# #   </script>
# # </head>
# # <body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
# #   <div class="w-full max-w-xl bg-white rounded-xl shadow-lg p-6">
# #     <h2 class="text-xl font-bold text-gray-800 mb-4 text-center">Welcome, {{ user }}</h2>
    
# #     <div id="msgs" class="border border-gray-300 h-64 overflow-y-auto p-3 rounded bg-gray-50 text-sm mb-4"></div>
    
# #     <form id="chat-form" class="flex items-center gap-2" onsubmit="event.preventDefault(); sendMessage();">
# #       <input type="hidden" name="sender" value="{{ user }}">
# #       <input type="hidden" name="receiver" value="{{ 'user1' if user=='user2' else 'user2' }}">

# #       <input name="message" required placeholder="Type a message..." 
# #              class="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />

# #       <button type="submit" 
# #               class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition duration-200">
# #         Send
# #       </button>
# #     </form>
# #   </div>
# # </body>
# # </html>''')
# # with open("templates/chat.html", "w") as f:
# #     f.write('''<!DOCTYPE html>
# # <html lang="en">
# # <head>
# #   <meta charset="UTF-8" />
# #   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
# #   <title>Chat</title>
# #   <script src="https://cdn.tailwindcss.com"></script>
# #   <script>
# #     function sendMessage() {
# #       const form = document.getElementById('chat-form');
# #       const formData = new FormData(form);
# #       fetch('/send', {
# #         method: 'POST',
# #         body: formData
# #       }).then(() => {
# #         form.reset();
# #         receiveMessages();
# #       });
# #     }

# #     function sendImage() {
# #       const form = document.getElementById('image-form');
# #       const formData = new FormData(form);
# #       fetch('/send-image', {
# #         method: 'POST',
# #         body: formData
# #       }).then(() => {
# #         form.reset();
# #         document.getElementById('preview').innerHTML = '';
# #         receiveMessages();
# #       });
# #     }

# #     function previewFile() {
# #       const fileInput = document.getElementById('file');
# #       const preview = document.getElementById('preview');
# #       preview.innerHTML = '';

# #       if (fileInput.files.length > 0) {
# #         const file = fileInput.files[0];
# #         const reader = new FileReader();
# #         if (file.type.startsWith('image/')) {
# #           reader.onload = function (e) {
# #             const img = document.createElement('img');
# #             img.src = e.target.result;
# #             img.className = "max-w-[150px] mt-2 rounded shadow";
# #             preview.appendChild(img);
# #           };
# #           reader.readAsDataURL(file);
# #         }
# #       }
# #     }

# #     function receiveMessages() {
# #       fetch('/receive?user={{ user }}')
# #         .then(res => res.json())
# #         .then(data => {
# #           const box = document.getElementById('msgs');
# #           data.messages.forEach(msg => {
# #             let html = '';
# #             if (msg.type === 'image') {
# #               html = '<img src="/static/' + msg.content + '" class="max-w-xs mb-2 rounded shadow"/>';
# #             } else {
# #               html = '<div class="mb-2 px-3 py-2 bg-blue-100 rounded w-fit max-w-xs">' + msg.content + '</div>';
# #             }
# #             box.innerHTML += html;
# #           });
# #           box.scrollTop = box.scrollHeight;
# #         });
# #     }

# #     setInterval(receiveMessages, 3000);
# #   </script>
# # </head>
# # <body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
# #   <div class="w-full max-w-xl bg-white rounded-xl shadow-lg p-6 space-y-4">
# #     <h2 class="text-xl font-bold text-gray-800 text-center">Welcome, {{ user }}</h2>

# #     <div id="msgs" class="border h-64 overflow-y-auto p-3 rounded bg-gray-50 text-sm"></div>

# #     <!-- Text Form -->
# #     <form id="chat-form" class="flex items-center gap-2" onsubmit="event.preventDefault(); sendMessage();">
# #       <input type="hidden" name="sender" value="{{ user }}">
# #       <input type="hidden" name="receiver" value="{{ 'user1' if user=='user2' else 'user2' }}">
# #       <input name="message" required placeholder="Type a message..." 
# #              class="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
# #       <button type="submit" 
# #               class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition duration-200">
# #         Send
# #       </button>
# #     </form>

# #     <!-- Image Upload Form -->
# #     <form id="image-form" class="space-y-2" onsubmit="event.preventDefault(); sendImage();" enctype="multipart/form-data">
# #       <input type="hidden" name="sender" value="{{ user }}">
# #       <input type="hidden" name="receiver" value="{{ 'user1' if user=='user2' else 'user2' }}">
# #       <input type="file" name="file" id="file" accept="image/*" onchange="previewFile()" 
# #              class="w-full border rounded p-2" required/>
# #       <div id="preview"></div>
# #       <button type="submit" 
# #               class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition">
# #         Send Image
# #       </button>
# #     </form>
# #   </div>
# # </body>
# # </html>''')
# with open("templates/chat.html", "w") as f:
#     f.write('''<!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8" />
#   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#   <title>Chat</title>
#   <script src="https://cdn.tailwindcss.com"></script>
#   <script>
#     function sendMessage() {
#       const form = document.getElementById('chat-form');
#       const formData = new FormData(form);
#       fetch('/send', {
#         method: 'POST',
#         body: formData
#       }).then(() => {
#         form.reset();
#         receiveMessages();
#       });
#     }

#     function sendImage() {
#       const form = document.getElementById('image-form');
#       const formData = new FormData(form);
#       fetch('/send-image', {
#         method: 'POST',
#         body: formData
#       }).then(() => {
#         form.reset();
#         document.getElementById('preview').innerHTML = '';
#         receiveMessages();
#       });
#     }

#     function previewFile() {
#       const fileInput = document.getElementById('file');
#       const preview = document.getElementById('preview');
#       preview.innerHTML = '';
#       if (fileInput.files.length > 0) {
#         const file = fileInput.files[0];
#         const reader = new FileReader();
#         if (file.type.startsWith('image/')) {
#           reader.onload = function (e) {
#             const img = document.createElement('img');
#             img.src = e.target.result;
#             img.className = "max-w-[150px] mt-2 rounded shadow";
#             preview.appendChild(img);
#           };
#           reader.readAsDataURL(file);
#         }
#       }
#     }

#     function revealImage(btn, encryptedPath) {
#       fetch('/decrypt-image?msg=' + encodeURIComponent(encryptedPath))
#         .then(res => res.json())
#         .then(data => {
#           const img = document.createElement('img');
#           img.src = '/static/' + data.path;
#           img.className = "max-w-xs mb-2 rounded shadow";
#           btn.parentElement.replaceWith(img);
#         });
#     }

#     function receiveMessages() {
#       fetch('/receive?user={{ user }}')
#         .then(res => res.json())
#         .then(data => {
#           const box = document.getElementById('msgs');
#           box.innerHTML = '';
#           data.messages.forEach(msg => {
#             let html = '';
#             if (msg.type === 'image') {
#               html = `
#                 <div class="flex flex-col items-start mb-3">
#                   <img src="/static/placeholder.png" class="w-40 h-28 object-cover rounded shadow-sm opacity-70 mb-1" />
#                   <button onclick="revealImage(this, '${msg.content}')" 
#                           class="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition">
#                     Show Image
#                   </button>
#                 </div>
#               `;
#             } else {
#               html = '<div class="mb-2 px-3 py-2 bg-blue-100 rounded w-fit max-w-xs">' + msg.content + '</div>';
#             }
#             box.innerHTML += html;
#           });
#           box.scrollTop = box.scrollHeight;
#         });
#     }

#     setInterval(receiveMessages, 3000);
#   </script>
# </head>
# <body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
#   <div class="w-full max-w-xl bg-white rounded-xl shadow-lg p-6 space-y-4">
#     <h2 class="text-xl font-bold text-gray-800 text-center">Welcome, {{ user }}</h2>

#     <div id="msgs" class="border h-64 overflow-y-auto p-3 rounded bg-gray-50 text-sm"></div>

#     <!-- Text Form -->
#     <form id="chat-form" class="flex items-center gap-2" onsubmit="event.preventDefault(); sendMessage();">
#       <input type="hidden" name="sender" value="{{ user }}">
#       <input type="hidden" name="receiver" value="{{ 'user1' if user=='user2' else 'user2' }}">
#       <input name="message" required placeholder="Type a message..." 
#              class="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
#       <button type="submit" 
#               class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition duration-200">
#         Send
#       </button>
#     </form>

#     <!-- Image Upload Form -->
#     <form id="image-form" class="space-y-2" onsubmit="event.preventDefault(); sendImage();" enctype="multipart/form-data">
#       <input type="hidden" name="sender" value="{{ user }}">
#       <input type="hidden" name="receiver" value="{{ 'user1' if user=='user2' else 'user2' }}">
#       <input type="file" name="file" id="file" accept="image/*" onchange="previewFile()" 
#              class="w-full border rounded p-2" required/>
#       <div id="preview"></div>
#       <button type="submit" 
#               class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition">
#         Send Image
#       </button>
#     </form>
#   </div>
# </body>
# </html>''')
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from auth import router as auth_router
from chat import router as chat_router
from stego import router as stego_router

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Page routes
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat")
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(stego_router)

# Ensure required dirs exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
