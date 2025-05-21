import numpy as np
import pygame
from pydub import AudioSegment
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 1024
RADIUS = 80  # Radius of the central circle
LINE_LENGTH = 150  # Length of the radiating lines
NUM_LINES = 36  # Number of radiating lines

# Function to create vibrant colors
def get_color(value: float) -> tuple:
    """Returns a color based on the input value."""
    r = int(255 * value)
    g = int(150 * (1 - value))  # Dynamic green value for contrast
    b = int(255 * (1 - value))  # Dynamic blue value for vibrance
    return (r, g, b)

# Function to draw the hollow circle
def draw_hollow_circle(screen: pygame.Surface, center: tuple) -> None:
    """Draws the hollow central circle."""
    pygame.draw.circle(screen, (255, 255, 255), center, RADIUS, 5)  # Hollow outline

# Function to draw radiating lines
def draw_radiating_lines(screen: pygame.Surface, center: tuple, magnitudes: np.ndarray) -> None:
    """Draws lines radiating from the circle based on the magnitudes of frequencies."""
    for i in range(NUM_LINES):
        angle = (i / NUM_LINES) * (2 * math.pi)
        length = LINE_LENGTH * (magnitudes[i % len(magnitudes)])  # Scale line length
        start_x = int(center[0] + RADIUS * math.cos(angle))  # Start from the edge of the circle
        start_y = int(center[1] + RADIUS * math.sin(angle))
        end_x = int(start_x + length * math.cos(angle))
        end_y = int(start_y + length * math.sin(angle))

        # Draw the line
        pygame.draw.line(screen, get_color(magnitudes[i % len(magnitudes)]), (start_x, start_y), (end_x, end_y), 3)

# Main loop
def main() -> None:
    """Runs the main loop."""
    try:
        # Load the audio file
        audio_file = r"C:\Users\audio.mp3" #Replace r"C:\Users\audio.mp3" with your audio file path (Ctrl+Shift+C to copy).
        audio_segment = AudioSegment.from_file(audio_file)
        audio_data = np.array(audio_segment.get_array_of_samples()).astype(np.float32)

        # Normalize audio data
        audio_data /= np.max(np.abs(audio_data))

        # Set up Pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Audio Visualizer")
        clock = pygame.time.Clock()

        # Initialize Pygame mixer
        pygame.mixer.init(frequency=audio_segment.frame_rate, channels=audio_segment.channels)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear screen
            screen.fill((0, 0, 0))

            # Read a frame of audio data
            if len(audio_data) >= FRAME_SIZE:
                frame = audio_data[:FRAME_SIZE]
                audio_data = audio_data[FRAME_SIZE:]  # Update audio_data
                
                # Perform FFT to get frequency magnitudes
                fft_data = np.fft.fft(frame)
                fft_magnitude = np.abs(fft_data[:len(fft_data) // 2])
                fft_magnitude = np.log1p(fft_magnitude)  # Logarithmic scaling
                max_magnitude = np.max(fft_magnitude)
                if max_magnitude > 0:
                    fft_magnitude /= max_magnitude  # Normalize

                center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

                draw_hollow_circle(screen, center)  # Draw the hollow nucleus
                draw_radiating_lines(screen, center, fft_magnitude)  # Draw lines

            pygame.display.flip()
            clock.tick(30)  # Limit frame rate

        pygame.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
