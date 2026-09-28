# 🤖 RAG AI Resume Analyzer

A **RAG-powered (Retrieval-Augmented Generation)** command-line tool that analyzes your resume against real job descriptions, gives you a match percentage, identifies skill gaps, generates a personalized learning roadmap, recommends alternate roles, and generates interview questions — all powered by **Groq LLM (Qwen 3.8-27B)** and **Qdrant Vector Database**.

---

## 🧠 How It Works

```
Your Resume (PDF)
      │
      ▼
  PDF Parser  ──►  Resume Extraction (LLM)
                          │
                          ▼
       Qdrant Vector DB  ──►  Job Description Retrieval (RAG)
                          │
                          ▼
                   LLM Match Analysis
                          │
              ┌───────────┼───────────────┐
              ▼           ▼               ▼
      Match % & Gaps  Roadmap     Interview Questions
              │           │               │
              └───────────┴───────────────┘
                          │
                          ▼
                   CLI Output 🖥️
```

---

## 📁 Project Structure

```
RAG-Ai-Resume-Analyzer-main/
│
├── backend/                        # Main application code
│   ├── main.py                     # ✅ Entry point — run this! (auto-initializes vector DB)
│   ├── setup_vector_db.py          # ⚙️  Contains `create_db()` function for Qdrant vector database setup
│   ├── config.py                   # App configuration & API clients
│   ├── schemas.py                  # Pydantic data models
│   └── services/
│       ├── resume_analysis.py      # Resume parsing & JD matching
│       ├── role_recommendation.py  # Suggests alternate roles
│       ├── roadmap.py              # Generates skill roadmap
│       ├── interview_questions.py  # Fetches interview questions
│       ├── llm_service.py          # Groq LLM calls
│       └── qdrant_service.py       # Vector search logic
│
├── data/                           # Knowledge & resume data
│   ├── available_roles.json        # List of supported job roles
│   ├── resumes/                    # 📂 Put YOUR resume PDF here
│   │   └── your_resume.pdf
│   └── roles_data/                 # Job description JSONs (15 roles)
│       └── *.json
│
├── requirements.txt                # Python dependencies
├── .env.example                    # Template for your API keys
└── .env                            # 🔑 Your secret API keys (create this!)
```

---

## ✅ Prerequisites

Before you start, make sure you have the following installed:

- **Python 3.10 or above** → [Download Python](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** (optional, for cloning) → [Download Git](https://git-scm.com/)

---

## 🚀 Step-by-Step Setup Guide

### Step 1 — Clone or Download the Project

```bash
git clone https://github.com/your-username/RAG-Ai-Resume-Analyzer.git
cd RAG-Ai-Resume-Analyzer-main
```

> 💡 Or download and extract the ZIP file and open the folder in your terminal.

---

### Step 2 — Create a Virtual Environment

A virtual environment keeps your project dependencies isolated from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> ✅ You'll know it's active when you see `(venv)` at the start of your terminal prompt.

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
| Package | Purpose |
|---|---|
| `groq` | Connects to Groq LLM (AI brain) |
| `qdrant-client` | Talks to Qdrant vector database |
| `fastembed` | Converts text into vector embeddings |
| `pypdf` | Reads and parses your PDF resume |
| `python-dotenv` | Loads secrets from `.env` file |
| `fastapi` + `uvicorn` | API framework (available for future use) |

> ⏳ The first time `fastembed` runs, it will **automatically download** the embedding model (`BAAI/bge-small-en-v1.5`, ~130MB). This is a one-time download.

---

### Step 4 — Get Your API Keys

You need **two** free API keys:

#### 🔑 A) Groq API Key (Free)

Groq is the AI engine that powers the analysis.

1. Go to → [https://console.groq.com](https://console.groq.com)
2. Sign up for a **free account**
3. Navigate to **API Keys** → Click **Create API Key**
4. Copy your key — it starts with `gsk_...`

---

#### 🗄️ B) Qdrant Cloud (Free Tier)

Qdrant is the vector database that stores job description knowledge.

1. Go to → [https://cloud.qdrant.io](https://cloud.qdrant.io)
2. Sign up for a **free account**
3. Click **Create Cluster** → Choose the **Free tier**
4. Once the cluster is ready, you'll find:
   - **Cluster URL** (looks like: `https://xxxx-xxxx.aws.cloud.qdrant.io`)
   - **API Key** → Go to **Access** tab → **Create API Key**
5. Copy both the URL and the API Key

---

### Step 5 — Set Up Your `.env` File

In the **root of the project** (same folder as `requirements.txt`), create a `.env` file.

You can copy the provided template:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Then open `.env` and fill in your actual keys:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here

QDRANT_URL=https://your-cluster-url.aws.cloud.qdrant.io

QDRANT_API_KEY=your_qdrant_api_key_here
```

> ⚠️ **Important:** No quotes needed around the values. Just paste them directly.
> 🔒 **Never share this file!** It's already in `.gitignore` so it won't be pushed to GitHub.

---

### Step 6 — Add Your Resume

Place your **PDF resume** inside the `data/resumes/` folder:

```
data/
└── resumes/
    └── your_resume.pdf    ← Put your PDF here
```

> 📌 Rules:
> - Must be a **PDF** file (`.pdf` extension)
> - Only **one resume** at a time is supported
> - The file can have any name

---

### Step 7 — Run the Analyzer!

From the project root, navigate into the `backend/` folder:

```bash
cd backend
```

Then run:

```bash
python main.py
```

> 💡 **Automatic Vector DB Setup:** You don't need to manually run a separate database setup script! On the first run, `main.py` checks if the collection exists and automatically calls the `create_db()` function from `setup_vector_db.py` to embed and upload all job descriptions to Qdrant Cloud.

The CLI will check the vector database, display all available roles, and ask you to pick one:

```
============================================================
  RAG AI Resume Analyzer
============================================================

[Step 1/2] Checking vector database...
  Vector DB ready — 638 knowledge chunks loaded.

[Step 2/2] Role Selection

  Available Roles:
  ----------------------------------------
   1. Ai Engineer
   2. Backend Developer
   3. Cloud Engineer
   4. Cloud Security Engineer
   5. Cybersecurity Engineer
   6. Data Analyst
   7. Data Engineer
   8. Data Scientist
   9. Devops Engineer
  10. Frontend Developer
  11. Full Stack Developer
  12. Generative Ai / Llm Engineer
  13. Machine Learning Engineer
  14. Mlops Engineer / Ml Platform Engineer
  15. Software Engineer
  ----------------------------------------

  You can enter:
    - A number (e.g. 3) to pick from the list above
    - The role name directly (e.g. data scientist)

  Your choice:
```

**Two ways to select a role:**
- Enter the **number** (e.g. `8` for Data Scientist)
- Type the **role name** directly (e.g. `data scientist`)

---

## 📊 Sample Output

```
Match Percentage:
72

Missing Skills:
- Deep Learning frameworks (PyTorch/TensorFlow)
- Model deployment & MLOps
- SQL & database querying

Analysis:
The candidate shows strong Python and data analysis skills with
relevant project experience. However, key gaps exist in production
ML deployment and deep learning frameworks.

Other Roles:
- data analyst
- machine learning engineer
- ai engineer

Learning Path:
- Python fundamentals for ML
- Statistics and probability
- Machine Learning with scikit-learn
- Deep Learning with PyTorch

Study Resources:
- fast.ai Practical Deep Learning course
- Kaggle Learn (free, hands-on ML)
- CS229 Stanford ML Course (free)

Recommended Projects:
- End-to-end ML pipeline with model deployment
- NLP text classification project
- Time series forecasting dashboard

Roadmap:
- Week 1-2: Brush up Python & NumPy/Pandas
- Week 3-4: Core ML algorithms with scikit-learn
- Month 2: Deep Learning fundamentals with PyTorch
- Month 3: Model deployment with FastAPI + Docker

Interview Questions:
1. Explain the bias-variance tradeoff...
2. How would you handle class imbalance?
...
```

---

## 🌟 Supported Roles

| Role |
|------|
| AI Engineer |
| Machine Learning Engineer |
| Generative AI / LLM Engineer |
| Software Engineer |
| Backend Developer |
| Full Stack Developer |
| Data Scientist |
| Data Engineer |
| Data Analyst |
| Cloud Engineer |
| DevOps Engineer |
| Cybersecurity Engineer |
| Cloud Security Engineer |
| Frontend Developer |
| MLOps Engineer / ML Platform Engineer |

---

## ❓ Troubleshooting

### ❌ `.env content is missing` error
→ Make sure your `.env` file is in the **root project folder** (same level as `requirements.txt`), not inside `backend/`.

### ❌ No PDF resume found error
→ Make sure your resume is inside the `data/resumes/` folder and it has a `.pdf` extension.

### ❌ `not a valid role or number` error
→ Type the role name **exactly** as shown (all lowercase), or enter the corresponding **number** from the list instead.

### ❌ Vector database not set up error
→ The database is set up automatically via `create_db()` when running `python main.py`. If you face issues, ensure your `.env` credentials (`QDRANT_URL`, `QDRANT_API_KEY`) are correct and your Qdrant cluster is active.

### ❌ Qdrant connection error
→ Double-check your `QDRANT_URL` and `QDRANT_API_KEY` in the `.env` file. Make sure there are no extra spaces or quotes.

### ❌ `fastembed` model downloading slowly
→ This is normal on first run. The model (~130MB) downloads once and is cached locally automatically.

### ❌ `ModuleNotFoundError`
→ Make sure your virtual environment is **activated** and you ran `pip install -r requirements.txt` from the root folder.

---

## 🔄 Re-running the Project Later

After the first-time setup, here's all you need to do:

```bash
# 1. Activate virtual environment
venv\Scripts\activate          # Windows
# or
source venv/bin/activate        # macOS/Linux

# 2. Go to backend folder
cd backend

# 3. Run the analyzer
python main.py
```

> Vector database initialization is automatically handled by `main.py` via `create_db()`.

---

## 🏗️ Tech Stack

| Technology | Role |
|---|---|
| 🐍 Python | Core language |
| 🤖 Groq (Qwen 3.8-27B) | LLM for analysis & generation |
| 🗃️ Qdrant Cloud | Vector database for RAG |
| ⚡ FastEmbed (BAAI/bge-small-en-v1.5) | Text embeddings |
| 📄 PyPDF | PDF resume parsing |
| 🔐 python-dotenv | Environment variable management |
| ✅ Pydantic | Structured JSON output schemas |

---

## 📝 License

This project is open-source and free to use for learning and personal projects.

---

> Built with ❤️ — Happy job hunting! 🚀
