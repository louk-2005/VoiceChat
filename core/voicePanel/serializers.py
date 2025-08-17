#rest files
from rest_framework import serializers

#your files
from .models import AudioMessage

# serializers.py
class AudioMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioMessage
        fields = ['id', 'audio_file', 'created_at']




