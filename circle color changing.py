import numpy as np
import pygame
from pydub import AudioSegment
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 1024
RADIUS = 150  # Radius of the medium circle
POWER = 2  # Increase power for more responsiveness
BAND_DIVISION = 4

# Function to create a dynamic color based on time
def get_dynamic_circle_color(time: float) -> tuple:
    """Returns a dynamic color for the circle based on time."""
    r = int(127.5 * (math.sin(time) + 1))  # Ranges from 0 to 255
    g = int(127.5 * (math.sin(time + 2) + 1))  # Ranges from 0 to 255
    b = 255  # Keep blue constant for a cooler tone
    return (r, g, b)

# Function to draw the circular spectrum
def draw_circular_spectrum(screen: pygame.Surface, samples: np.ndarray, circle_color: tuple) -> None:
    """Draws the circular spectrum based on the input samples."""
    fft_data = np.fft.fft(samples)
    fft_magnitude = np.abs(fft_data[:len(fft_data) // 2])

    # Normalize using logarithmic scaling
    fft_magnitude = np.log1p(fft_magnitude)
    max_magnitude = np.max(fft_magnitude)
    if max_magnitude > 0:
        fft_magnitude /= max_magnitude

    # Smooth the magnitude using a moving average
    smooth_magnitude = np.convolve(fft_magnitude, np.ones(5) / 5, mode='valid')

    # Clear screen
    screen.fill((0, 0, 0))

    # Set parameters
    num_bands = len(smooth_magnitude) // BAND_DIVISION
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Draw the spectrum with adjusted angles
    for i in range(num_bands):
        # Map the bands to angles
        if i < num_bands // 2:  # 0 to 180 degrees
            angle = (i / (num_bands // 2)) * math.pi  # 0 to π
        else:  # 180 to 360 degrees
            angle = ((i - (num_bands // 2)) / (num_bands // 2)) * math.pi + math.pi  # π to 2π

        # Ensure symmetry by mirroring the angles
        angle_mirror = angle + math.pi  # Mirror angle for the other half

        for angle in (angle, angle_mirror):
            start_x = int(center_x + RADIUS * np.cos(angle))
            start_y = int(center_y + RADIUS * np.sin(angle))

            # Calculate line length extending outward
            line_length = RADIUS + int((smooth_magnitude[i * BAND_DIVISION] ** POWER) * 50)
            line_length = max(line_length, RADIUS + 5)  # Ensure it doesn't shrink below the circle's radius

            end_x = int(center_x + line_length * np.cos(angle))
            end_y = int(center_y + line_length * np.sin(angle))

            # Draw spectrum line with circle's color
            pygame.draw.line(screen, circle_color, (start_x, start_y), (end_x, end_y), 2)

    # Draw the dynamic gradient circle
    current_time = pygame.time.get_ticks() / 1000  # Get time in seconds
    circle_color = get_dynamic_circle_color(current_time)  # Get color based on time
    pygame.draw.circle(screen, circle_color, (center_x, center_y), RADIUS, 5)  # Draw circle outline

    pygame.display.flip()

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
        pygame.display.set_caption("Dynamic Circular Audio Spectrum")
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
                circle_color = get_dynamic_circle_color(pygame.time.get_ticks() / 1000)  # Update circle color
                draw_circular_spectrum(screen, frame, circle_color)

            clock.tick(30)  # Limit frame rate

        pygame.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
