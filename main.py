import pygame
from pygame.locals import *
from hand_tracking import *
from game import *
from result import *

SCREEN_WIDTH: int = 650
SCREEN_HEIGHT: int = 850

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.init()

    hand_tracking: HandTracking = HandTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
    game: Game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, hand_tracking)
    result = None

    # フォントを使いタイトルテキストを作る
    run = True

    scene_num: int = 0
    f = open('high_score.txt', 'r')
    datalist = f.readlines()
    f.close()
    high_score = int(datalist[0])
    print(high_score)

    while run:
        hand_tracking.update()
        
        match scene_num:
            case 0:
                game.set_screen(screen)
                game.set_hands(hand_tracking)
                game.draw()
                if game.is_over():
                    new_record_flag = False
                    if high_score < game.score:
                        with open('high_score.txt', mode='w') as f:
                            f.write(str(game.score))
                            high_score = game.score
                            new_record_flag = True

                    result = Result(game.score, high_score, new_record_flag)
                    scene_num = 1
            case 1:
                result.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    hand_tracking.finish()

if __name__ == "__main__":
    main()