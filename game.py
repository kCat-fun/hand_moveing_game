import pygame
from bullet import *

class Game:
    def __init__(self, screen, width, height, hand_tracking):
        self.screen = screen
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        # フォントを設定する
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.antialias = True

        self.hand_tracking = hand_tracking
        self.bullets = []

        self.right_hand_rock_flag = False
        self.left_hand_rock_flag = False

    def draw(self):
        self.screen.fill((0, 0, 0))

        hands_pos = self.hand_tracking.get_hand_pos()
        is_hands_rock = self.hand_tracking.is_rock()
        print(hands_pos, is_hands_rock)

        self.draw_hands_pos(hands_pos, is_hands_rock)

        if(is_hands_rock["left"]):
            if (not hands_pos["left"] == None) and (not self.left_hand_rock_flag):
                pos = self.convert_pos_hand_screen(hands_pos["left"]["x"], hands_pos["left"]["y"])
                self.bullets.append(Bullet(pos["x"], pos["y"],0, -30))
                self.left_hand_rock_flag = True
        else:
            self.left_hand_rock_flag = False
        
        if(is_hands_rock["right"]):
            if (not hands_pos["right"] == None) and (not self.right_hand_rock_flag):
                pos = self.convert_pos_hand_screen(hands_pos["right"]["x"], hands_pos["right"]["y"])
                self.bullets.append(Bullet(pos["x"], pos["y"],0, -30))
                self.right_hand_rock_flag = True
        else:
            self.right_hand_rock_flag = False

        if(0 < len(self.bullets)):
            counter: int = 0
            for bullet in self.bullets:
                bullet.update()
                bullet.draw(self.screen)
                if bullet.remove_flag:
                    self.bullets.pop(counter)
                    counter -= 1
                counter += 1

        text = self.font.render("bullets: " + str(len(self.bullets)), True, (255, 255, 255))
        self.screen.blit(text, (10,10))



    def set_hands(self, hand_tracking):
        self.hand_tracking = hand_tracking

    def set_screen(self, screen):
        self.screen = screen

    def draw_hands_pos(self, hands_pos, is_hands_rock):
        left_hand_pos = hands_pos["left"]
        right_hand_pos = hands_pos["right"]

        if not left_hand_pos == None:
            pos = self.convert_pos_hand_screen(left_hand_pos["x"], left_hand_pos["y"])
            pygame.draw.circle(
                self.screen,
                (200, 255, 255) if is_hands_rock["left"] else (100, 150, 150),
                (pos["x"], pos["y"]),
                30,
            )

        if not right_hand_pos == None:
            pos = self.convert_pos_hand_screen(right_hand_pos["x"], right_hand_pos["y"])
            pygame.draw.circle(
                self.screen,
                (255, 200, 255) if is_hands_rock["right"] else (150, 100, 150),
                (pos["x"], pos["y"]),
                30,
            )

    def convert_pos_hand_screen(self, x, y):
        return {"x": (x/100.0)*self.SCREEN_WIDTH, "y": (y/100.0)*self.SCREEN_HEIGHT}