import numpy as np
import pygame
from pydub import AudioSegment

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 1024
BAR_COUNT = 40  # Number of bars
MAX_BAR_HEIGHT = 300  # Maximum height of the bars

# Function to create vibrant colors
def get_color(value: float) -> tuple:
    """Returns a color based on the input value."""
    r = int(255 * value)
    g = int(150 * (1 - value))  # Dynamic green value for contrast
    b = int(255 * (1 - value))  # Dynamic blue value for vibrance
    return (r, g, b)

# Function to draw the spectrum bars
def draw_bars(screen: pygame.Surface, magnitudes: np.ndarray) -> None:
    """Draws bars based on the magnitudes of frequencies."""
    bar_width = SCREEN_WIDTH // BAR_COUNT  # Calculate width of each bar
    for i in range(BAR_COUNT):
        bar_height = int(magnitudes[i % len(magnitudes)] * MAX_BAR_HEIGHT)
        bar_x = i * bar_width
        bar_y = SCREEN_HEIGHT - bar_height  # Position bars at the bottom

        # Draw the bar
        pygame.draw.rect(screen, get_color(magnitudes[i % len(magnitudes)]), (bar_x, bar_y, bar_width - 2, bar_height))

# Main loop
def main() -> None:
    """Runs the main loop."""
    try:
        # Load the audio file
        audio_file = r"C:\Users\mukes\Desktop\IBM\IG Mix\mix soft\hayyoda.mp3"  # Replace with your audio file path
        audio_segment = AudioSegment.from_file(audio_file)
        audio_data = np.array(audio_segment.get_array_of_samples()).astype(np.float32)

        # Normalize audio data
        audio_data /= np.max(np.abs(audio_data))

        # Set up Pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Line Spectrum Visualizer")
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

                draw_bars(screen, fft_magnitude)  # Draw bars

            pygame.display.flip()
            clock.tick(30)  # Limit frame rate

        pygame.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
