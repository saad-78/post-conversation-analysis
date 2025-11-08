from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random


class ConversationAnalyzer:
    """
    Analyzes conversations and returns scores for 10+ parameters
    """
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze_conversation(self, conversation):
        """
        Main analysis function
        Returns a dictionary with all analysis scores
        """
        messages = conversation.messages.all()
        ai_messages = [m.text for m in messages if m.sender == 'ai']
        user_messages = [m.text for m in messages if m.sender == 'user']
        
        sentiment_result = self.analyze_sentiment(user_messages)
        clarity = self.analyze_clarity(ai_messages)
        relevance = self.analyze_relevance(ai_messages, user_messages)
        empathy = self.analyze_empathy(ai_messages)
        completeness = self.analyze_completeness(ai_messages)
        accuracy = self.analyze_accuracy(ai_messages)
        fallback_count = self.count_fallbacks(ai_messages)
        resolution = self.check_resolution(messages)
        escalation_needed = self.check_escalation(sentiment_result, resolution)
        response_time = self.calculate_response_time()
        
        overall_score = self.calculate_overall_score({
            'clarity': clarity,
            'relevance': relevance,
            'accuracy': accuracy,
            'completeness': completeness,
            'empathy': empathy,
        })
        
        return {
            'clarity_score': round(clarity, 2),
            'relevance_score': round(relevance, 2),
            'accuracy_score': round(accuracy, 2),
            'completeness_score': round(completeness, 2),
            'sentiment': sentiment_result['label'],
            'empathy_score': round(empathy, 2),
            'response_time_avg': round(response_time, 2),
            'resolution': resolution,
            'escalation_needed': escalation_needed,
            'fallback_count': fallback_count,
            'overall_score': round(overall_score, 2),
        }
    
    def analyze_sentiment(self, user_messages):
        """
        Analyze user sentiment using VADER
        Returns: {'label': 'positive/neutral/negative', 'score': float}
        """
        if not user_messages:
            return {'label': 'neutral', 'score': 0.0}
        
        scores = []
        for msg in user_messages:
            sentiment = self.sia.polarity_scores(msg)
            scores.append(sentiment['compound'])
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score > 0.05:
            return {'label': 'positive', 'score': avg_score}
        elif avg_score < -0.05:
            return {'label': 'negative', 'score': avg_score}
        else:
            return {'label': 'neutral', 'score': avg_score}
    
    def analyze_clarity(self, ai_messages):
        """
        Score clarity based on message length and structure
        Range: 0.0 to 1.0
        """
        if not ai_messages:
            return 0.5
        
        clarity_scores = []
        for msg in ai_messages:
            length = len(msg)
           
            if 20 <= length <= 200:
                clarity_scores.append(0.9)
            elif length < 20:
                clarity_scores.append(0.4) 
            else:
                clarity_scores.append(0.7) 
        
        return sum(clarity_scores) / len(clarity_scores)
    
    def analyze_relevance(self, ai_messages, user_messages):
        """
        Check if AI stayed on topic by analyzing keyword overlap
        Range: 0.0 to 1.0
        """
        if not ai_messages or not user_messages:
            return 0.5
        
        user_words = set(' '.join(user_messages).lower().split())
        ai_words = set(' '.join(ai_messages).lower().split())
        
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'i', 'you', 'can', 'will'}
        user_words -= stopwords
        ai_words -= stopwords
        
        if not user_words:
            return 0.5
        
        overlap = len(user_words.intersection(ai_words))
        relevance = min(overlap / len(user_words), 1.0)
        
        return max(relevance, 0.3)  
    
    def analyze_empathy(self, ai_messages):
        """
        Detect empathy keywords in AI responses
        Range: 0.0 to 1.0
        """
        empathy_keywords = [
            'sorry', 'understand', 'help', 'appreciate', 
            'apologize', 'thank', 'care', 'concern',
            'happy', 'glad', 'pleasure', 'welcome'
        ]
        
        if not ai_messages:
            return 0.0
        
        empathy_count = 0
        for msg in ai_messages:
            msg_lower = msg.lower()
            if any(keyword in msg_lower for keyword in empathy_keywords):
                empathy_count += 1
        
        return min(empathy_count / len(ai_messages), 1.0)
    
    def analyze_completeness(self, ai_messages):
        """
        Check if AI provided complete answers
        Heuristic: longer messages = more complete
        Range: 0.0 to 1.0
        """
        if not ai_messages:
            return 0.0
        
        avg_length = sum(len(msg) for msg in ai_messages) / len(ai_messages)
        
        if avg_length > 100:
            return 0.9
        elif avg_length > 50:
            return 0.7
        elif avg_length > 20:
            return 0.5
        else:
            return 0.3
    
    def analyze_accuracy(self, ai_messages):
        """
        Mock accuracy scoring (in real-world, would use fact-checking)
        Range: 0.0 to 1.0
        """
        return random.uniform(0.7, 1.0)
    
    def count_fallbacks(self, ai_messages):
        """
        Count fallback responses (AI admitting it doesn't know)
        Returns: integer count
        """
        fallback_phrases = [
            "i don't know", 
            "i'm not sure", 
            "i cannot",
            "sorry, i can't", 
            "don't understand",
            "unable to help",
            "not able to"
        ]
        
        count = 0
        for msg in ai_messages:
            msg_lower = msg.lower()
            if any(phrase in msg_lower for phrase in fallback_phrases):
                count += 1
        
        return count
    
    def check_resolution(self, messages):
        """
        Check if the issue was resolved
        Looks for positive keywords in last messages
        Returns: boolean
        """
        if not messages:
            return False
        
        messages_list = list(messages)
        
        if len(messages_list) < 2:
            return False
        
        last_messages = [m.text.lower() for m in messages_list[-2:]]
        resolution_keywords = [
            'thank', 'thanks', 'resolved', 'fixed', 
            'solved', 'great', 'perfect', 'awesome',
            'helped', 'appreciate', 'done'
        ]
        
        return any(keyword in ' '.join(last_messages) for keyword in resolution_keywords)
    
    def check_escalation(self, sentiment_result, resolution):
        """
        Determine if escalation to human is needed
        Criteria: negative sentiment AND not resolved
        Returns: boolean
        """
        if sentiment_result['label'] == 'negative' and not resolution:
            return True
        return False
    
    def calculate_response_time(self):
        """
        Mock response time calculation
        In production, would use actual timestamp differences
        Returns: float (seconds)
        """
        return random.uniform(5.0, 30.0)
    
    def calculate_overall_score(self, scores):
        """
        Calculate weighted average of all quality metrics
        Range: 0.0 to 1.0
        """
        weights = {
            'clarity': 0.20,
            'relevance': 0.25,
            'accuracy': 0.20,
            'completeness': 0.20,
            'empathy': 0.15,
        }
        
        total = sum(scores[key] * weights[key] for key in scores)
        return total
