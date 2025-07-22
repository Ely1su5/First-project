import cv2 as cv
import numpy as np
import os
import json
from vosk import Model, KaldiRecognizer
import pyaudio
import time
from datetime import datetime

class Figure():
    def __init__(self, **data):
        if "coordenada1xy" in data:
            self.point1 = data["coordenada1xy"]
        if "coordenada2xy" in data:
            self.point2 = data["coordenada2xy"]
        if "radio" in data:
            self.radius = data["radio"]
        if "color" in data:
            self.color = data["color"]
        else:
            self.color = (0, 255, 0)  # Default green color
        if "grosor" in data:
            self.thickness = data["grosor"]
        else:
            self.thickness = 2  # Default thickness
    
    def draw_line(self, img):
        cv.line(img, self.point1, self.point2, self.color, self.thickness)
        return img
    
    def draw_rectangle(self, img):
        cv.rectangle(img, self.point1, self.point2, self.color, self.thickness)
        return img
    
    def draw_circle(self, img):
        cv.circle(img, self.point1, self.radius, self.color, self.thickness)
        return img

def get_voice_command():
    # Initialize Vosk model
    model_path = "vosk-model-en-us-0.22"
    if not os.path.exists(model_path):
        print(f"Please download the Vosk model from https://alphacephei.com/vosk/models and unpack as {model_path} in the current folder.")
        return None
    
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    
    print("Listening for voice command... (press Ctrl+C to stop)")
    
    try:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                command = result_dict.get("text", "").lower()
                if command:
                    print(f"Voice command recognized: {command}")
                    return command
    except KeyboardInterrupt:
        print("Listening stopped by user")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    return None

def process_voice_command(command, img):
    if not command:
        return img
    
    if "line" in command:
        print("Drawing line from voice command")
        parts = command.split()
        try:
            x1, y1 = int(parts[4]), int(parts[5])
            x2, y2 = int(parts[7]), int(parts[8])
            line = Figure(coordenada1xy=(x1, y1), coordenada2xy=(x2, y2))
            img = line.draw_line(img)
        except (IndexError, ValueError):
            print("Could not parse coordinates from voice command")
    
    elif "rectangle" in command or "square" in command:
        print("Drawing rectangle from voice command")
        parts = command.split()
        try:
            x1, y1 = int(parts[4]), int(parts[5])
            x2, y2 = int(parts[7]), int(parts[8])
            rect = Figure(coordenada1xy=(x1, y1), coordenada2xy=(x2, y2))
            img = rect.draw_rectangle(img)
        except (IndexError, ValueError):
            print("Could not parse coordinates from voice command")
    
    elif "circle" in command:
        print("Drawing circle from voice command")
        parts = command.split()
        try:
            x, y = int(parts[4]), int(parts[5])
            radius = int(parts[8])
            circle = Figure(coordenada1xy=(x, y), radio=radius)
            img = circle.draw_circle(img)
        except (IndexError, ValueError):
            print("Could not parse coordinates from voice command")
    
    elif "record" in command or "video" in command:
        print("Starting video recording...")
        record_video()
    
    elif "screenshot" in command or "capture" in command:
        print("Taking screenshot...")
        take_screenshot(img)
    
    return img

def record_video(duration=10, output_file="output_video.avi"):
    # Initialize video capture
    cap = cv.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video device")
        return
    
    # Get video properties
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = 30
    
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
    
    start_time = time.time()
    
    print(f"Recording for {duration} seconds... (press 'q' to stop early)")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Write the frame to the output file
        out.write(frame)
        
        # Display the frame
        cv.imshow('Recording...', frame)
        
        # Check for duration or key press
        if (time.time() - start_time) > duration:
            break
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release everything when done
    cap.release()
    out.release()
    cv.destroyAllWindows()
    print(f"Video saved as {output_file}")

def take_screenshot(img, output_file=None):
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"screenshot_{timestamp}.png"
    
    cv.imwrite(output_file, img)
    print(f"Screenshot saved as {output_file}")

def show_image_until_w(img, window_name="Image"):
    """
    Muestra una imagen en una ventana hasta que se presione la tecla 'w'
    """
    cv.imshow(window_name, img)
    print(f"Ventana '{window_name}' abierta. Presione 'w' para continuar...")
    while True:
        key = cv.waitKey(0) & 0xFF
        if key == ord('w'):
            break
    cv.destroyAllWindows()

def main():
    # Load image
    img = cv.imread("img1.jpeg")
    if img is None:
        print("Could not open or find the image")
        return
    
    # Display original image
    show_image_until_w(img, "Original Image")
    
    while True:
        print("\nOptions:")
        print("1. Draw line")
        print("2. Draw rectangle")
        print("3. Draw circle")
        print("4. Voice command")
        print("5. Record video")
        print("6. Take screenshot")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            # Draw line
            try:
                x1 = int(input("Enter x1 coordinate: "))
                y1 = int(input("Enter y1 coordinate: "))
                x2 = int(input("Enter x2 coordinate: "))
                y2 = int(input("Enter y2 coordinate: "))
                color = input("Enter color (R G B, default green): ")
                if color:
                    color = tuple(map(int, color.split()))
                else:
                    color = (0, 255, 0)
                thickness = int(input("Enter thickness (default 2): ") or 2)
                
                line = Figure(coordenada1xy=(x1, y1), coordenada2xy=(x2, y2), color=color, grosor=thickness)
                img = line.draw_line(img)
                show_image_until_w(img, "Image with Line")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
        
        elif choice == "2":
            # Draw rectangle
            try:
                x1 = int(input("Enter top-left x coordinate: "))
                y1 = int(input("Enter top-left y coordinate: "))
                x2 = int(input("Enter bottom-right x coordinate: "))
                y2 = int(input("Enter bottom-right y coordinate: "))
                color = input("Enter color (R G B, default green): ")
                if color:
                    color = tuple(map(int, color.split()))
                else:
                    color = (0, 255, 0)
                thickness = int(input("Enter thickness (default 2, -1 for filled): ") or 2)
                
                rect = Figure(coordenada1xy=(x1, y1), coordenada2xy=(x2, y2), color=color, grosor=thickness)
                img = rect.draw_rectangle(img)
                show_image_until_w(img, "Image with Rectangle")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
        
        elif choice == "3":
            # Draw circle
            try:
                x = int(input("Enter center x coordinate: "))
                y = int(input("Enter center y coordinate: "))
                radius = int(input("Enter radius: "))
                color = input("Enter color (R G B, default green): ")
                if color:
                    color = tuple(map(int, color.split()))
                else:
                    color = (0, 255, 0)
                thickness = int(input("Enter thickness (default 2, -1 for filled): ") or 2)
                
                circle = Figure(coordenada1xy=(x, y), radio=radius, color=color, grosor=thickness)
                img = circle.draw_circle(img)
                show_image_until_w(img, "Image with Circle")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
        
        elif choice == "4":
            # Voice command
            command = get_voice_command()
            if command:
                img = process_voice_command(command, img)
                show_image_until_w(img, "Image with Voice Command")
        
        elif choice == "5":
            # Record video
            try:
                duration = int(input("Enter recording duration in seconds (default 10): ") or 10)
                filename = input("Enter output filename (default 'output_video.avi'): ") or "output_video.avi"
                record_video(duration, filename)
            except ValueError:
                print("Invalid input. Please enter a number for duration.")
        
        elif choice == "6":
            # Take screenshot
            filename = input("Enter output filename (default based on timestamp): ") or None
            take_screenshot(img, filename)
        
        elif choice == "7":
            # Exit
            print("Exiting program...")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
    
    # Save the final image
    cv.imwrite("output_image.jpg", img)
    print("Final image saved as 'output_image.jpg'")

if __name__ == "__main__":
    main()