from rest_framework import serializers
from .models import Conversation, Message, ConversationAnalysis


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for individual messages
    """
    class Meta:
        model = Message
        fields = ['sender', 'text']


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating conversations with nested messages
    """
    messages = MessageSerializer(many=True)
    
    class Meta:
        model = Conversation
        fields = ['title', 'messages']
    
    def create(self, validated_data):
        messages_data = validated_data.pop('messages')
        conversation = Conversation.objects.create(**validated_data)
        
        for message_data in messages_data:
            Message.objects.create(conversation=conversation, **message_data)
        
        return conversation


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing conversations
    """
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'analyzed']


class AnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for analysis results
    """
    conversation_title = serializers.CharField(source='conversation.title', read_only=True)
    
    class Meta:
        model = ConversationAnalysis
        fields = [
            'id',
            'conversation',
            'conversation_title',
            'clarity_score',
            'relevance_score',
            'accuracy_score',
            'completeness_score',
            'sentiment',
            'empathy_score',
            'response_time_avg',
            'resolution',
            'escalation_needed',
            'fallback_count',
            'overall_score',
            'created_at',
        ]
        read_only_fields = ['created_at']
