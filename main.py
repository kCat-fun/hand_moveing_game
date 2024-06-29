import pygame
from pygame.locals import *
from hand_tracking import *
from game import *

SCREEN_WIDTH: int = 650
SCREEN_HEIGHT: int = 850

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.init()

    hand_tracking: HandTracking = HandTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
    game: Game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, hand_tracking)

    # フォントを使いタイトルテキストを作る
    run = True
    while run:
        hand_tracking.update()
        game.set_screen(screen)
        game.set_hands(hand_tracking)
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    hand_tracking.finish()

if __name__ == "__main__":
    main()