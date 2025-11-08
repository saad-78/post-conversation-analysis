# 🚀 Post-Conversation Analysis System

**Automated Django REST API for analyzing AI-human chat conversations with 11+ quality parameters and daily automated cron jobs.**

Built for **Kipps.AI Internship Assignment** by Saad

---

## 📋 Project Overview

This system automatically analyzes conversations between AI agents and human users, scoring them on multiple quality metrics including:

- **Clarity** - Message comprehensibility
- **Relevance** - Topic adherence
- **Accuracy** - Response correctness
- **Completeness** - Answer thoroughness
- **Sentiment** - User emotional state
- **Empathy** - AI empathy level
- **Response Time** - Average response speed
- **Resolution** - Issue resolved status
- **Escalation Need** - Human intervention required
- **Fallback Count** - Times AI couldn't help
- **Overall Score** - Weighted quality average

### Key Features

✅ **REST API** - Upload conversations, trigger analysis, retrieve reports  
✅ **Automated Analysis** - Daily cron job via Celery Beat  
✅ **11 Quality Parameters** - Comprehensive conversation scoring  
✅ **Sentiment Analysis** - NLTK VADER-powered sentiment detection  
✅ **Database Persistence** - SQLite/PostgreSQL storage  
✅ **Admin Panel** - Django admin for data inspection  
✅ **Production Ready** - Celery, Redis, async task processing  

---

## 🛠️ Tech Stack

- **Backend Framework**: Django 4.2
- **API Framework**: Django REST Framework 3.14
- **Task Queue**: Celery 5.3
- **Scheduler**: Celery Beat (django-celery-beat)
- **Message Broker**: Redis 5.0
- **NLP Library**: NLTK 3.8 (VADER Sentiment Analysis)
- **Database**: SQLite (default) / PostgreSQL (production)
- **Language**: Python 3.12

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Redis server
- Git

### 1. Clone Repository

git clone https://github.com/YOUR-USERNAME/post-conversation-analysis.git
cd post-conversation-analysis



### 2. Create Virtual Environment

python3 -m venv venv
source venv/bin/activate # Linux/macOS

venv\Scripts\activate # Windows


### 3. Install Dependencies

pip install -r requirements.txt



### 4. Download NLTK Data

python -m nltk.downloader vader_lexicon punkt



### 5. Configure Database

**Option A: SQLite (Default - No setup needed)**

Already configured in `settings.py`.

**Option B: PostgreSQL (Production)**

1. Install PostgreSQL
2. Create database: `conversation_db`
3. Update `DATABASES` in `conversation_analyzer/settings.py`:

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'conversation_db',
'USER': 'your_username',
'PASSWORD': 'your_password',
'HOST': 'localhost',
'PORT': '5432',
}
}



### 6. Run Migrations

python manage.py migrate



### 7. Create Superuser (Optional)

python manage.py createsuperuser



### 8. Start Redis Server

sudo systemctl start redis-server # Linux

redis-server # macOS/Windows




## 🚀 Running the Application

You need **3 terminal windows** (all with virtual environment activated):

### Terminal 1: Django Development Server

python manage.py runserver



Server runs at: `http://localhost:8000`

### Terminal 2: Celery Worker

celery -A conversation_analyzer worker -l info



Processes background tasks.

### Terminal 3: Celery Beat (Cron Scheduler)

celery -A conversation_analyzer beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler



Runs daily automated analysis at midnight UTC.


## 📡 API Endpoints

### Base URL
http://localhost:8000/api/



### 1️⃣ Upload Conversation

**POST** `/api/conversations/`

curl -X POST http://localhost:8000/api/conversations/
-H "Content-Type: application/json"
-d '{
"title": "Customer Support",
"messages": [
{"sender": "user", "text": "I need help with order 123"},
{"sender": "ai", "text": "Sure! Let me check that for you."},
{"sender": "user", "text": "Thanks!"},
{"sender": "ai", "text": "Your order will arrive tomorrow."}
]
}'



**Response:**
{
"id": 1,
"title": "Customer Support",
"message": "Conversation uploaded successfully",
"analyzed": false
}



### 2️⃣ Analyze Conversation

**POST** `/api/analyse/`

curl -X POST http://localhost:8000/api/analyse/
-H "Content-Type: application/json"
-d '{"conversation_id": 1}'



**Response:**
{
"message": "Analysis completed successfully",
"analysis": {
"clarity_score": 0.85,
"relevance_score": 0.72,
"sentiment": "positive",
"overall_score": 0.78,
...
}
}



### 3️⃣ Get All Reports

**GET** `/api/reports/`

curl http://localhost:8000/api/reports/



**Optional Filters:**
- `?sentiment=positive`
- `?resolution=true`

### 4️⃣ List Conversations

**GET** `/api/conversations/list/`

curl http://localhost:8000/api/conversations/list/



📖 **Full API documentation**: See `API_DOCUMENTATION.md`

---

## 🤖 Automated Cron Job

The system automatically analyzes all new (unanalyzed) conversations **daily at midnight UTC** using Celery Beat.

No manual intervention required! Just upload conversations, and they'll be analyzed automatically.

### Manual Trigger (For Testing)

python manage.py shell


undefined
from analysis.tasks import analyze_all_new_conversations
result = analyze_all_new_conversations.delay()
print(result.get(timeout=10))


---

## 🧪 Testing

### Test Models in Django Shell

python manage.py shell


undefined
from analysis.models import Conversation, Message
from analysis.services import ConversationAnalyzer

Create test conversation
conv = Conversation.objects.create(title="Test")
Message.objects.create(conversation=conv, sender="user", text="Hello")
Message.objects.create(conversation=conv, sender="ai", text="Hi! How can I help?")

Analyze
analyzer = ConversationAnalyzer()
results = analyzer.analyze_conversation(conv)
print(results)



### Test API with curl

See examples in **API Endpoints** section above.

---

## 📊 Analysis Parameters Explained

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| **Clarity Score** | Float | 0.0-1.0 | Message clarity based on length/structure |
| **Relevance Score** | Float | 0.0-1.0 | Topic adherence via keyword overlap |
| **Accuracy Score** | Float | 0.0-1.0 | Response correctness (mocked) |
| **Completeness Score** | Float | 0.0-1.0 | Answer thoroughness |
| **Sentiment** | String | pos/neu/neg | User sentiment via NLTK VADER |
| **Empathy Score** | Float | 0.0-1.0 | Empathy keyword detection |
| **Response Time** | Float | seconds | Average response time (mocked) |
| **Resolution** | Boolean | true/false | Issue resolved detection |
| **Escalation Needed** | Boolean | true/false | Human intervention required |
| **Fallback Count** | Integer | 0+ | Times AI said "I don't know" |
| **Overall Score** | Float | 0.0-1.0 | Weighted average of metrics |

---

## 🔐 Admin Panel

Access Django admin at: `http://localhost:8000/admin`

Login with superuser credentials created during setup.

View/edit:
- Conversations
- Messages
- Analysis Results
- Celery scheduled tasks

---

## 🐳 Production Deployment (Optional)

For production deployment, consider:

1. **Use PostgreSQL** instead of SQLite
2. **Set `DEBUG = False`** in settings.py
3. **Use environment variables** for secrets (`.env` file)
4. **Use Gunicorn** as WSGI server
5. **Use Nginx** as reverse proxy
6. **Deploy on**: Heroku, AWS, DigitalOcean, or Railway

---

## 📝 Assignment Requirements Checklist

✅ **Part 1**: Post-conversation analysis with 11 parameters  
✅ **Part 2**: Django application with database storage  
✅ **Part 3**: REST API endpoints (upload, analyze, reports)  
✅ **Part 4**: Automated cron job (Celery Beat, daily midnight)  
✅ **Documentation**: README, API docs, code comments  
✅ **Code Quality**: Clean, modular, production-ready  
✅ **Git**: Proper version control with meaningful commits  

---

## 🤝 Contributing

This is an assignment project, but feedback and suggestions are welcome!

---

## 📧 Contact

**Developer**: Saad  
**Project**: Kipps.AI Internship Assignment  
**Date**: November 2025  

---

## 📄 License

This project is created for educational purposes as part of an internship assignment.

---

## 🙏 Acknowledgments

- **Kipps.AI** for the internship opportunity
- **Django** and **Django REST Framework** communities
- **NLTK** for sentiment analysis tools
- **Celery** for task queue functionality

---
