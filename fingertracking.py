import cv2
import mediapipe as mp
import numpy as np
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def calculate_angle(a, b, c):
    """
    Menghitung sudut antara tiga titik.
    Sudut dibentuk di titik b.
    """
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    angle = np.degrees(angle)
    
    return angle

while True:
    success, img = cap.read()
    if not success:
        print("Gagal mengakses kamera")
        break
        
    img = cv2.flip(img, 1)
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    finger_count = 0
  
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        handedness = results.multi_handedness[0].classification[0].label
        
        # Struktur landmark tangan:
        # 0: pergelangan tangan
        # 1-4: jempol (1: pangkal, 4: ujung)
        # 5-8: telunjuk (5: pangkal, 8: ujung)
        # 9-12: jari tengah (9: pangkal, 12: ujung)
        # 13-16: jari manis (13: pangkal, 16: ujung)
        # 17-20: kelingking (17: pangkal, 20: ujung)
        
        # Definisikan landmark untuk setiap jari
        fingers_landmarks = [
            [0, 1, 2, 3, 4],       # jempol
            [0, 5, 6, 7, 8],       # telunjuk
            [0, 9, 10, 11, 12],    # tengah
            [0, 13, 14, 15, 16],   # manis
            [0, 17, 18, 19, 20]    # kelingking
        ]
        
        #Menghitung Jari
        fingers = []
        
       
        thumb_angle = calculate_angle(
            hand_landmarks.landmark[1], 
            hand_landmarks.landmark[2], 
            hand_landmarks.landmark[4]
        )
        
        if thumb_angle > 150:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for finger_idx in range(1, 5):
         
            mcp = fingers_landmarks[finger_idx][1]  
            pip = fingers_landmarks[finger_idx][2]  
            dip = fingers_landmarks[finger_idx][3]  
            tip = fingers_landmarks[finger_idx][4]  
            
            
            finger_angle = calculate_angle(
                hand_landmarks.landmark[mcp],
                hand_landmarks.landmark[pip],
                hand_landmarks.landmark[dip]
            )
            
           
            if finger_angle > 160:
                fingers.append(1)
            else:
                fingers.append(0)
        
   
        finger_count = sum(fingers)
        
     
        cv2.rectangle(img, (20, 20), (170, 120), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(finger_count), (45, 90), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
        
       
        finger_names = ["Jempol", "Telunjuk", "Tengah", "Manis", "Kelingking"]
        for i, status in enumerate(fingers):
            status_text = f"{finger_names[i]}: {'Terangkat' if status == 1 else 'Turun'}"
            cv2.putText(img, status_text, (10, 150 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
  
    cv2.imshow("Penghitung Jari", img)
    
    #
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
