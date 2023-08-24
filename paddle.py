class Paddle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dy = 0
        self.color = color

    def move(self):
        self.y += self.dy

        # Keep paddle inside screen
        if self.y < 0:
            self.y = 0
        if self.y + 60 > 480:
            self.y = 480 - 60

    def draw(self, screen):
        import pygame  # Importing here to avoid circular imports
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, 15, 60))
