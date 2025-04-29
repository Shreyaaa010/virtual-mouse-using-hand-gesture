
import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.FAILSAFE = True  # Failsafe(*DO NOT REMOVE THIS FAILSAFE*)

# Initialize MediaPipe Hands

hand_skeleton = mp.solutions.hands
hands = hand_skeleton.Hands(max_num_hands=2, static_image_mode=False,min_detection_confidence=0.8, min_tracking_confidence=0.8)

mp_draw = mp.solutions.drawing_utils  # Utility to draw hand landmarks

camera = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
print(screen_width,screen_height)

while True:
    ret, frame = camera.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip horizontally for a mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB

    results = hands.process(rgb_frame)  # Detect hands

    if results.multi_hand_landmarks:
        right_hand = None
        left_hand = None
        for i, hand in enumerate(results.multi_hand_landmarks):
            label = results.multi_handedness[i].classification[0].label  # 'Right' or 'Left'

            if label == "Right":
                right_hand = hand
            elif label == "Left":
                left_hand = hand
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, hand_skeleton.HAND_CONNECTIONS)# Draw hand landmarks and skeleton


        if right_hand:                                # For right hand
            thumb_tip = right_hand.landmark[4]
            thumb_mcp = right_hand.landmark[2]
            index_finger_tip = right_hand.landmark[8]
            index_finger_mcp = right_hand.landmark[5]
            middle_finger_tip = right_hand.landmark[12]
            middle_finger_mcp = right_hand.landmark[9]
            ring_finger_tip = right_hand.landmark[16]
            ring_finger_mcp = right_hand.landmark[13]
            pinky_tip = right_hand.landmark[20]
            pinky_mcp = right_hand.landmark[17]

            index_finger_extended = index_finger_mcp.y > index_finger_tip.y
            middle_finger_extended = middle_finger_mcp.y > middle_finger_tip.y
            ring_finger_extended = ring_finger_mcp.y > ring_finger_tip.y
            pinky_extended = pinky_mcp.y > pinky_tip.y

            hand_width = max(abs(index_finger_mcp.x - pinky_mcp.x), 0.01)#thumb normalize
            thumb_normalized_x = (thumb_tip.x - thumb_mcp.x) / hand_width
            thumb_extended = thumb_normalized_x > 0.1

            Sensitivity = 2
            screen_x = int((index_finger_tip.x * screen_width) * Sensitivity)# for movement (mapped to index finger)
            screen_y = int((index_finger_tip.y * screen_height) * Sensitivity)
            pyautogui.moveTo(screen_x, screen_y, duration=0)

            if thumb_extended and index_finger_extended and middle_finger_extended and ring_finger_extended and pinky_extended:                            #For left click (right thumb)
                pyautogui.click()

            if  not middle_finger_extended and  not thumb_extended and index_finger_extended and ring_finger_extended and pinky_extended:        #for right click(middle finger)
                pyautogui.rightClick()

            if thumb_extended and index_finger_extended and not middle_finger_extended and not ring_finger_extended and not pinky_extended:
                screenshot = pyautogui.screenshot()  # Screenshot
                screenshot.save(r"C:\Users\HP\screenshot2.png")
                time.sleep(2)



        if left_hand :                                         # For left hand
            thumb_tip1 = left_hand.landmark[4]
            thumb_mcp1 = left_hand.landmark[2]
            index_finger_tip1 = left_hand.landmark[8]
            index_finger_mcp1 = left_hand.landmark[5]
            middle_finger_tip1 = left_hand.landmark[12]
            middle_finger_mcp1 = left_hand.landmark[9]
            ring_finger_tip1 = left_hand.landmark[16]
            ring_finger_mcp1 = left_hand.landmark[13]
            pinky_tip1 = left_hand.landmark[20]
            pinky_mcp1 = left_hand.landmark[17]

            index_finger_extended = index_finger_mcp1.y > index_finger_tip1.y
            middle_finger_extended = middle_finger_mcp1.y > middle_finger_tip1.y
            ring_finger_extended = ring_finger_mcp1.y > ring_finger_tip1.y
            pinky_extended = pinky_mcp1.y > pinky_tip1.y

            hand_width = max(abs(index_finger_mcp1.x - pinky_mcp1.x), 0.01)  # thumb normalize
            thumb_normalized_x = (thumb_tip1.x - thumb_mcp1.x) / hand_width
            thumb_extended = thumb_normalized_x > 0.1

            if not thumb_extended and index_finger_extended and middle_finger_extended and ring_finger_extended and pinky_extended: # scroll down
                pyautogui.scroll(-100)

            if not ring_finger_extended and not pinky_extended and index_finger_extended and middle_finger_extended and thumb_extended:   #scroll up
                pyautogui.scroll(100)

            if not ring_finger_extended and not middle_finger_extended and not ring_finger_extended and not pinky_extended and thumb_extended :   # copu
                pyautogui.hotkey('ctrl', 'c')

            if not ring_finger_extended and not middle_finger_extended and not ring_finger_extended and not pinky_extended and not thumb_extended:  # paste
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.PAUSE = 2


    resized_frame=cv2.resize(frame,(800,600))
    cv2.imshow("Both Hand Skeleton", resized_frame)  # Show output(Have to remove this line afterwards )

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.release()
cv2.destroyAllWindows()
