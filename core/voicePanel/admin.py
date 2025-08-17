#django files
from django.contrib import admin

#your files
from .models import AudioMessage, VoiceMessage

admin.site.register(AudioMessage)

admin.site.register(VoiceMessage)




