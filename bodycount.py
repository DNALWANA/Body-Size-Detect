import cv2
import sys
import numpy as np
import threading
import os
from gtts import gTTS
import pygame

# --- INISIALISASI SUARA ---
pygame.mixer.init()
VOICE_FILE = "status_voice.mp3"

def speak(text):
    try:
        # Hapus file lama jika ada agar tidak bentrok
        if os.path.exists(VOICE_FILE):
            pygame.mixer.music.unload() # Pastikan file tidak sedang dikunci
        
        tts = gTTS(text=text, lang='id') # Menggunakan bahasa Indonesia
        tts.save(VOICE_FILE)
        pygame.mixer.music.load(VOICE_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Gagal memutar suara: {e}")

# --- INISIALISASI MEDIAPIPE ---
try:
    import mediapipe as mp
    from mediapipe.python.solutions import pose as mp_pose
    from mediapipe.python.solutions import drawing_utils as mp_drawing
    print("[INFO] Library MediaPipe berhasil dimuat.")
except Exception as e:
    print(f"[ERROR] Masalah pada library: {e}")
    sys.exit()

pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

# --- VARIABEL STATE (STATUS TERAKHIR) ---
current_status = None # Untuk menyimpan status terakhir (GEMUK/IDEAL)

print("[INFO] Program Berjalan. Tekan 'Q' untuk berhenti.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    h, w, _ = frame.shape
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark

        # 1. Koordinat Bounding Box
        x_points = [int(lm.x * w) for lm in landmarks]
        y_points = [int(lm.y * h) for lm in landmarks]
        x_min, x_max = min(x_points), max(x_points)
        y_min, y_max = min(y_points), max(y_points)

        # 2. Logika Rasio Perut (Hip) vs Bahu (Shoulder)
        shoulder_width = abs(landmarks[11].x - landmarks[12].x)
        waist_width = abs(landmarks[23].x - landmarks[24].x)
        ratio = waist_width / shoulder_width if shoulder_width > 0 else 0

        # 3. Klasifikasi dengan SENSITIVITAS (Ganti 0.80 sesuai keinginanmu)
        new_status = "GEMUK" if ratio > 0.60 else "IDEAL"

        # 4. LOGIKA SUARA SEKALI SAAT BERUBAH
        if new_status != current_status:
            current_status = new_status # Update status terbaru
            
            if current_status == "GEMUK":
                pesan = "gemuk banget bro wkwkw diet bro"
                color = (0, 0, 255)
            else:
                pesan = "tubuhmu sudah ideal king"
                color = (0, 255, 0)
            
            # Jalankan suara di thread terpisah agar kamera tidak lag
            threading.Thread(target=speak, args=(pesan,)).start()
        
        # Tentukan warna berdasarkan status sekarang
        box_color = (0, 0, 255) if current_status == "GEMUK" else (0, 255, 0)

        # 5. Visualisasi
        cv2.rectangle(frame, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), box_color, 3)
        cv2.putText(frame, f"{current_status} ({ratio:.2f})", (x_min, y_min - 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, box_color, 3)

    cv2.imshow("Body Analysis Voice", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
if os.path.exists(VOICE_FILE): os.remove(VOICE_FILE)



