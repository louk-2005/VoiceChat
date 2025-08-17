# rest files
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
# your files
from .serializers import AudioMessageSerializer
from .models import AudioMessage, VoiceMessage
import os
from django.conf import settings
from io import BytesIO
import openai
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

from django.http import FileResponse


class AudioMessageViewSet(viewsets.ModelViewSet):
    queryset = AudioMessage.objects.all()
    serializer_class = AudioMessageSerializer


# # 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
#
openai.api_key = "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"
#
#
#
# class HandlerVoiceToTextAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request, format=None):
#         audio_file = request.FILES.get('audio_file')
#         if not audio_file:
#             return Response({"error": "No file uploaded"}, status=400)
#
#         audio_instance = AudioMessage.objects.create(audio_file=audio_file)
#
#         file_bytes = BytesIO(audio_file.read())
#         file_bytes.name = audio_file.name
#
#         client = openai.OpenAI(
#             api_key="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"
#         )
#
#         transcription_text = client.audio.transcriptions.create(
#             model="gpt-4o-transcribe",
#             file=file_bytes,
#             response_format="text"
#         )
#
#         return Response({"text": transcription_text})




class HandlerVoiceToTextAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        audio_file = request.FILES.get("audio_file")
        if not audio_file:
            return Response({"error": "No file uploaded"}, status=400)

        audio_instance = AudioMessage.objects.create(audio_file=audio_file)
        file_path = audio_instance.audio_file.path

        try:
            sound = AudioSegment.from_file(file_path)
            wav_path = file_path.rsplit(".", 1)[0] + ".wav"
            sound.export(wav_path, format="wav")
            file_path = wav_path
        except Exception as e:
            return Response({"error": f"خطای تبدیل فایل صوتی: {e}"}, status=500)

        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(file_path) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-US")
        except sr.UnknownValueError:
            return Response({"error": "صدا قابل تشخیص نبود"}, status=400)
        except sr.RequestError as e:
            return Response({"error": f"خطای سرویس گوگل: {e}"}, status=500)
        except Exception as e:
            return Response({"error": f"خطای ناشناخته: {e}"}, status=500)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": text}]
            )
            chat_text = response.choices[0].message.content
        except Exception as e:
            chat_text = f"خطا در دریافت پاسخ از ChatGPT: {e}"

        try:
            tts = gTTS(text=chat_text, lang="en")
            mp3_path = file_path.rsplit(".", 1)[0] + "_response.mp3"
            file_name = os.path.basename(file_path).rsplit(".", 1)[0] + "_response.mp3"

            relative_path = os.path.join('voice', file_name)

            absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            tts.save(absolute_path)
        except Exception as e:
            return Response({"error": f"خطا در تبدیل متن به صوت: {e}"}, status=500)
        VoiceMessage.objects.create(voice_file=relative_path)
        file_url = request.build_absolute_uri(settings.MEDIA_URL + relative_path)
        return Response({"text": chat_text, "audio_url": file_url})