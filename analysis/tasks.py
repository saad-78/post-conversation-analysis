from celery import shared_task
from .models import Conversation, ConversationAnalysis
from .services import ConversationAnalyzer


@shared_task
def analyze_all_new_conversations():
    """
    Celery task: Analyze all unanalyzed conversations
    This runs daily at midnight via Celery Beat
    """
    conversations = Conversation.objects.filter(analyzed=False)
    analyzer = ConversationAnalyzer()
    
    count = 0
    for conversation in conversations:
        if not conversation.messages.exists():
            continue
        
        try:
            analysis_data = analyzer.analyze_conversation(conversation)
            
            ConversationAnalysis.objects.update_or_create(
                conversation=conversation,
                defaults=analysis_data
            )
            
            conversation.analyzed = True
            conversation.save()
            
            count += 1
        except Exception as e:
            print(f"Error analyzing conversation {conversation.id}: {str(e)}")
    
    return f"Successfully analyzed {count} conversations"


@shared_task
def analyze_single_conversation(conversation_id):
    """
    Celery task: Analyze a single conversation asynchronously
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        analyzer = ConversationAnalyzer()
        
        analysis_data = analyzer.analyze_conversation(conversation)
        
        ConversationAnalysis.objects.update_or_create(
            conversation=conversation,
            defaults=analysis_data
        )
        
        conversation.analyzed = True
        conversation.save()
        
        return f"Analyzed conversation {conversation_id}"
    except Conversation.DoesNotExist:
        return f"Conversation {conversation_id} not found"
