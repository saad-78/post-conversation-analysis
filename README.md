# Post-Conversation Analysis System

Automated Django REST API for analyzing AI-human chat conversations.

## Setup Instructions

### 1. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate


### 2. Install Dependencies
pip install -r requirements.txt
python -m nltk.downloader vader_lexicon punkt


### 3. Run Migrations
python manage.py migrate

### 4. Start Development Server
python manage.py runserver


Visit http://localhost:8000

## Project Structure
- `conversation_analyzer/` — Django project settings
- `analysis/` — Main app for conversation analysis
- `venv/` — Virtual environment
- `manage.py` — Django management tool

## Next Steps
- Part 2: Database Models
- Part 3: REST API Endpoints