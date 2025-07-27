# 🧠 PersonaRewriter

**PersonaRewriter** is a two-part application that rewrites text fragments based on a given personality description. The system includes:

- A **FastAPI** server that processes rewrite requests using langchain model to work with LLMs.
- A **Streamlit** client that provides a user-friendly interface to input text and select personality descriptions.

Both components are containerized and managed with Docker Compose.

---

## 📦 Project Structure
text-rewriter-by-personality/
├── rewriter.client/ # Streamlit frontend
├── rewriter.server/ # FastAPI backend
├── docker-compose.yml # Orchestration for client/server
├── example.env # Example configuration
└── README.md

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/text-rewriter-by-personality.git
cd text-rewriter-by-personality
```

### 2. Set up environment variables
Create a .env file based on the provided template:
```bash
cp example.env .env
```
Inside .env, define the following:
GOOGLE_API_KEY=your_google_api_key_here

### 3. Build and run the application
```bash
docker compose build
docker compose up
```
The Streamlit client will be available at: http://localhost:5585
The FastAPI server will be available at: http://localhost:5583/

---

## License
MIT License