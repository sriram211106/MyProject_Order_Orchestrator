import pygame
from .player import Player
from .obstacle import Obstacle
from .sound_effects import SoundEffects

# Game Engine

WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)
BLACK = (0, 0, 0)
DIFFICULTIES = {
    "Easy": (4.5, 95),
    "Medium": (6.0, 70),
    "Hard": (8.0, 55),
}
MAX_SPEED = 12.0


class GameEngine:
    def __init__(self, width, height, difficulty="Medium", sound_effects=None):
        self.width = width
        self.height = height
        self.ground_y = height - 40
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.sounds = sound_effects
        if self.sounds is None and pygame.mixer.get_init():
            self.sounds = SoundEffects()

        self.reset(difficulty)

    def reset(self, difficulty="Medium"):
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty}")

        self.difficulty = difficulty
        starting_speed, self.spawn_interval = DIFFICULTIES[difficulty]
        self.player = Player(80, self.ground_y)
        self.speed = starting_speed
        self.speed_increase_per_frame = 0.003
        self._spawn_timer = 0
        self.obstacles = []
        self.distance = 0
        self.score = 0
        self.game_over = False

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            return "quit"

        if self.game_over:
            difficulty_keys = {
                pygame.K_1: "Easy",
                pygame.K_2: "Medium",
                pygame.K_3: "Hard",
            }
            return difficulty_keys.get(event.key)

        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            was_on_ground = self.player.on_ground
            self.player.jump()
            if was_on_ground and self.sounds is not None:
                self.sounds.play_jump()
        return None

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self.speed = min(MAX_SPEED, self.speed + self.speed_increase_per_frame)
        previous_player = (
            self.player.x,
            self.player.y,
            self.player.width,
            self.player.height,
        )
        self.player.update()
        current_player = (
            self.player.x,
            self.player.y,
            self.player.width,
            self.player.height,
        )

        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.obstacles.append(Obstacle(self.width, self.ground_y, self.speed))

        for obstacle in self.obstacles:
            previous_obstacle = (
                obstacle.x,
                obstacle.y,
                obstacle.width,
                obstacle.height,
            )
            obstacle.move()
            obstacle.speed = self.speed
            current_obstacle = (
                obstacle.x,
                obstacle.y,
                obstacle.width,
                obstacle.height,
            )
            if self._swept_collision(
                previous_player,
                current_player,
                previous_obstacle,
                current_obstacle,
            ):
                self.game_over = True
                if self.sounds is not None:
                    self.sounds.play_game_over()
                return

        for obstacle in self.obstacles:
            if not obstacle.scored and obstacle.x + obstacle.width < self.player.x:
                obstacle.scored = True
                self.score += 1
                if self.sounds is not None:
                    self.sounds.play_score()

        self.obstacles = [o for o in self.obstacles if not o.off_screen()]

        self.distance += self.speed

    @staticmethod
    def _swept_collision(player_start, player_end, obstacle_start, obstacle_end):
        relative_x = obstacle_start[0] - player_start[0]
        relative_y = obstacle_start[1] - player_start[1]
        velocity_x = (obstacle_end[0] - obstacle_start[0]) - (
            player_end[0] - player_start[0]
        )
        velocity_y = (obstacle_end[1] - obstacle_start[1]) - (
            player_end[1] - player_start[1]
        )

        def axis_times(position, velocity, lower_bound, upper_bound):
            if velocity == 0:
                if lower_bound < position < upper_bound:
                    return float("-inf"), float("inf")
                return None
            first = (lower_bound - position) / velocity
            second = (upper_bound - position) / velocity
            return min(first, second), max(first, second)

        x_times = axis_times(
            relative_x,
            velocity_x,
            -obstacle_start[2],
            player_start[2],
        )
        y_times = axis_times(
            relative_y,
            velocity_y,
            -obstacle_start[3],
            player_start[3],
        )
        if x_times is None or y_times is None:
            return False

        entry_time = max(x_times[0], y_times[0], 0)
        exit_time = min(x_times[1], y_times[1], 1)
        return entry_time < exit_time

    def render(self, screen):
        pygame.draw.line(screen, BROWN, (0, self.ground_y), (self.width, self.ground_y), 4)

        if self.game_over:
            self._render_game_over(screen)
            return

        pygame.draw.rect(screen, WHITE, self.player.rect())
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, DARK_GREEN, obstacle.rect())

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def _render_game_over(self, screen):
        panel = pygame.Rect(80, 45, self.width - 160, self.height - 90)
        pygame.draw.rect(screen, WHITE, panel, border_radius=12)
        pygame.draw.rect(screen, DARK_GREEN, panel, width=3, border_radius=12)

        title = self.title_font.render("Game Over", True, BLACK)
        final_score = self.font.render(f"Final score: {self.score}", True, BLACK)
        prompt = self.small_font.render("Choose a difficulty to play again:", True, BLACK)
        choices = (
            self.small_font.render("1 - Easy: speed 4.5, spawn every 95 frames", True, BLACK),
            self.small_font.render("2 - Medium: speed 6, spawn every 70 frames", True, BLACK),
            self.small_font.render("3 - Hard: speed 8, spawn every 55 frames", True, BLACK),
        )
        exit_prompt = self.small_font.render("Esc - Exit", True, BLACK)

        for text, y in (
            (title, 95),
            (final_score, 155),
            (prompt, 210),
        ):
            screen.blit(text, text.get_rect(center=(self.width // 2, y)))
        for text, y in zip(choices, (240, 270, 300)):
            screen.blit(text, text.get_rect(center=(self.width // 2, y)))
        screen.blit(exit_prompt, exit_prompt.get_rect(center=(self.width // 2, 330)))
