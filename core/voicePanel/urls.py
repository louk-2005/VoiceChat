from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioMessageViewSet, HandlerVoiceToTextAPIView

app_name = 'voicePanel'

router = DefaultRouter()
router.register(r'voice', AudioMessageViewSet, basename='voice')

urlpatterns = [
    path('voice/text/', HandlerVoiceToTextAPIView.as_view(), name='voiceText'),
    path('', include(router.urls)),
]
