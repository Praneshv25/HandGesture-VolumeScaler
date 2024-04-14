# HandGesture-VolumeScaler

This project uses Mediapipe and OpenCV to recognize hand gestures to raise and decrease the volume on computers.

## Features

- **Hand Gesture Recognition**: Detects hand gestures using Mediapipe.
- **Volume Control**: Raises or decreases the volume based on recognized gestures.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe

## Installation

To install the required libraries, run the following commands:

```bash
pip install opencv-python
pip install mediapipe
```

## Usage

Run the main script to start controlling the volume with hand gestures.

```bash
python volume_control.py
```

## How it Works

The project uses the following steps to control the volume:

1. **Hand Detection**: OpenCV is used to capture video frames and detect the presence of a hand.
2. **Hand Landmark Recognition**: Mediapipe is used to recognize landmarks on the hand.
3. **Gesture Recognition**: Based on the detected landmarks, specific hand gestures are recognized.
4. **Volume Adjustment**: The recognized gestures are mapped to volume control commands to raise or decrease the volume.

## Demo
# Volume Up Gesture:
![DEMO](https://github.com/Praneshv25/HandGesture-VolumeScaler/blob/b9c901da6554b1350e2ad7dff9986ff8b798e403/Images/Hand%20Gestures%20Shaka%202022%20May%20from%20Rawpixel.webp)
# Volume Down Gesture:
![Demo](https://github.com/Praneshv25/HandGesture-VolumeScaler/blob/915025e1ae0aa8eca61631a8187e775afd514c5c/Images/Hand%20Gestures%20Claw.webp)
