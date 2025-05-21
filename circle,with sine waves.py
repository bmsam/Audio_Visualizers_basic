import numpy as np
import pygame
from pydub import AudioSegment
import math
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 1024
RADIUS = 150  # Radius of the medium circle
POWER = 2  # Power for better visibility
NUM_SINE_WAVES = 3  # Number of sine waves
DANCE_SPEED = 0.1  # Speed for the sine wave movement

# Function to create a gradient color for the circle outline
def get_gradient_color(time: float) -> tuple:
    """Returns a gradient color for the circle based on time."""
    r = int(127.5 * (math.sin(time) + 1))
    g = int(127.5 * (math.sin(time + 2) + 1))
    b = 255  # Keep blue constant
    return (r, g, b)

# Function to draw sine waves around a circle
def draw_circular_sine_waves(screen: pygame.Surface, samples: np.ndarray, time: float) -> None:
    """Draws multiple sine waves around a circle based on the input samples."""
    fft_data = np.fft.fft(samples)
    fft_magnitude = np.abs(fft_data[:len(fft_data) // 2])

    # Normalize using logarithmic scaling
    fft_magnitude = np.log1p(fft_magnitude)
    max_magnitude = np.max(fft_magnitude)
    if max_magnitude > 0:
        fft_magnitude /= max_magnitude

    # Clear screen
    screen.fill((0, 0, 0))

    # Set parameters
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    num_points = 360  # Number of points around the circle

    # Draw sine waves
    for wave_index in range(NUM_SINE_WAVES):
        frequency = random.uniform(0.02, 0.05)  # Random frequency for smoother movement
        offset_angle = wave_index * (360 / NUM_SINE_WAVES) * (math.pi / 180)  # Offset for each wave

        for angle in range(num_points):
            # Calculate the corresponding FFT index
            index = int((angle / num_points) * (len(fft_magnitude) - 1))
            if index < len(fft_magnitude):
                amplitude = (fft_magnitude[index] ** POWER) * RADIUS * 0.5  # Scale the amplitude
            else:
                amplitude = 0

            # Calculate the position on the circle
            theta = math.radians(angle) + offset_angle + (time * DANCE_SPEED)
            x = center_x + int((RADIUS + amplitude) * math.cos(theta))
            y = center_y + int((RADIUS + amplitude) * math.sin(theta))

            # Draw the point of the sine wave
            color = get_gradient_color(time)  # Get gradient color for the current wave
            pygame.draw.circle(screen, color, (x, y), 2)

    # Draw the gradient circle outline
    pygame.draw.circle(screen, get_gradient_color(time), (center_x, center_y), RADIUS, 5)  # Draw circle outline

    pygame.display.flip()

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
        pygame.display.set_caption("Gradient Circular Sine Wave Audio Visualizer")
        clock = pygame.time.Clock()

        # Initialize Pygame mixer
        pygame.mixer.init(frequency=audio_segment.frame_rate, channels=audio_segment.channels)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        running = True
        start_time = pygame.time.get_ticks() / 1000  # Start time in seconds
        while running:
            current_time = pygame.time.get_ticks() / 1000 - start_time  # Elapsed time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Read a frame of audio data
            if len(audio_data) >= FRAME_SIZE:
                frame = audio_data[:FRAME_SIZE]
                audio_data = audio_data[FRAME_SIZE:]  # Update audio_data
                draw_circular_sine_waves(screen, frame, current_time)

            clock.tick(30)  # Limit frame rate

        pygame.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
