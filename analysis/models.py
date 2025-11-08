from django.db import models

class Conversation(models.Model):
    """
    Represents a chat conversation between user and AI
    """
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    analyzed = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.title} (ID: {self.id})"

    class Meta:
        ordering = ['-created_at']  


class Message(models.Model):
    """
    Individual messages within a conversation
    """
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name="messages"
    )
    sender = models.CharField(max_length=20) 
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}..."

    class Meta:
        ordering = ['timestamp']  


class ConversationAnalysis(models.Model):
    """
    Stores analysis results for each conversation
    Includes 10+ parameters as required
    """
    conversation = models.OneToOneField(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name="analysis"
    )
    
    clarity_score = models.FloatField(default=0.0, help_text="0.0 to 1.0")
    relevance_score = models.FloatField(default=0.0, help_text="0.0 to 1.0")
    accuracy_score = models.FloatField(default=0.0, help_text="0.0 to 1.0")
    completeness_score = models.FloatField(default=0.0, help_text="0.0 to 1.0")
    
    sentiment = models.CharField(
        max_length=20, 
        default='neutral',
        choices=[
            ('positive', 'Positive'),
            ('neutral', 'Neutral'),
            ('negative', 'Negative'),
        ]
    )
    empathy_score = models.FloatField(default=0.0, help_text="0.0 to 1.0")
    response_time_avg = models.FloatField(default=0.0, help_text="Average seconds (mock)")
    
    resolution = models.BooleanField(default=False, help_text="Was issue resolved?")
    escalation_needed = models.BooleanField(default=False, help_text="Needs human escalation?")
    
    fallback_count = models.IntegerField(default=0, help_text="Times AI said 'I don't know'")
    
    overall_score = models.FloatField(default=0.0, help_text="0.0 to 1.0")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for: {self.conversation.title} (Score: {self.overall_score})"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Conversation Analyses"
