from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Conversation, ConversationAnalysis
from .serializers import (
    ConversationCreateSerializer,
    ConversationListSerializer,
    AnalysisSerializer
)
from .services import ConversationAnalyzer


@api_view(['POST'])
def upload_conversation(request):
    """
    POST /api/conversations/
    Upload a new conversation with messages
    
    Expected JSON format:
    {
        "title": "Customer Support",
        "messages": [
            {"sender": "user", "text": "I need help"},
            {"sender": "ai", "text": "How can I assist you?"}
        ]
    }
    """
    serializer = ConversationCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        conversation = serializer.save()
        return Response(
            {
                'id': conversation.id,
                'title': conversation.title,
                'message': 'Conversation uploaded successfully',
                'analyzed': conversation.analyzed
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def analyze_conversation(request):
    """
    POST /api/analyse/
    Trigger analysis on a specific conversation
    
    Expected JSON format:
    {
        "conversation_id": 1
    }
    """
    conversation_id = request.data.get('conversation_id')
    
    if not conversation_id:
        return Response(
            {'error': 'conversation_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {'error': f'Conversation with id {conversation_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if conversation has messages
    if not conversation.messages.exists():
        return Response(
            {'error': 'Conversation has no messages to analyze'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Run analysis
    analyzer = ConversationAnalyzer()
    analysis_data = analyzer.analyze_conversation(conversation)
    
    # Save or update analysis
    analysis, created = ConversationAnalysis.objects.update_or_create(
        conversation=conversation,
        defaults=analysis_data
    )
    
    # Mark conversation as analyzed
    conversation.analyzed = True
    conversation.save()
    
    serializer = AnalysisSerializer(analysis)
    
    return Response(
        {
            'message': 'Analysis completed successfully',
            'analysis': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_reports(request):
    """
    GET /api/reports/
    Retrieve all conversation analysis results
    
    Optional query parameters:
    - sentiment: filter by sentiment (positive, neutral, negative)
    - resolution: filter by resolution status (true, false)
    """
    analyses = ConversationAnalysis.objects.all()
    
    # Optional filtering
    sentiment_filter = request.query_params.get('sentiment', None)
    resolution_filter = request.query_params.get('resolution', None)
    
    if sentiment_filter:
        analyses = analyses.filter(sentiment=sentiment_filter)
    
    if resolution_filter:
        resolution_bool = resolution_filter.lower() == 'true'
        analyses = analyses.filter(resolution=resolution_bool)
    
    serializer = AnalysisSerializer(analyses, many=True)
    
    return Response(
        {
            'count': analyses.count(),
            'results': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def list_conversations(request):
    """
    GET /api/conversations/
    List all conversations
    """
    conversations = Conversation.objects.all()
    serializer = ConversationListSerializer(conversations, many=True)
    
    return Response(
        {
            'count': conversations.count(),
            'results': serializer.data
        },
        status=status.HTTP_200_OK
    )
