# 🕵️‍♂️ **Facebook Scraper Bot**

A Facebook scraping bot using `undetected-chromedriver`, `selenium`, and `pyautogui`.  
Compatible with **Windows, macOS, Ubuntu, Debian, and Fedora**.

---

⚠️ **Disclaimer:** This project is for educational purposes only.  
Scraping Facebook without permission may violate its Terms of Service.  
The author is not responsible for any misuse of this tool.

---

## 📋 **Prerequisites**

Before starting, make sure you have the following installed:  

✅ **Required:**  
- **Python** (3.8 or later) ➜ [Download Python](https://www.python.org/downloads/)  
- **Google Chrome** ➜ [Download Chrome](https://www.google.com/chrome/)  

✅ **Only for Linux (Ubuntu/Debian/Fedora):**  
`PyAutoGUI` requires additional packages to control the mouse and keyboard. Install them before running the bot:

- **Ubuntu/Debian**:  
  ```bash
  sudo apt update
  sudo apt install x11-utils xclip xserver-xorg-input-evdev -y
  ```
- **Fedora**:  
  ```bash
  sudo dnf install xorg-x11-server-Xvfb xclip xorg-x11-xauth -y
  ```

Then, ensure that your X11 session allows access:  
```bash
xhost +local:
export DISPLAY=:0
```

ℹ️ **Windows/macOS** do not require additional configuration.

---

## 🛠 **Installation**

### 1️⃣ **Clone the project**
```bash
git clone https://github.com/Thomas-soft/Facebook-Scrapping.git
cd facebook-scraper
```

### 2️⃣ **Create a virtual environment (recommended)**
📌 **(Optional but recommended to avoid dependency conflicts)**  
```bash
python -m venv env
source env/bin/activate  # macOS / Linux
env\Scripts\activate     # Windows
```

### 3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Set up the `.env` file**
Create your `.env` file from the example template:
```bash
cp .env.example .env  # macOS / Linux
copy .env.example .env  # Windows (cmd)
```
Then edit `.env` with your Facebook credentials:
```env
FACEBOOK_LOGIN="your_email_or_phone"
FACEBOOK_PASSWORD="your_password"
```

---

## 🚀 **Running the Bot**

### 1️⃣ **Start the bot**
```bash
python src/main.py
```
✅ **Everything runs automatically, no need to start ChromeDriver manually!**  

---

## 🛑 **Troubleshooting**

### ✅ **Chrome doesn't launch**
If Chrome does not start on Linux, run these commands:
```bash
export DISPLAY=:0
xhost +local:
```
If you are using **Wayland (Fedora, Ubuntu 22.04+)**, try running your script with:
```bash
env --unset=WAYLAND_DISPLAY python src/main.py
```

### ✅ **Error: `options.binary_location`**
If Chrome is not located at `/usr/bin/google-chrome`, find its path using:
```bash
which google-chrome  # Linux/macOS
where chrome         # Windows (cmd)
```
Then update this line in `main.py`:
```python
options.binary_location = "/path/to/google-chrome"
```

### ✅ **PyAutoGUI is not working on Linux**
Ensure you have installed the required packages:
```bash
sudo apt install x11-utils xclip xserver-xorg-input-evdev -y  # Ubuntu/Debian
sudo dnf install xorg-x11-server-Xvfb xclip xorg-x11-xauth -y  # Fedora
```
Then allow access to the X server:
```bash
xhost +local:
export DISPLAY=:0
```

---

## 🔄 **Using Docker (Optional)**
If you prefer to use Docker, follow these steps:

### 1️⃣ **Build the Docker image**
```bash
docker build -t facebook-scraper .
```

### 2️⃣ **Run the container**
```bash
docker run --env-file .env facebook-scraper
```

---

## 🔗 **Useful Links**
- 📌 [Download ChromeDriver](https://sites.google.com/chromium.org/driver/)
- 📌 [Python Downloads](https://www.python.org/downloads/)

---

## 📄 **License**
This project is licensed under the MIT License.

---

## 🎯 **Author**
- **Developed by**: [Thomas-soft](https://github.com/Thomas-soft)
- **Contact**: dev.thomas.soft+git@gmail.com
