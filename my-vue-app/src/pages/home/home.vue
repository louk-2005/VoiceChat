<template>
  <div class="record-audio">
    <div class="buttons">
      <button @click="startRecording" :disabled="isRecording" class="btn start">
        🎤 Start
      </button>

      <button @click="stopRecording" :disabled="!isRecording" class="btn stop">
        ⏹ Stop
      </button>
    </div>

    <div v-if="isRecording" class="timer">
      ⏱ {{ formatTime(recordingTime) }}
    </div>

    <p v-if="statusMessage" class="status">{{ statusMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isRecording = ref(false)
const statusMessage = ref('')
const recordingTime = ref(0)
let mediaRecorder = null
let audioChunks = []
let timerInterval = null

// شروع ضبط
const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    isRecording.value = true
    statusMessage.value = 'Recording in progress...'
    recordingTime.value = 0

    // تایمر شروع شود
    timerInterval = setInterval(() => {
      recordingTime.value++
    }, 1000)

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }

    mediaRecorder.onstop = handleRecordingStop
    mediaRecorder.start()
  } catch (error) {
    console.error('Microphone access denied:', error)
    statusMessage.value = '❌ Microphone access denied'
  }
}

// توقف ضبط
const stopRecording = () => {
  if (mediaRecorder && isRecording.value) {
    isRecording.value = false
    statusMessage.value = 'Processing audio...'
    clearInterval(timerInterval) // تایمر را متوقف کن
    mediaRecorder.stop()
  }
}

// آپلود صدا
const audioUrl = ref(null) // اضافه کنید در بالای script

const handleRecordingStop = async () => {
  try {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
    audioChunks = []

    const formData = new FormData()
    formData.append('audio_file', audioBlob, 'recording.wav')

    const { data } = await axios.post('http://127.0.0.1:8000/voice/text/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    console.log('Upload success:', data)
    statusMessage.value = '✅ Audio uploaded successfully!'

    // لینک فایل صوتی برگشتی از سرور
    audioUrl.value = data.audio_url

    // پخش خودکار صدا
    if (audioUrl.value) {
      const audio = new Audio(audioUrl.value)
      audio.play()
    }
  } catch (error) {
    console.error('Error uploading file:', error)
    statusMessage.value = '❌ Failed to upload audio'
  }
}





// فرمت کردن زمان به دقیقه:ثانیه
const formatTime = (seconds) => {
  const mins = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${mins}:${secs}`
}
</script>

<style scoped>
.record-audio {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 150px;
  gap: 15px;
  font-family: sans-serif;
}

.buttons {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 10px 18px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  border-radius: 8px;
  font-weight: bold;
  transition: transform 0.2s ease, background-color 0.3s;
}

.start {
  background-color: #34df3b;
  color: white;
}
.start:hover:not(:disabled) {
  background-color: #43a047;
  transform: scale(1.05);
}

.start:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.stop {
  background-color: #f44336;
  color: white;
}
.stop:hover:not(:disabled) {
  background-color: #e53935;
  transform: scale(1.05);
}

.stop:disabled {
  background-color: #ef9a9a;
  cursor: not-allowed;
}

.status {
  font-size: 14px;
  color: #333;
}

.timer {
  font-size: 20px;
  font-weight: bold;
  color: #ff5722;
}
</style>
