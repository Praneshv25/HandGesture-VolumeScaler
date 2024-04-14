import cv2
import mediapipe as mp
import platform
import time


def pointed_down(key_fingers, reference_fingers):
    for i in key_fingers:
        for j in reference_fingers:
            if i < j:
                return False
    return True


def pointed_up(key_fingers, reference_fingers):
    for i in key_fingers:
        for j in reference_fingers:
            if i > j:
                return False
    return True


def main():
    # Import volume control functions based on the operating system
    if platform.system() == 'Darwin':  # macOS
        import applescript

        # Define AppleScript commands to control volume
        set_volume_script = '''
        tell application "System Events"
            set currentVolume to output volume of (get volume settings)
            set newVolume to currentVolume + {}
            if newVolume < 0 then
                set newVolume to 0
            else if newVolume > 100 then
                set newVolume to 100
            end if
            set volume output volume newVolume
        end tell
        '''

        def set_system_volume(volume_change):
            applescript.run(set_volume_script.format(volume_change))

    elif platform.system() == 'Windows':  # Windows
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        def set_system_volume(volume_change):
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current_volume = volume.GetMasterVolumeLevel()
            volume.SetMasterVolumeLevel(current_volume + volume_change, None)

    else:
        raise NotImplementedError("Volume control is not implemented for this operating system.")

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    # Initialize MediaPipe hands model
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                           min_detection_confidence=0.5, min_tracking_confidence=0.2)

    mp_drawing = mp.solutions.drawing_utils

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process hands detection
        results = hands.process(image_rgb)

        # Check if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on frame
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get y-coordinates of index finger and thumb tips
                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                middle_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
                pinky_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
                ring_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                key_fingers = [pinky_finger_y, thumb_y]
                reference_fingers = [middle_finger_y, index_finger_y, ring_finger_y]

                # Determine hand gesture
                if pointed_up(key_fingers, reference_fingers):
                    hand_gesture = 'pointing up'
                elif pointed_down(key_fingers, reference_fingers):
                    hand_gesture = 'pointing down'
                else:
                    hand_gesture = 'other'

                # Control volume based on hand gesture
                if hand_gesture == 'pointing up':
                    set_system_volume(5)  # Increase volume by 5%
                    time.sleep(0.5)
                elif hand_gesture == 'pointing down':
                    set_system_volume(-5)  # Decrease volume by 5%
                    time.sleep(0.5)

        # Display frame with hand landmarks
        cv2.imshow('Hand Gesture', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()