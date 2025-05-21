import numpy as np
import pygame
from pydub import AudioSegment

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 1024
NUM_ROWS = 20
NUM_COLS = 40

# Function to load the audio file
def load_audio_file(file_path):
    try:
        audio_segment = AudioSegment.from_file(file_path)
        audio_data = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
        return audio_data
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None

# Function to initialize Pygame
def init_pygame():
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Audio Spectrum")
        clock = pygame.time.Clock()
        return screen, clock
    except Exception as e:
        print(f"Error initializing Pygame: {e}")
        return None, None

# Function to draw a character
def draw_char(screen, x, y, char, amplitude, color):
    font = pygame.font.Font(None, 24)
    text = font.render(char, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    if amplitude > 0.5:
        pygame.draw.circle(screen, color, (x, y), int(amplitude * 10))

# Function to draw the character grid
def draw_char_grid(screen, samples):
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
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            # Calculate amplitude
            index = (i * NUM_COLS + j) % len(fft_magnitude)
            amplitude = fft_magnitude[index]
            amplitude_clamped = min(amplitude, 1)

            # Choose color based on amplitude
            color_index = int(amplitude_clamped * (len(colors) - 1))
            color = colors[color_index]

            # Draw character
            draw_char(screen, j * (SCREEN_WIDTH // NUM_COLS) + 20, i * (SCREEN_HEIGHT // NUM_ROWS) + 20, '#', amplitude, color)

    pygame.display.flip()

# Main loop
def main():
    audio_file = r"C:\Users\audio.mp3" #Replace r"C:\Users\audio.mp3" with your audio file path (Ctrl+Shift+C to copy).
    audio_data = load_audio_file(audio_file)
    if audio_data is None:
        return

    screen, clock = init_pygame()
    if screen is None:
        return

    pygame.mixer.init(frequency=44100, channels=2)
    try:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing audio: {e}")
        return

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Read a frame of audio data
        if len(audio_data) >= FRAME_SIZE:
            frame = audio_data[:FRAME_SIZE]
            audio_data = audio_data[FRAME_SIZE:]  # Update audio_data
            draw_char_grid(screen, frame)

        clock.tick(30)  # Limit frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
