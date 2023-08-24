import random

class Ball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = self.random_color()

    @staticmethod
    def random_color():
        """Generate a random color."""
        return (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off top and bottom
        if self.y - 15 < 0 or self.y + 15 > 480:
            self.dy = -self.dy
            self.color = self.random_color()  # Change color if you want the ball to change color on bouncing

    def draw(self, screen):
        import pygame  # Importing here to avoid circular imports
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)

    def collides_with(self, paddle):
        if self.x - 15 < paddle.x + 15 and self.x + 15 > paddle.x:
            if self.y - 15 < paddle.y + 60 and self.y + 15 > paddle.y:
                self.color = self.random_color()  # Change color
                return True
        return False
