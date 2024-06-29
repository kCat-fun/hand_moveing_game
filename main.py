import pygame
from pygame.locals import *
from hand_tracking import *

SCREEN_WIDTH: int = 1000
SCREEN_HEIGHT: int = 800

def main():
    hand_tracking: HandTracking = HandTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # フォントを設定する
    font = pygame.font.Font(None, 36)
    color = (255, 255, 255)
    antialias = True
    # フォントを使いタイトルテキストを作る
    run = True
    while run:
        screen.fill((0, 0, 0))

        hand_tracking.update()
        hands_pos = hand_tracking.get_hand_pos()
        is_hands_rock = hand_tracking.is_rock()
        print(hands_pos, is_hands_rock)

        draw_hands_pos(screen, hands_pos, is_hands_rock)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    hand_tracking.finish()

def draw_hands_pos(screen, hands_pos, is_hands_rock):
    left_hand_pos = hands_pos["left"]
    right_hand_pos = hands_pos["right"]

    if not left_hand_pos == None:
        pygame.draw.circle(
            screen,
            (200, 255, 255) if is_hands_rock["left"] else (100, 150, 150),
            ((left_hand_pos["x"]/100.0)*SCREEN_WIDTH, (left_hand_pos["y"]/100.0)*SCREEN_HEIGHT),
            30,
        )

    if not right_hand_pos == None:
        pygame.draw.circle(
            screen,
            (255, 200, 255) if is_hands_rock["right"] else (150, 100, 150),
            ((right_hand_pos["x"]/100.0)*SCREEN_WIDTH, (right_hand_pos["y"]/100.0)*SCREEN_HEIGHT),
            30,
        )


if __name__ == "__main__":
    main()