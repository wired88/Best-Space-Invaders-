import math
import random

import pygame
from pygame import mixer


class Window(pygame.sprite.Sprite):
    def __init__(self, caption, image, window_open):
        super().__init__()
        self.width = 800
        self.height = 600
        self.change_y_screen_image = 0
        self.caption = caption
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.window_open = window_open

        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.group = pygame.sprite.Group()
        self.back_button = BackButton()
        self.spaceship_group = pygame.sprite.Group()

        self.xwing = XWing()
        self.tiefighter = TFighterBG()

        self.spaceship_group.add(self.xwing)
        self.spaceship_group.add(self.tiefighter)

    def print_headline(self, pos):
        orange = (255, 165, 0)
        menu_font = pygame.font.Font("Starjedi.ttf", 55)
        menu_font = menu_font.render(self.caption, True, orange)
        self.screen.blit(menu_font, pos)

    def draw(self, m_pos):
        self.screen.blit(self.image, (0, 0))
        for sprite in self.group.sprites():
            sprite.draw(m_pos, self.screen)
        self.group.draw(self.screen)
        self.spaceship_group.draw(self.screen)

    def update(self, m_pos, current_time, lvl_window, hs_window, menu_window, game_window, level_three_window, setting_window):
        for sprite in self.spaceship_group.sprites():
            sprite.update(current_time)
        self.back_button.update(m_pos, menu_window, game_window, level_three_window)
        if self.back_button.action:
            menu_window.window_open = True
            self.window_open = False
            self.back_button.action = False

    def change_screen_boolians(self, clicked_window, clicked_button):
        clicked_window.window_open = True
        clicked_button.action = False
        return False
class BackGroundSpaceships(pygame.sprite.Sprite):
    def __init__(self, x, y, image, spaceship_size_x, spaceship_size_y, flight_count, speedx, speedy):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.spaceship_size_x = spaceship_size_x
        self.spaceship_size_y = spaceship_size_y
        self.image = pygame.transform.scale(self.image, (spaceship_size_x, spaceship_size_y))
        self.rect = self.image.get_rect(center=[self.x, self.y])
        self.last_count = pygame.time.get_ticks()
        self.flight_count = flight_count
        self.speedx = speedx
        self.speedy = speedy

    def move(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def update(self, current_time):
        if current_time - self.last_count > self.flight_count and self.rect.x <= 1000:
            self.move()
        if self.rect.x <= -200:
            self.last_count = current_time
            self.rect.x = 950

    def draw(self, m_pos, surface):
        pass


class TFighterBG(BackGroundSpaceships):
    def __init__(self):
        x = 1000
        y = 200
        image = "t_fighter_menu.png"
        spaceship_size_x = 64
        spaceship_size_y = 64
        flight_count = 6000
        speedx = -5
        speedy = 2
        super().__init__(x, y, image, spaceship_size_x, spaceship_size_y, flight_count, speedx, speedy)




















class XWing(BackGroundSpaceships):
    def __init__(self):
        x = 600
        y = 800
        image = "battleship.png"
        spaceship_size_x = 64
        spaceship_size_y = 64
        flight_count = 3000
        speedx = -2
        speedy = -5
        super().__init__(x, y, image, spaceship_size_x, spaceship_size_y, flight_count, speedx, speedy)
        self.image = pygame.transform.rotate(self.image, 15)


class Buttons(pygame.sprite.Sprite):
    def __init__(self, x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey, text, plus_vecx, plus_vecy):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (extra_image_sizex, extra_image_sizey))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.bg_image = pygame.image.load(bg_image)
        self.bg_image = pygame.transform.scale(self.bg_image, (bgimage_sizex, bgimage_sizey))
        self.star_wars_color = (255, 165, 1)
        self.clicked = False
        self.action = False
        self.text = text
        self.plus_vecx = plus_vecx
        self.plus_vecy = plus_vecy

    def draw(self, m_pos, surface):
        if self.rect.collidepoint(m_pos):
            surface.blit(self.bg_image, (self.rect.x + self.plus_vecx, self.rect.y + self.plus_vecy))

    def update(self, m_pos, menu_window, game_window, level_three_window, empty_groups=None,
               group_l=None, explosion_group=None, extra_posx=0, extra_posy=0):
        sound = mixer.Sound('sounds/button_click_ogg.ogg')
        if self.rect.collidepoint(m_pos) and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            sound.play()
            self.clicked = True
            self.action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.action

    def draw_text(self, surface, size, x, y, text):
        grey = (105, 105, 105)
        font = pygame.font.Font("Starjedi.ttf", size)
        text = font.render(str(text), True, grey)
        surface.blit(text, (x, y))


########################################################################################################################
# Game Mother Classes
class StaticObjects(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.show_shield = False

    def update(self, player):
        pass

    def check_click(self):
        pass

    def draw(self, current_time, player, print_counter, surface):
        pass


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_powerup = pygame.time.get_ticks()

    def check_collision(self, player, heart_g):
        if self.rect.colliderect(player.rect):
            self.apply(player, heart_g)
            self.kill()

    def apply(self, player, heart_gr):
        pass

    def move(self):
        self.rect.y += self.speed
        if self.rect.y >= 600:
            self.kill()

    def update(self, player, heart_g, current_time, powerup_group):
        self.move()
        self.check_collision(player, heart_g)





class Spaceships(pygame.sprite.Sprite):
    def __init__(self, image, speed, lives, shoot_count, x, y, cooldown, direction, sound, speed_y, image_size_x=64, image_size_y=64):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.speed_y = speed_y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (image_size_x, image_size_y))
        self.rect = self.image.get_rect(center=[x, y])
        self.lives = lives
        self.last_shot = pygame.time.get_ticks()
        self.shoot_count = shoot_count
        self.cooldown = cooldown
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction
        self.sound = sound
        self.lives_index = 0

    def draw(self, surface, print_counter):
        pass

    def shoot(self, current_time, h_group, bullet_group, volume):
        if current_time - self.last_shot > self.shoot_count and len(h_group) > 0:
            shooting_sound = mixer.Sound(f'sounds/{self.sound}')
            shooting_sound.play()
            shooting_sound.set_volume(volume)
            bullet = Bullet(self.rect.centerx, self.rect.bottom, "death_star_laser1.png", math.pi/2, 10, 0)
            bullet_group.add(bullet)
            if current_time - self.last_shot > self.cooldown:
                self.last_shot = current_time

    def move_y(self, speed):
        self.rect.y = min(max(self.rect.y, 0), 536)
        self.rect.y += speed

    def move_x(self, speed):
        self.rect.x = min(max(self.rect.x, 0), 736)
        self.rect.x += speed

    def move(self, func, spaceship, surface, explosion_group, group):
        self.move_x(self.speed)
        if self.rect.x >= 736 or self.rect.x <= 0:
            self.speed = -self.speed
            self.rect.y += self.speed_y
        if self.rect.y >= 600:
            func()
            spaceship.dead = True

    def update(self, surface, volume, current_time, func, h_group, game_score, explosion_group, group, bullet_group, enemy_bullet_group, spaceship):
        game_score = self.check_collision(h_group, game_score, spaceship, explosion_group, enemy_bullet_group, group)
        self.shoot(current_time, h_group, bullet_group, volume)
        self.move(func, spaceship, surface, explosion_group, group)
        return game_score

    def check_collision(self, h_group, game_score, player, explosion_group, enemy_bullet_group, group):
        game_score = game_score
        explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
        if pygame.sprite.collide_mask(self, player):
            explosion_group.add(explosion)
            if not player.shield_bool and len(h_group) > 0:
                h_group.sprites()[-1].kill()
                player.lives -= 1
            self.kill()
        for bullet in enemy_bullet_group.sprites():
            if pygame.sprite.collide_mask(self, bullet):
                self.lives_index += 1
                explosion_small = Explosion(bullet.rect.centerx, bullet.rect.centery, 1)
                explosion_group.add(explosion_small)
                bullet.kill()
                game_score += 1
                self.lives -= 1
                if self.lives == 0:
                    self.check_live()
        return game_score

    def check_live(self):
        self.rect.x = random.randint(0, 736)
        self.rect.y = random.randint(-130, -60)
        self.lives += self.lives_index
        self.lives_index = 0


class BackButton(Buttons):
    def __init__(self):
        x = 40
        y = 40
        image = "previous.png"
        extra_image_sizex = 32
        extra_image_sizey = 32
        bg_image = "previou_green.png"
        bgimage_sizex = 32
        bgimage_sizey = 32
        text = ''
        plus_vecx = 0
        plus_vecy = 0
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)


class Bullet(pygame.sprite.Sprite):  # 13
    def __init__(self, x, y, image, direction, speed=-10, angle=60):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle
        self.direction = direction
        self.image = pygame.transform.rotate(self.image, self.angle)

    def update(self):  # 14
        new_x = self.rect.x + (self.speed * math.cos(self.direction))
        new_y = self.rect.y + (self.speed * math.sin(self.direction))
        self.rect.x = new_x
        self.rect.y = new_y
        if self.rect.bottom < 0 or self.rect.bottom > 800 or self.rect.x > 800 or self.rect.x < -30:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.images = []
        for i in range(1, 6):
            self.img = pygame.image.load(f"exp/exp{i}.png")
            if size == 1:
                self.img = pygame.transform.scale(self.img, (50, 50))  # alle Bilder auf die gleihe Größe skallieren
            elif size == 2:
                self.img = pygame.transform.scale(self.img, (100, 100))
            elif size == 3:
                self.img = pygame.transform.scale(self.img, (1000, 1000))
            self.images.append(self.img)
        self.index = 0  # zeigt das momentane Bild
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        self.sound = ''

    def update(self):
        explosion_speed = 4  # wird für die länge des anzeigens eines Bildes verwendet
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

