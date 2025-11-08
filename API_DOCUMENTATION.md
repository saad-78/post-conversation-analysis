# Post-Conversation Analysis API Documentation

## Base URL
http://localhost:8000/api/


## Endpoints

### 1. Upload Conversation
**POST** `/api/conversations/`

Upload a new conversation with messages.

**Request Body:**
{
"title": "Customer Support Chat",
"messages": [
{"sender": "user", "text": "I need help"},
{"sender": "ai", "text": "How can I assist you?"}
]
}


**Response (201 Created):**
{
"id": 1,
"title": "Customer Support Chat",
"message": "Conversation uploaded successfully",
"analyzed": false
}


---

### 2. Analyze Conversation
**POST** `/api/analyse/`

Trigger analysis on a specific conversation.

**Request Body:**
{
"conversation_id": 1
}


**Response (200 OK):**
{
"message": "Analysis completed successfully",
"analysis": {
"id": 1,
"conversation": 1,
"conversation_title": "Customer Support Chat",
"clarity_score": 0.85,
"relevance_score": 0.72,
"accuracy_score": 0.89,
"completeness_score": 0.78,
"sentiment": "positive",
"empathy_score": 0.65,
"response_time_avg": 15.43,
"resolution": true,
"escalation_needed": false,
"fallback_count": 0,
"overall_score": 0.79,
"created_at": "2025-11-08T12:00:00Z"
}
}



### 3. Get All Reports
**GET** `/api/reports/`

Retrieve all conversation analysis results.

**Optional Query Parameters:**
- `sentiment` - Filter by sentiment (positive, neutral, negative)
- `resolution` - Filter by resolution status (true, false)

**Example:** `/api/reports/?sentiment=positive&resolution=true`

**Response (200 OK):**
{
"count": 2,
"results": [
{
"id": 1,
"conversation_title": "Order Help",
"overall_score": 0.79,
"sentiment": "positive",
"resolution": true,
...
}
]
}



### 4. List Conversations
**GET** `/api/conversations/list/`

List all uploaded conversations.

**Response (200 OK):**
{
"count": 3,
"results": [
{
"id": 1,
"title": "Order Help",
"created_at": "2025-11-08T10:00:00Z",
"analyzed": true
}
]
}


## Analysis Parameters

The system analyzes conversations on **11 parameters**:

1. **Clarity Score** (0.0-1.0) - Message clarity
2. **Relevance Score** (0.0-1.0) - Topic adherence
3. **Accuracy Score** (0.0-1.0) - Response accuracy
4. **Completeness Score** (0.0-1.0) - Answer completeness
5. **Sentiment** (positive/neutral/negative) - User sentiment
6. **Empathy Score** (0.0-1.0) - AI empathy level
7. **Response Time Avg** (seconds) - Average response time
8. **Resolution** (boolean) - Issue resolved?
9. **Escalation Needed** (boolean) - Needs human intervention?
10. **Fallback Count** (integer) - Times AI said "I don't know"
11. **Overall Score** (0.0-1.0) - Weighted average

## Automated Cron Job

The system automatically analyzes all new (unanalyzed) conversations **daily at midnight UTC** using Celery Beat.

No manual intervention required!
