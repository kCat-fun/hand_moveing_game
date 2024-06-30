import time
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

    restart_load_time = 0.0

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
                    restart_load_time = time.time()
                    new_record_flag = False
                    if high_score < game.score:
                        with open('high_score.txt', mode='w') as f:
                            f.write(str(game.score))
                            high_score = game.score
                            new_record_flag = True

                    result = Result(game.score, high_score, new_record_flag)
                    scene_num = 1
            case 1:
                is_hands_rock = hand_tracking.is_rock()
                hands_pos = hand_tracking.get_hand_pos()
                if (not (is_hands_rock["left"] and is_hands_rock["right"])) or\
                    (hands_pos["right"] == None or hands_pos["left"] == None):
                    restart_load_time = time.time()
                result.draw(screen, (time.time() - restart_load_time) / 3.0)
                if time.time() - restart_load_time > 3.0:
                    scene_num = 0
                    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, hand_tracking)
                draw_hands_pos(screen, hand_tracking.get_hand_pos(), hand_tracking.is_rock())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                match(scene_num):
                    case 1:
                        if pygame.key.name(event.key) == 'r':
                            scene_num = 0
                            game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, hand_tracking)

        pygame.display.update()

    hand_tracking.finish()

def draw_hands_pos(screen, hands_pos, is_hands_rock):
    def convert_pos_hand_screen(x, y):
        return {"x": (x/100.0)*SCREEN_WIDTH, "y": (y/100.0)*SCREEN_HEIGHT}
    
    left_hand_pos = hands_pos["left"]
    right_hand_pos = hands_pos["right"]

    if not left_hand_pos == None:
        pos = convert_pos_hand_screen(left_hand_pos["x"], left_hand_pos["y"])
        pygame.draw.circle(
            screen,
            (200, 255, 255) if is_hands_rock["left"] else (100, 150, 150),
            (pos["x"], pos["y"]),
            10,
        )

    if not right_hand_pos == None:
        pos = convert_pos_hand_screen(right_hand_pos["x"], right_hand_pos["y"])
        pygame.draw.circle(
            screen,
            (255, 200, 255) if is_hands_rock["right"] else (150, 100, 150),
            (pos["x"], pos["y"]),
            10,
        )

if __name__ == "__main__":
    main()