# Chatbot AI Azure

**Chatbot AI Azure** is an intelligent, multilingual web application built with Python and Microsoft Azure services. It helps users detect potential **scams, hoaxes, and online gambling promotions** by analyzing suspicious text messages. Users simply paste the message, and the system returns a classification, explanation, sentiment, and confidence level.

---

## 🚀 Features

- 🧠 Detects **scams**, **hoaxes**, and **online gambling promotions**
- 🌐 Supports multi-language input (Indonesian, English, Arabic, and more)
- 🧾 Provides detailed **risk category**, **confidence level**, and **sentiment**
- ⚡ Fast, responsive, and mobile-friendly UI
- 🔗 Integrated with **Azure OpenAI** and **Azure Text Analytics**
- 🌈 Built using **Flask**, **Tailwind CSS**, and **JavaScript**

---

## 📖 How to Use

1. Paste or type a suspicious message into the input box.
2. Click the **"Analyze Now"** button.
3. The system will return:
   - Risk Category (e.g. Scam, Hoax, Safe)
   - Explanation & Warning Indicators
   - Sentiment & Confidence Level

---

## 🗂️ Folder Structure

```
/
chatbot-ai-azure/
├── app.py # Main Flask app
├── config/ # Azure configuration (with .env support)
├── services/ # AI service integration (OpenAI & Azure AI)
├── static/ # Frontend assets (Tailwind CSS & JS)
├── templates/ # HTML templates (Jinja2)
├── requirements.txt # Python dependencies
├── .env # Environment variables
```

---

## 💻 Requirements

- Python **3.8+**
- Azure OpenAI endpoint + key
- Azure AI Services (Text Analytics) endpoint + key

See [`requirements.txt`](requirements.txt) for dependencies.

---

## ⚙️ Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/chatbot-ai-azure.git
cd chatbot-ai-azure

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables in .env or config/azure_config.py

# 4. Run the Flask server
python app.py

Then open http://localhost:5000 in your browser 🚀

```

👤 Author
Built with ❤️ by Wira Dhana Putra
🧾 [Portfolio](https://wiradp.github.io) | 💼 [LinkedIn](https://www.linkedin.com/in/wira-dhana-putra/)

📄 License
MIT License – Feel free to use and modify with credit.
