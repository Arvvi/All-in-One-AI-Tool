# Proper AI Tool - PDF Chat 🚀

**Proper AI Tool** is a fast, lightweight, and modern web application that allows you to chat directly with your PDF documents using Google's **Gemini AI** and **ChromaDB**. Just upload your PDF, wait a few seconds, and start asking questions! 

---

## ✨ Features
- **Upload Any PDF:** Automatically extracts text and creates intelligent vector embeddings.
- **Smart Answers:** Uses `gemini-3-flash-preview` to answer questions based *strictly* on your uploaded document.
- **Fast Vector Search:** Powered by **ChromaDB** for lightning-fast semantic search.
- **Modern UI:** A clean, responsive, and distraction-free frontend (ChatGPT style) built with HTML, CSS, and JS.
- **Chat History:** Automatically saves your recent conversations using **SQLite** so you can revisit them anytime.
- **No API Rate Limit Errors:** Smart time delays built-in to prevent `429 Too Many Requests` errors from Gemini API.

---

## 🛠️ Tech Stack
**Backend:**
- Python 3.x
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance backend framework.
- [Google GenAI](https://ai.google.dev/) - Embeddings & Text Generation.
- [ChromaDB](https://www.trychroma.com/) - Local Vector Database.
- [SQLAlchemy](https://www.sqlalchemy.org/) & SQLite - Chat History Database.
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF text extraction.

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript (No heavy frameworks required).

---

## 🚀 Installation & Setup

### 1. Prerequisites
Make sure you have **Python 3.8+** installed on your machine.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/proper-ai-tool.git
cd proper-ai-tool
```

### 3. Install Required Packages
Install the required backend libraries using pip:
```bash
pip install fastapi uvicorn pydantic google-genai chromadb sqlalchemy PyPDF2 python-multipart
```

### 4. Setup Gemini API Key
In your backend Python code (`main.py`), make sure to replace the dummy API key with your actual **Google Gemini API Key**:
```python
ai_client = genai.Client(api_key="YOUR_ACTUAL_API_KEY_HERE")
```

---

## 💻 How to Run the App

### Step 1: Start the Backend (FastAPI)
Open your terminal/command prompt, navigate to the project folder, and run:
```bash
uvicorn main:app
```
*(The backend will start running locally at `http://127.0.0.1:8000`)*

### Step 2: Open the Frontend
- **Do NOT** use VS Code "Live Server" (it auto-refreshes the page when the SQLite database updates).
- Simply go to your project folder in your File Manager.
- **Double-click** on the `frontend_final.html` (or `index.html`) file to open it directly in Google Chrome or any modern browser.

---

## 💡 Usage Guide
1. **Upload:** Click on the "Upload PDF" button in the sidebar and select a PDF file. 
2. **Wait:** Give it a moment to extract and vectorize the text (time depends on the PDF size). A success message will appear.
3. **Chat:** Type your question in the chat box at the bottom and hit "Send" or press Enter.
4. **History:** Your past questions will appear in the sidebar. Click on them to view the conversation.

---

## 🛑 Troubleshooting

**1. "CORS / Network Error" when clicking upload:**
- Ensure your backend is running (`uvicorn main:app`).
- Check your `main.py` file to ensure `allow_origins=["*"]` is set inside `CORSMiddleware`.

**2. Chat panel clears out after pressing Enter:**
- Ensure you are opening the HTML file directly (`file:///C:/...`) and **not** through an auto-reloading local server like VS Code Live Server.
- Ensure the `frontend_final.html` has `translate="no"` in the `<html>` tag to prevent Google Translate from crashing the DOM.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/proper-ai-tool/issues).

## 📜 License
This project is licensed under the [MIT License](LICENSE).
