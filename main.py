"""
Program Name: Main.py
Author Antoni Labsz
Purpose: Space invader like game
Starter Code: None
Date: July 12, 2026
"""
import sys
import pygame
from player import Player
from enemy import Enemy

class GameLogic:
    """
    The main game state and loop logic
    - Player input and updates
    - enemy spawning and movement
    - collision detection
    - Score, Lives, and Level tracking
    - Game states (active, reset, game over)
    """
    def __init__(self):
        """
        Initializes all game systems
        -Loads assets
        -creates player and enemy groups
        -sets initial game state
        """
        self.font = pygame.font.Font(None, 60)
        self.game_active = False

        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.level = 1

        self.resetting = False
        self.reset_time = 0
        self.reset_delay = 1000

        self.level_clearing = False

        self.screen = screen

        self.background = pygame.image.load('game_images/background.png').convert()
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        player_sprite = Player((screen_width // 2, screen_height), screen_width, 10)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.hit_timer = 0

        self.enemies = pygame.sprite.Group()
        self.enemy_direction = 1
        self.enemy_speed = 2
        self.enemy_drop = 40

        self.spawn_enemy()

    def run(self):
        """
        Main game loop:
        - Manages game states (menu, active, reset, game over)
        - updates and draws player, nemeis, UI
        - Handles collisons
        - Progresses levles when there is no enemies
        """
        if self.resetting:
            if pygame.time.get_ticks() - self.reset_time < self.reset_delay:
                return
            else:
                self.reset_enemies()
                self.resetting = False


        if not self.game_active:
            self.screen.fill((0,0,0))

            text = self.font.render("Press space to Start", True, "white")
            self.screen.blit(text, (screen_width // 2 - 200, screen_height//2))
            return
        
        self.screen.blit(self.background, (0, 0)) #background drawn first
        
        score_surf = self.font.render(f"Score: {self.score}", True, "white")
        lives_surf = self.font.render(f"Lives: {self.lives}", True, "white")
        high_surf = self.font.render(f"High Score: {self.high_score}", True, "white")
        level_surf = self.font.render(f"Level: {self.level}", True, "white")

        self.screen.blit(score_surf, (900, 70))
        self.screen.blit(lives_surf, (50, 70))
        self.screen.blit(high_surf, (900, 10))
        self.screen.blit(level_surf, (50, 10))

        self.player.update()
        self.player.draw(self.screen)

        for player in self.player:
            player.bullets.update()
            player.bullets.draw(self.screen)

            for bullet in player.bullets:
                hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
                if hits:
                    bullet.kill()
                    self.score += 1
            if pygame.sprite.spritecollide(player, self.enemies, False):
                if pygame.time.get_ticks() - self.hit_timer > 1000:

                    self.lives -= 1
                    self.hit_timer = pygame.time.get_ticks()

                    self.resetting = True
                    self.reset_time = pygame.time.get_ticks()

                if self.lives <=0:
                    self.game_over()


        self.enemy_movement()
        self.enemies.draw(self.screen)

        if len(self.enemies) == 0:
            self.next_level()
    
    def spawn_enemy(self):
        """
        Spawns enemies
        -5 rows and 10 columns
        """
        for row in range(5):
            for col in range(10):
                x = 100 + col * 80
                y = 50 + row * 60
                enemy = Enemy((x, y))
                self.enemies.add(enemy)
    
    def enemy_movement(self):
        """
        Moves enemies closer to player
        - reverses enemy direction on wall hit
        - and moves enemies closer each time they hit the wall
        """
        hit_edge = False

        for enemy in self.enemies:
            enemy.rect.x += self.enemy_speed * self.enemy_direction

            if enemy.rect.right >= screen_width or enemy.rect.left <= 0:
                hit_edge = True

        if hit_edge:
            self.enemy_direction *= -1 #reverses direction

            for enemy in self.enemies:
                enemy.rect.y += self.enemy_drop #move down

    def reset_enemies(self):
        """
        Resets enemy wave
        -clears current enemies
        -spawns new wave
        - resets movement directon
        """
        self.enemies.empty()
        self.spawn_enemy()
        self.enemy_direction = 1

    def next_level(self):
        self.level += 1
        self.spawn_enemy()
        self.level_clearing = False

    def game_over(self):
        """
        Resets game state when player loses all lives:
        - stops game
        - resets player position and bullets
        -updates high score if needed
        -resets score and lives
        """
        self.game_active = False

        self.enemies.empty()
        self.spawn_enemy()

        for player in self.player:
            player.rect.midbottom = (screen_width // 2, screen_height)
            player.bullets.empty()

        if self.score > self.high_score:
            self.high_score = self.score

        self.score = 0
        self.lives = 3

if __name__ == '__main__':
    pygame.init()
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = GameLogic()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game.game_active:
                        game.game_active = True
                    else:
                        for player in game.player:
                            player.shoot()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game.run()

        pygame.display.flip()
        clock.tick(60)