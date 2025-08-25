# Info_sec_project

## Overview

**Info_sec_project** is a Python-based application focused on demonstrating essential information security concepts. The project implements core security mechanisms such as authentication, cryptography, and steganography, and provides a user-friendly interface for interacting with these features. It is designed for learning and experimenting with security techniques.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [File Descriptions](#file-descriptions)
- [Contact](#contact)

---

## Features

- **Authentication:** Basic user authentication system.
- **Cryptography:** Implementation of cryptographic utilities for data protection.
- **Steganography:** Hide and extract information within images.
- **Chat Functionality:** Secure chat interface.
- **Web Interface:** HTML templates and static resources for user interaction.

---

## Project Structure

```
.
├── .gitignore
├── .python-version
├── auth.py
├── chat.py
├── crypto_utils.py
├── main.py
├── pyproject.toml
├── static/
├── stego.py
├── templates/
└── README.md
```

- `auth.py`: Implements authentication logic.
- `chat.py`: Manages chat functionality.
- `crypto_utils.py`: Handles cryptographic operations.
- `main.py`: Main entry point for running the application.
- `stego.py`: Functions for steganography.
- `static/`: Contains static assets (CSS, JS, images).
- `templates/`: HTML templates for the web interface.
- `.python-version`: Specifies Python version.
- `pyproject.toml`: Project metadata and dependencies.
- `.gitignore`: Files and folders to be ignored by Git.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SwayamGupta12345/Info_sec_project.git
   cd Info_sec_project
   ```

2. **Set up Python environment:**
   - Make sure you have Python 3.8+ installed.
   - (Optional) Use a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or, if using Poetry:
   ```bash
   poetry install
   ```

---

## Usage

1. **Run the main application:**
   ```bash
   python main.py
   ```
   This will start the web interface for interacting with the project's security features.

2. **Access the web interface:**
   - Open your browser and navigate to the address shown in your terminal after running the app.

---

## Configuration

- **Python Version:** This project uses the version specified in `.python-version`.
- **Project Metadata & Dependencies:** Managed via `pyproject.toml`.
- **Static and Template Files:** Located in the `static/` and `templates/` directories.

---

## File Descriptions

- **auth.py:** User login/logout and session management.
- **chat.py:** Handles real-time chat, likely with security features.
- **crypto_utils.py:** Provides encryption/decryption functions.
- **stego.py:** Hide messages within images and extract them.
- **main.py:** Entry point for the web application, ties together all modules.
- **static/:** CSS, JavaScript, images for frontend.
- **templates/:** HTML files rendered by Flask/Django or other frameworks.

---

## Contact

- **GitHub:** [SwayamGupta12345](https://github.com/SwayamGupta12345)
- **Email:**  swayamsam2005@gmail.com

For questions or suggestions, please open an issue in this repository.

---


