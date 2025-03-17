# 🕵️‍♂️ **Facebook Scraper Bot**

A Facebook scraping bot built with [`undetected-chromedriver`](https://github.com/ultrafunkamsterdam/undetected-chromedriver), [`selenium`](https://www.selenium.dev/), and [`pyautogui`](https://pyautogui.readthedocs.io/).  
Compatible with **Windows, macOS, Ubuntu, Debian, and Fedora**.

This bot not only scrapes Facebook posts but also:

-   Scrolls through the Facebook feed and clicks "See more" buttons (using an optimized 250px margin to ensure full content loads).
-   Extracts key post information (Author, Text, Images, Videos, External Links, Date) while avoiding duplicates.
-   Downloads images via Selenium by taking screenshots of `<img>` elements—saving them in separate CSV columns.
-   Opens the author's profile in a new tab (via a middle click), waits 1 second, then automatically closes the tab using keyboard shortcuts (Ctrl+W on Windows/Linux or Cmd+W on macOS).
-   Analyzes post content using an AI prompt to determine if the post relates to a website sale or purchase (blog, e-commerce, etc.).
    -   **Response Format:**
        -   If the post is an offer, the AI returns:
            ```json
            { "result": true }
            ```
        -   If it is not an offer, the AI returns:
            ```json
            { "result": false, "reason": "brief explanation" }
            ```
        -   _Note:_ Even if the post contains only a description (without explicit pricing or sales incentive) but originates from a website sales channel, it should be considered an offer.

---

⚠️ **Disclaimer:**  
This project is **for educational and research purposes only**.  
Scraping Facebook without explicit permission **may violate its Terms of Service**.  
It is the user’s responsibility to comply with local laws and platform policies.  
The author **does not endorse nor encourage** any misuse of this tool.

---

## 📋 **Prerequisites**

Before starting, ensure you have the following installed:

### ✅ **Required:**

-   **Python** (3.8 or later) ➜ [Download Python](https://www.python.org/downloads/)
-   **Google Chrome** ➜ [Download Chrome](https://www.google.com/chrome/)

### ✅ **For Linux (Ubuntu/Debian/Fedora) Only:**

`PyAutoGUI` requires additional packages to control the mouse and keyboard. Install them before running the bot:

-   **Ubuntu/Debian:**
    ```bash
    sudo apt update
    sudo apt install x11-utils xclip xserver-xorg-input-evdev -y
    ```
-   **Fedora:**
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

## ⚙️ **LM Studio & Local LM Server Setup**

For the AI analysis feature, LM Studio is required to run the language model locally. Follow these steps:

1. **Download and Install LM Studio:**

    - For **Debian/Ubuntu**: Download the LM Studio package and follow the Linux installation instructions.
    - For **Windows**: Download the Windows installer.
    - For **macOS**: Download the macOS version.  
      _(Refer to the [LM Studio Official Website](https://lmstudio.ai/) for detailed instructions.)_

2. **Download the Model:**

    - Download the desired model (e.g., `mathstral-7b-v0.1`) from its official repository or the provided link.

3. **Add the Model to the `.env` File:**  
   In addition to your Facebook credentials, add a variable in your `.env` file to specify which model to use. See the provided `.env.example` below.

4. **Launch the LM Studio Server Locally:**
    - Start LM Studio and load the downloaded model.
    - Ensure that the local LM server is running before starting the bot. The Facebook Scraper Bot will send requests to this local server for AI-based analysis.

This setup is required on all platforms: Debian, Ubuntu, Windows, macOS, etc.

---

## 🛠 **Installation**

### 1️⃣ **Clone the Project**

```bash
git clone https://github.com/Thomas-soft/Facebook-Scrapping.git
cd facebook-scraper
```

### 2️⃣ **Create a Virtual Environment (Recommended)**

_(Optional but recommended to avoid dependency conflicts)_

```bash
python -m venv env
source env/bin/activate  # macOS / Linux
env\Scripts\activate     # Windows
```

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Set up the `.env` File**

Create your `.env` file from the template provided by `.env.example`:

```bash
cp .env.example .env  # macOS / Linux
copy .env.example .env  # Windows (cmd)
```

Then, edit the `.env` file to include your credentials and LM model:

```env
# .env.example is a template file for the .env file
LOGIN=your-email-or-phone
PASSWORD=your-password
FACEBOOK_URL=url-of-facebook-website
FACEBOOK_GROUP_LINK=url-of-facebook-group
LM_MODEL=your-language-model
```

Replace the placeholders with your actual information.

---

## 🚀 **Running the Bot**

### 1️⃣ **Start the Bot**

```bash
python src/main.py
```

✅ **Everything runs automatically; you do not need to start ChromeDriver manually!**

---

## 🌟 **New Features & Functionality**

### Post Extraction & "See more" Handling

-   **Optimized Scrolling:** The bot scrolls the Facebook feed and checks post visibility using an increased margin (250px) to ensure "See more" buttons are visible. It clicks these buttons and loads the full post content.
-   **Duplicate Avoidance:** Posts are processed only once (using unique keys based on Author, Date, and Text), allowing periodic execution without adding duplicates to the CSV.

### Author Tab Interaction

-   When processing a post, the bot performs a middle click on the author's element to open their profile in a new tab.
-   The bot automatically switches to the new tab, waits 1 second, then closes it using the appropriate keyboard shortcut (Ctrl+W on Windows/Linux or Cmd+W on macOS) before returning to the main tab.

### Image Downloading via Selenium

-   Instead of making separate HTTP requests, images are downloaded by loading the image URL in Selenium and taking a screenshot of the `<img>` element.
-   Images are saved in a dedicated folder (default: `images/`) and their local paths are updated in the CSV.
-   **CSV Columns:** Each image is stored in a separate column (e.g., `Downloaded_Image_1`, `Downloaded_Image_2`, etc.) so that multiple images per post are clearly separated.

### CSV Update & Duplicate Handling

-   The CSV file is updated with new posts and the local paths of downloaded images.
-   Duplicate posts (based on Author, Date, and Text) are automatically filtered out, which is especially useful when the bot is scheduled to run every 24 hours.

### Website Sales Offer Analysis (AI Prompt)

-   The bot includes a module that sends a prompt to an AI model (using the model specified in your `.env` file, e.g., `mathstral-7b-v0.1`) to analyze a post and determine if it relates to an offer to sell or buy a website (blog, e-commerce, etc.).
-   **Response Format:**
    -   If the post is an offer, the AI returns:
        ```json
        { "result": true }
        ```
    -   If it is not an offer, the AI returns:
        ```json
        { "result": false, "reason": "brief explanation" }
        ```
-   **Note:** The prompt accounts for posts coming from website sales channels—even if they only contain a description without explicit pricing or a call-to-sale.

Example payload for the AI analysis:

```python
payload = {
    "model": "mathstral-7b-v0.1",
    "messages": [
        {
            "role": "system",
            "content": (
                "You are an expert in analyzing website sale and purchase announcements. "
                "Analyze the following post to determine whether it is an offer related to the sale or purchase of a website (blog, e-commerce, etc.). "
                "Keep in mind that the post may come from a website sales channel, so even if it only contains a description mentioning a website without a specific price or explicit sales incentive, it may still be a sales post. "
                "If it is an offer, respond only with the JSON: {\"result\": true} without any additional explanation. "
                "If it is not an offer, respond with the JSON: {\"result\": false, \"reason\": \"brief explanation\"}."
            )
        },
        message_user
    ],
    "temperature": 0.2,
    "max_tokens": 50,
    "stream": False
}
```

---

## 🛑 **Troubleshooting**

### Chrome Doesn't Launch

If Chrome does not start on Linux, run these commands:

```bash
export DISPLAY=:0
xhost +local:
```

For **Wayland (Fedora, Ubuntu 22.04+)** users, try running:

```bash
env --unset=WAYLAND_DISPLAY python src/main.py
```

### Error: `options.binary_location`

If Chrome is not located at `/usr/bin/google-chrome`, find its path:

```bash
which google-chrome  # Linux/macOS
where chrome         # Windows (cmd)
```

Then update in `main.py`:

```python
options.binary_location = "/path/to/google-chrome"
```

### PyAutoGUI Not Working on Linux

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

If you prefer Docker, follow these steps:

### 1️⃣ **Build the Docker Image**

```bash
docker build -t facebook-scraper .
```

### 2️⃣ **Run the Container**

```bash
docker run --env-file .env facebook-scraper
```

---

## 🔗 **Useful Links**

-   [Download ChromeDriver](https://sites.google.com/chromium.org/driver/)
-   [Python Downloads](https://www.python.org/downloads/)
-   [LM Studio Official Website](https://lmstudio.ai/)

---

## 📄 **License**

This project is licensed under the MIT License.

---

## 🎯 **Author**

-   **Developed by**: [Thomas-soft](https://github.com/Thomas-soft)
-   **Contact**: dev.thomas.soft+git@gmail.com

---

Feel free to adapt or extend this README as the project evolves or based on user feedback.
