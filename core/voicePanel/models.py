from django.db import models






# models.py
class AudioMessage(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    created_at = models.DateTimeField(auto_now_add=True)




class VoiceMessage(models.Model):
    voice_file = models.FileField(upload_to='voice/')
    created_at = models.DateTimeField(auto_now_add=True)



