import pygame

from GameClasses import GameWindow
from MenuClasses import MenuWindow, LevelWindow, HighScoreWindow
from Level3 import LevelThreeWindow

# Todo morgen
# - score reaparieren
# - sounds zuende einfügen
# manche vereinzelte aliens sterben nicht
level_window = LevelWindow()
high_score_window = HighScoreWindow()
main_menu_window = MenuWindow()
game_window = GameWindow('Space Invaders', 'vortex.png')
level_three_game_window = LevelThreeWindow('ENDLEVEL', 'blue_nebula.png')

window_group = pygame.sprite.Group()
window_group.add(main_menu_window, high_score_window, level_window, game_window, level_three_game_window)

pygame.init()

clock = pygame.time.Clock()

menu = True
while menu:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    time_now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            menu = False
        elif event.type == pygame.mouse.get_pressed(5):
            menu = False

    for window in window_group.sprites():
        if window.window_open:
            window.draw(mouse_pos)
            window.update(mouse_pos, time_now,
                          level_window,
                          high_score_window,
                          main_menu_window,
                          game_window,
                          level_three_game_window)

    pygame.display.update()

