from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.upload_conversation, name='upload-conversation'),
    
    path('conversations/list/', views.list_conversations, name='list-conversations'),
    
    path('analyse/', views.analyze_conversation, name='analyze-conversation'),
    
    path('reports/', views.get_reports, name='get-reports'),
]
