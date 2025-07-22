# First Project: Shape Drawing with OpenCV

![OpenCV Logo](https://opencv.org/wp-content/uploads/2020/07/OpenCV_logo_black-2.png)

A Python application that allows users to draw shapes (lines, rectangles, circles) on images using both voice commands and manual input, with additional features for video recording and screenshot capture.

## Features

- **Shape Drawing**:
  - Lines, rectangles, and circles
  - Customizable colors (RGB values)
  - Adjustable thickness or filled shapes
- **Voice Control**:
  - Voice-activated shape drawing
  - Example commands:
    - "Draw line from 100 200 to 300 400"
    - "Draw circle at 150 150 with radius 50"
- **Media Features**:
  - Video recording with adjustable duration
  - Automatic screenshot capture with timestamp
- **Interactive Interface**:
  - Menu-driven console interface
  - Real-time preview of drawings
  - Keyboard-controlled display windows

## Prerequisites

- Python 3.7+
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)
- Vosk Speech Recognition (`pip install vosk`)
- PyAudio (`pip install pyaudio`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/first-project.git
   cd first-project
  
