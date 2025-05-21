import numpy as np
import pygame
from pydub import AudioSegment

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 1024
MAX_HEIGHT = 300  # Reduced for better visual balance
POWER = 0.5
BAND_DIVISION = 4

# Function to create a color gradient
def get_color_gradient(value: float, index: int, total: int) -> tuple:
    """Returns a color gradient based on the input value."""
    hue = (index / total) * 360
    color = pygame.Color(0)
    color.hsva = (hue, 100, 100)  # Convert HSV to RGB
    return (color.r, color.g, color.b)

# Function to draw the line spectrum
def draw_line_spectrum(screen: pygame.Surface, samples: np.ndarray) -> None:
    """Draws the line spectrum based on the input samples."""
    fft_data = np.fft.fft(samples)
    fft_magnitude = np.abs(fft_data[:len(fft_data) // 2])

    # Normalize using logarithmic scaling
    fft_magnitude = np.log1p(fft_magnitude)
    max_magnitude = np.max(fft_magnitude)
    if max_magnitude > 0:
        fft_magnitude /= max_magnitude

    # Smooth the magnitude using a moving average
    smooth_magnitude = np.convolve(fft_magnitude, np.ones(5)/5, mode='valid')

    # Apply a weighting function to emphasize middle frequencies
    weighting_function = np.exp(-(np.arange(len(smooth_magnitude)) - len(smooth_magnitude) / 2) ** 2 / (len(smooth_magnitude) / 4) ** 2)
    smooth_magnitude *= weighting_function

    # Clear screen
    screen.fill((0, 0, 0))

    # Set parameters
    num_bands = len(smooth_magnitude) // BAND_DIVISION
    band_width = SCREEN_WIDTH // num_bands
    base_height = SCREEN_HEIGHT - 50  # Set spectrum above the bottom

    for i in range(num_bands):
        height = int((smooth_magnitude[i * BAND_DIVISION] ** POWER) * MAX_HEIGHT)
        height = max(height, 5)

        x = i * band_width
        y = base_height - height

        color = get_color_gradient(smooth_magnitude[i * BAND_DIVISION], i, num_bands)
        pygame.draw.rect(screen, color, (x, y, band_width - 2, height))

    pygame.display.flip()

# Main loop
def main() -> None:
    """Runs the main loop."""
    try:
        # Load the audio file
        audio_file = r"C:\Users\audio.mp3" # Replace r"C:\Users\audio.mp3" with your audio file path (Ctrl+Shift+C to copy).
        audio_segment = AudioSegment.from_file(audio_file)
        audio_data = np.array(audio_segment.get_array_of_samples()).astype(np.float32)

        # Normalize audio data
        audio_data /= np.max(np.abs(audio_data))

        # Set up Pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Audio Spectrum")
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
                draw_line_spectrum(screen, frame)

            clock.tick(30)  # Limit frame rate

        pygame.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
