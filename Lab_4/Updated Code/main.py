import warnings

import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.mixer.pre_init(22050, -16, 1)
pygame.init()
if pygame.mixer.get_init() is None:
    try:
        pygame.mixer.init()
    except pygame.error as error:
        warnings.warn(f"Audio effects are unavailable: {error}", RuntimeWarning)

# Screen dimensions
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner - Pygame Version")

# Colors
SKY = (200, 220, 240)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(SKY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                action = engine.handle_event(event)
                if action == "quit":
                    running = False
                elif action is not None:
                    engine.reset(action)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
