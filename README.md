# Chatbot AI Azure

**Chatbot AI Azure** is an intelligent web app that helps detect **scams, hoaxes, and online gambling promotions** using Azure OpenAI and Text Analytics. Just paste any suspicious message — the AI will analyze it, classify the risk, and explain why.

---

## 🚀 Features

- 🧠 AI-based detection for scams, hoaxes, gambling
- 🌐 Supports multi-language input (Indonesian, English, Arabic, etc.)
- 🧾 Risk explanation, confidence level, and sentiment analysis
- ⚡ Fast, responsive UI built with Flask + Tailwind CSS
- 🔗 Powered by Azure OpenAI + Azure Cognitive Services

---

## 🌍 Live Demo

Try it now on **Azure App Service**:  
🔗 [https://cekfakta-ai-app.azurewebsites.net](https://cekfakta-ai-app.azurewebsites.net)

## ⚠️ Disclaimer

If you encounter the message:

“App is no longer available”
or
“Your subscription has been disabled”

This is because the free Azure subscription used to host the application has expired. As a result, the deployed web app and AI services are no longer active.

You can still run the application locally or explore the source code on [GitHub](https://github.com/yourusername/chatbot-ai-azure.git)

---

## 📖 How to Use

1. Paste a suspicious message into the input field
2. Click **Analyze Now**
3. View results: risk category, explanation, sentiment, and confidence

---

## 🗂️ Project Structure

```
chatbot-ai-azure/
├── app.py
├── requirements.txt
├── .env
├── config/
│   └── azure_config.py
├── services/
│   └── ai_service.py
├── templates/
│   └── index.html
├── static/
│   ├── js/script.js
│   └── css/input.css
```

---

## 💻 Requirements

- Python 3.8+
- Azure OpenAI + Azure Text Analytics credentials
- Environment variables (.env or Azure App Settings)

---

## ⚙️ Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/chatbot-ai-azure.git
cd chatbot-ai-azure

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally
python app.py

Then open http://localhost:5000 in your browser 🚀

```

👤 Author
Built with ❤️ by Wira Dhana Putra
🧾 [Portfolio](https://wiradp.github.io) | 💼 [LinkedIn](https://www.linkedin.com/in/wira-dhana-putra/)

📄 License
MIT License – Feel free to use and modify with credit.
