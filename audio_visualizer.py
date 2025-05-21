import numpy as np
import pygame
from pydub import AudioSegment
from moviepy.editor import ImageSequenceClip
import os

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
FRAME_SIZE = 1024
BASE_RADIUS = 50
MAX_WAVE_RADIUS = 250
POWER = 1.5
NUM_DOTS = 50
MIN_DOT_RADIUS = 2
MAX_DOT_RADIUS = 4

def get_gradient_color(value: float) -> tuple:
    value = min(max(value, 0), 1)
    r = int(255 * value)
    g = int(255 * (1 - value) * 0.75)
    b = 255
    return (r, g, b)

def draw_dots_circle(screen: pygame.Surface, samples: np.ndarray) -> None:
    fft_data = np.fft.fft(samples)
    fft_magnitude = np.abs(fft_data[:len(fft_data) // 2])
    fft_magnitude = np.log1p(fft_magnitude)
    max_magnitude = np.max(fft_magnitude)
    if max_magnitude > 0:
        fft_magnitude /= max_magnitude

    screen.fill((0, 0, 0))
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    average_magnitude = np.mean(fft_magnitude[:len(fft_magnitude) // (NUM_DOTS // 2)])
    wave_radius = int(BASE_RADIUS + (average_magnitude ** POWER) * (MAX_WAVE_RADIUS - BASE_RADIUS))

    for i in range(NUM_DOTS):
        angle = (2 * np.pi / NUM_DOTS) * i
        dot_radius = MIN_DOT_RADIUS + (wave_radius / MAX_WAVE_RADIUS) * (MAX_DOT_RADIUS - MIN_DOT_RADIUS)
        x = center_x + (wave_radius * np.cos(angle))
        y = center_y + (wave_radius * np.sin(angle))
        dot_color = get_gradient_color(average_magnitude)
        pygame.draw.circle(screen, dot_color, (int(x), int(y)), int(dot_radius))

    pygame.display.flip()

def main() -> None:
    try:
        audio_file = r"C:\Users\mukes\Desktop\IBM\IG Mix\mix soft\completed\posted\proj 1\Chall.mp3"
        audio_segment = AudioSegment.from_file(audio_file)
        
        if audio_segment.channels > 1:
            audio_data = np.array(audio_segment.get_array_of_samples()).reshape((-1, audio_segment.channels)).mean(axis=1)
        else:
            audio_data = np.array(audio_segment.get_array_of_samples())

        audio_data = audio_data.astype(np.float32)
        audio_data /= np.max(np.abs(audio_data))

        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Circular Dots Audio Spectrum")
        clock = pygame.time.Clock()

        pygame.mixer.init(frequency=audio_segment.frame_rate, channels=audio_segment.channels)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        frames = []
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if len(audio_data) >= FRAME_SIZE:
                frame = audio_data[:FRAME_SIZE]
                audio_data = audio_data[FRAME_SIZE:]
                draw_dots_circle(screen, frame)

                # Capture the current screen and append it to frames
                frame_data = pygame.surfarray.array3d(screen)
                frames.append(frame_data)

            else:
                running = False

            clock.tick(30)

        pygame.quit()

        # Convert frames to video
        if frames:  # Ensure there are frames to write
            frames = [np.rot90(frame) for frame in frames]
            output_file = "cha_visualization.mp4"
            clip = ImageSequenceClip(frames, fps=30)
            clip.write_videofile(output_file, codec="libx264")

            # Indicate successful download
            if os.path.exists(output_file):
                print(f"Video saved as {output_file}. You can download it from your current working directory.")
            else:
                print("Failed to save the video.")
        else:
            print("No frames were captured. Video was not saved.")

    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()

if __name__ == "__main__":
    main()
