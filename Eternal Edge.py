import pygame
import math

class KnifeHitGame:
    def __init__(self):
        pygame.init()
        
        # Screen Constants
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 700
        self.FPS = 60
        
        # Colors
        self.WHITE = (240, 240, 240)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        
        # Game Settings
        self.CIRCLE_CENTER = (self.SCREEN_WIDTH // 2, 200)
        self.CIRCLE_RADIUS = 100
        self.ROTATION_SPEED = 2
        self.KNIFE_SPEED = 15
        self.COLLISION_THRESHOLD = 15
        self.TOTAL_KNIVES = 20
        
        # Setup Display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Knife Hit Game")
        self.clock = pygame.time.Clock()
        
        # Load Images
        self.knife_img = pygame.image.load("knife.png")
        self.knife_img = pygame.transform.scale(self.knife_img, (30, 100))
        self.knife_width = self.knife_img.get_width()
        self.knife_height = self.knife_img.get_height()
        
        # Load and scale circle image
        self.circle_img = pygame.image.load("circle.png")  # Replace with your image name
        self.circle_img = pygame.transform.scale(self.circle_img, 
                                               (self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2))
        # Create a copy for rotation
        self.original_circle = self.circle_img
        
        # Game State
        self.reset_game()

    def reset_game(self):
        self.knives = []
        self.knife_thrown = False
        self.knife_x = self.SCREEN_WIDTH // 2 - self.knife_width // 2
        self.knife_y = self.SCREEN_HEIGHT - 100
        self.circle_angle = 0
        self.knives_remaining = self.TOTAL_KNIVES
        self.game_over = False
        self.level_complete = False

    def draw_circle_and_knives(self):
        # Rotate the circle image
        rotated_circle = pygame.transform.rotate(self.original_circle, self.circle_angle)
        circle_rect = rotated_circle.get_rect(center=self.CIRCLE_CENTER)
        self.screen.blit(rotated_circle, circle_rect)
        
        # Draw embedded knives
        for knife in self.knives:
            angle = knife["angle"] + self.circle_angle
            
            # Calculate position so only the tip enters the circle
            x = self.CIRCLE_CENTER[0] + (self.CIRCLE_RADIUS - 20) * math.cos(math.radians(angle))
            y = self.CIRCLE_CENTER[1] + (self.CIRCLE_RADIUS - 20) * math.sin(math.radians(angle))
            
            # Rotate knife to point towards center
            rotated_knife = pygame.transform.rotate(self.knife_img, -angle + 90)
            
            # Position knife so only its tip enters the circle
            knife_rect = rotated_knife.get_rect()
            knife_rect.center = (
                x + (knife_rect.height // 2 - 20) * math.cos(math.radians(angle)),
                y + (knife_rect.height // 2 - 20) * math.sin(math.radians(angle))
            )
            
            self.screen.blit(rotated_knife, knife_rect)
        
        # Update rotation
        self.circle_angle = (self.circle_angle + self.ROTATION_SPEED) % 360

    def check_collision(self, new_angle):
        return any(abs(knife["angle"] - new_angle) < self.COLLISION_THRESHOLD for knife in self.knives)

    def draw_ui(self):
        # Draw remaining knives counter
        font = pygame.font.Font(None, 36)
        text = font.render(f'Knives: {self.knives_remaining}', True, self.BLACK)
        self.screen.blit(text, (20, self.SCREEN_HEIGHT - 40))

        # Draw game over or level complete message
        font = pygame.font.Font(None, 74)
        if self.game_over:
            text = font.render('Game Over!', True, self.RED)
            self.screen.blit(text, (self.SCREEN_WIDTH//2 - text.get_width()//2, self.SCREEN_HEIGHT//2))
        elif self.level_complete:
            text = font.render('Level Complete!', True, self.BLACK)
            self.screen.blit(text, (self.SCREEN_WIDTH//2 - text.get_width()//2, self.SCREEN_HEIGHT//2))

    def update(self):
        if self.knife_thrown:
            self.knife_y -= self.KNIFE_SPEED
            if self.knife_y <= self.CIRCLE_CENTER[1] + self.CIRCLE_RADIUS:
                knife_angle = (360 - self.circle_angle) % 360
                
                if self.check_collision(knife_angle):
                    self.game_over = True
                else:
                    self.knives.append({"angle": knife_angle})
                    self.knives_remaining -= 1
                    self.knife_thrown = False
                    self.knife_y = self.SCREEN_HEIGHT - 100
                    
                    if self.knives_remaining == 0:
                        self.level_complete = True

    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and not self.knife_thrown:
                    if event.key == pygame.K_SPACE and not (self.game_over or self.level_complete):
                        self.knife_thrown = True
                    elif event.key == pygame.K_r:
                        self.reset_game()
            
            self.draw_circle_and_knives()
            self.update()
            
            if self.knife_thrown or self.knives_remaining > 0:
                self.screen.blit(self.knife_img, (self.knife_x, self.knife_y))
            
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

if __name__ == "__main__":
    game = KnifeHitGame()
    game.run()
