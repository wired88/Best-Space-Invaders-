import pygame
from GameClasses import GameWindow, Explosion
from MotherClasses import Spaceships, Bullet
import math


class LevelThreeWindow(GameWindow):
    def __init__(self, caption, image):
        super().__init__(caption, image)

    def add_enemies(self, group):
        pass


class Endboss(Spaceships):
    def __init__(self, x, y):
        image = "endboss_final3.png"
        speed = 1
        lives = 500
        shoot_count = 2000
        cooldown = 3000
        speed_y = 1
        image_size_x = 450
        image_size_y = 450
        super().__init__(image, speed, lives, shoot_count, x, y, cooldown, 4, speed_y, image_size_x, image_size_y)
        self.get_aliens = True

    def draw(self, surface, print_counter):
        super().draw(surface, print_counter)
        if self.lives != 0:
            self.draw_health_bar(surface)

    def move_x(self, speed):
        self.rect.x = min(max(self.rect.x, -100), 601)
        self.rect.x += self.speed

    def move_y(self, speed):
        self.rect.y = min(max(self.rect.y, -500), -100)
        self.rect.y += self.speed_y

    def move(self, func, spaceship, surface, explosion_group, group):
        self.move_y(self.speed_y)
        if len(group) == 1 and self.rect.y > -109:
            self.move_x(self.speed)
            if self.rect.x >= 550:
                self.speed = -self.speed
            if self.rect.x <= -100:
                self.speed = 1
        elif len(group) < 1:
            self.move_x(self.speed)
            self.speed_y = -1
            if self.rect.x > 300:
                self.speed = 0

    def draw_health_bar(self, surface):
        red = (255, 0, 0)
        green = (0, 255, 0)
        pygame.draw.rect(surface, red, (self.rect.x + 125, self.rect.centery, 200, 10))
        pygame.draw.rect(surface, green, (self.rect.x + 125, self.rect.centery, int(200 * (self.lives / 500)), 10))

    def check_collision(self, h_group, game_score, spaceship, explosion_group, enemy_bullet_group, group):
        self.check_live(group, explosion_group)
        for bullet in enemy_bullet_group:
            explosion_small = Explosion(bullet.rect.centerx, bullet.rect.centery, 1)
            if pygame.sprite.collide_mask(self, bullet):
                explosion_group.add(explosion_small)
                bullet.kill()
                game_score += 1
                self.lives -= 1
        explosion_normal_size = Explosion(spaceship.rect.centerx, spaceship.rect.centery, 2)
        if pygame.sprite.collide_mask(self, spaceship):
            if not spaceship.shield_bool and len(h_group) > 0:
                h_group.sprites()[-1].kill()
                spaceship.lives -= 1
                explosion_group.add(explosion_normal_size)
        return game_score

    def check_live(self, group, explosion_group):
        explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
        live_check_list = [450, 400, 350, 300, 250, 200, 150, 100, 50]
        for live in live_check_list:
            if self.lives == live and self.get_aliens:
                for enemy in range(2):
                    group.add(TieFighterLeft(-100, 0 + enemy * 200))
                for enemy in range(2):
                    group.add(TieFighterRight(900, 50 + enemy * 200))
                self.get_aliens = False
            if self.lives == live + 1:
                self.get_aliens = True
        if self.lives == 0:
            explosion_group.add(explosion)
            self.kill()


class TieFighter(Spaceships):
    def __init__(self, x, y, speed, list, plus_angle, direction, bullet_angle):
        self.index = 0
        lives = 2
        shoot_count = 800
        self.list = list
        image = list[self.index]
        cooldown = 800
        speed_y = 1
        super().__init__(image, speed, lives, shoot_count, x, y, cooldown, direction, speed_y)
        self.plus_angle = plus_angle
        self.counter = 0
        self.angle = 0
        self.bullet_angle = bullet_angle

    def update_rotation(self):
        rotate_speed = 6  # wird für die länge des anzeigens eines Bildes verwendet
        self.counter += 1
        self.angle += self.plus_angle
        if self.counter >= rotate_speed and self.index < len(self.list) - 1:
            self.counter = 0
            self.index += 1
            self.image = pygame.image.load(self.list[self.index])
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.image = pygame.transform.rotate(self.image, self.angle)

    def move(self, func, spaceship, surface, explosion_group, group):
        self.rect.x += self.speed
        self.rect.y += self.speed_y
        if 350 < self.rect.x <= 368:
            self.update_rotation()
            self.speed_y = - self.speed_y
        if not 1000 >= self.rect.x > -200:
            self.kill()

    def shoot(self, current_time, h_group, bullet_group):
        if current_time - self.last_shot > self.shoot_count:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, "death_star_laser1.png", math.pi / self.direction, 10,
                            self.bullet_angle)
            bullet_group.add(bullet)
            if current_time - self.last_shot > self.cooldown:
                self.last_shot = current_time


class TieFighterRight(TieFighter):
    def __init__(self, x, y):
        list = [f'tie_r/tie{1}.png',
                f'tie_r/tie{2}.png',
                f'tie_r/tie{3}.png',
                f'tie_r/tie{4}.png']
        speed = -2
        plus_angle = -4
        direction = -0.9
        bullet_angle = 110
        super().__init__(x, y, speed, list, plus_angle, direction, bullet_angle)


class TieFighterLeft(TieFighter):
    def __init__(self, x, y):
        list = [f'tie_l/tie{1}.png',
                f'tie_l/tie{2}.png',
                f'tie_l/tie{3}.png',
                f'tie_l/tie{4}.png']
        speed = 2
        plus_angle = 4
        direction = 4
        bullet_angle = 50
        super().__init__(x, y, speed, list, plus_angle, direction, bullet_angle)
