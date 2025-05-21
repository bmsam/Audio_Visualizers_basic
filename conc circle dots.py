import numpy as np
import pygame
from pydub import AudioSegment

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 1024
BASE_RADIUS = 50
MAX_WAVE_RADIUS = 250
POWER = 1.5
NUM_DOTS = 50  # Maximum number of dots in the outer circle

# Function to create a vibrant color based on audio magnitude
def get_vibrant_color(value: float) -> tuple:
    """Returns a vibrant blue and green or blue and pink color based on the input value."""
    if value < 0.5:
        # Blue to Green gradient
        r = 0
        g = int(255 * (value * 2))  # Linear interpolation
        b = 255
    else:
        # Blue to Pink gradient
        r = int(255 * ((value - 0.5) * 2))  # Linear interpolation
        g = 0
        b = 255
    
    return (r, g, b)

# Function to draw the dots on the outer circle
def draw_dots_circle(screen: pygame.Surface, samples: np.ndarray) -> None:
    fft_data = np.fft.fft(samples)
    fft_magnitude = np.abs(fft_data[:len(fft_data) // 2])

    # Normalize using logarithmic scaling
    fft_magnitude = np.log1p(fft_magnitude)
    max_magnitude = np.max(fft_magnitude)
    if max_magnitude > 0:
        fft_magnitude /= max_magnitude

    # Clear screen
    screen.fill((0, 0, 0))

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Calculate average magnitude for wave effect
    average_magnitude = np.mean(fft_magnitude[:len(fft_magnitude) // (NUM_DOTS // 2)])
    wave_radius = int(BASE_RADIUS + (average_magnitude ** POWER) * (MAX_WAVE_RADIUS - BASE_RADIUS))

    # Calculate dot positions and sizes
    for i in range(NUM_DOTS):
        angle = (2 * np.pi / NUM_DOTS) * i
        dot_radius = 5 + (wave_radius / MAX_WAVE_RADIUS) * 10  # Vary dot size based on wave radius

        # Calculate dot position
        x = center_x + (wave_radius * np.cos(angle))
        y = center_y + (wave_radius * np.sin(angle))

        # Get vibrant color for the dot
        dot_color = get_vibrant_color(average_magnitude)

        # Draw the dot
        pygame.draw.circle(screen, dot_color, (int(x), int(y)), int(dot_radius))

    pygame.display.flip()

# Main loop
def main() -> None:
    try:
        # Load the audio file
        audio_file = r"C:\Users\audio.mp3" #Replace r"C:\Users\audio.mp3" with your audio file path (Ctrl+Shift+C to copy).
        audio_segment = AudioSegment.from_file(audio_file)

        # Handle stereo audio
        if audio_segment.channels > 1:
            audio_data = np.array(audio_segment.get_array_of_samples()).reshape((-1, audio_segment.channels)).mean(axis=1)
        else:
            audio_data = np.array(audio_segment.get_array_of_samples())

        audio_data = audio_data.astype(np.float32)
        audio_data /= np.max(np.abs(audio_data))

        # Set up Pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Circular Dots Audio Spectrum")
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

            # Read a frame of audio data
            if len(audio_data) >= FRAME_SIZE:
                frame = audio_data[:FRAME_SIZE]
                audio_data = audio_data[FRAME_SIZE:]  # Update audio_data
                draw_dots_circle(screen, frame)
            else:
                running = False  # Stop if there are no more audio frames

            clock.tick(30)  # Limit frame rate

        pygame.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
