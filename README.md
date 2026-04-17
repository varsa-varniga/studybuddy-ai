# StudyBuddy AI 📚🤖

> Turn your notes, PDFs, and study materials into an intelligent AI tutor.

StudyBuddy AI is a **Retrieval-Augmented Generation (RAG)** powered learning assistant that helps students learn smarter using their own documents.

Upload notes, textbooks, PDFs, or research materials and ask questions in natural language. Instead of giving generic answers, StudyBuddy AI retrieves relevant content from uploaded files and generates accurate, context-aware responses.

Built with a modern full-stack architecture using **FastAPI**, **React**, and AI-powered retrieval systems.

---

## 🚀 Why StudyBuddy AI?

Traditional chatbots answer from general knowledge.

StudyBuddy AI answers from **your study materials**.

That means:

✅ Personalized learning  
✅ Better revision experience  
✅ Reduced hallucinations  
✅ Faster concept understanding  
✅ Real AI productivity tool

---

## ✨ Features

- 📄 Upload PDFs, TXT files, and notes
- 💬 Ask questions from your own materials
- 🧠 Context-aware AI answers
- 🔍 Semantic search with embeddings
- ⚡ Fast retrieval using vector database
- 🌐 Full-stack web application
- 🎯 Clean modern UI
- 🛠️ Modular scalable backend

---

## 🧠 How It Works

1. Upload your study materials  
2. Extract and clean text  
3. Split text into chunks  
4. Convert chunks into embeddings  
5. Store vectors in database  
6. Retrieve relevant content for questions  
7. Generate grounded AI responses

---

## 🛠️ Tech Stack

### Frontend

- React
- MUI
- Axios

### Backend

- FastAPI
- Python
- Uvicorn

### AI / RAG

- LangChain
- FAISS
- Sentence Transformers

### File Processing

- PymuPDF

### Dev Tools

- Git
- GitHub
- VS Code

---

## 📁 Project Structure

```bash
StudyBuddy-AI/
│── frontend/
│── backend/
│   │── app/
│   │   │── routes/
│   │   │── schemas/
│   │   │── config/
│   │── main.py
│
│── rag_engine/
│   │── loaders/
│   │── processing/
│   │── embeddings/
│   │── vectorstore/
│   │── retrieval/
│   │── prompts/
│   │── pipeline.py
│
│── data/
│── requirements.txt