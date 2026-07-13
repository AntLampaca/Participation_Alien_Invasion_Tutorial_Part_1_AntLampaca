import pygame

class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by the player

    - The bullet moves upward each frame and is automatically removed when it leaves the screen.
    """
    def __init__(self, pos):
        """
        Creates a bullet at the given starting position.
        """
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill("red")
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 10

    def update(self):
        """
        Moves the bullet upward each frame
        """
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()