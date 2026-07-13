import pygame

class Enemy(pygame.sprite.Sprite):
    """
    Represents a enemy in the game
    (parts are outdated)
    """
    def __init__(self, pos):
        """
        Initializes an enemy at a given position
        """
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill("green")
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 2
    
    def update(self):
        """
        Move the enemy downward each frame.

        removes enemy when it eaches the bottom
        """
        self.rect.y += self.speed

        if self.rect.top > 800:
            self.kill()