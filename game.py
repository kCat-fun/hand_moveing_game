import math
import pygame
import random
from bullet import *
from enemy import *
class Game:
    def __init__(self, screen, width, height, hand_tracking):
        self.frame_count = 0

        self.screen = screen
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        # フォントを設定する
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.antialias = True

        self.hand_tracking = hand_tracking
        self.bullets = []
        self.enemies = []
        self.create_enemies_flag = False
        self.player_radius = 30

        self.right_hand_rock_flag = False
        self.left_hand_rock_flag = False

        self.score = 0

    def draw(self):
        self.screen.fill((0, 0, 0))

        hands_pos = self.hand_tracking.get_hand_pos()
        is_hands_rock = self.hand_tracking.is_rock()
        # print(hands_pos, is_hands_rock)

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

        self.draw_hands_pos(hands_pos, is_hands_rock)

        if self.frame_count % (80 - min(round(self.frame_count/30.0), 60)) > 10 and (not self.create_enemies_flag):
            random_number = (random.random() * 0.8) + 0.1
            self.enemies.append(Enemy(random_number*self.SCREEN_WIDTH, 0, 0, 10))
            self.create_enemies_flag = True
        elif self.frame_count % (80 - min(round(self.frame_count/30.0), 60)) < 10:
            self.create_enemies_flag = False

        if(0 < len(self.bullets)):
            counter: int = 0
            for bullet in self.bullets:
                bullet.update()
                bullet.draw(self.screen)
                if bullet.remove_flag:
                    self.bullets.pop(counter)
                    counter -= 1
                counter += 1
        
        if(0 < len(self.enemies)):
            counter1: int = 0
            for enemy in self.enemies:
                enemy.update()
                enemy.draw(self.screen)

                counter2: int = 0
                for bullet in self.bullets:
                    if (
                        self.is_overlap(
                            {"x": bullet.pos.x, "y": bullet.pos.y}, bullet.radius, 
                            {"x": enemy.pos.x, "y": enemy.pos.y}, enemy.radius
                        )
                    ):
                        self.score += 1
                        self.enemies.pop(counter1)
                        self.bullets.pop(counter2)
                        counter1 -= 1
                        counter2 -= 1
                    counter2 += 1
                counter1 += 1

        text1 = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        text2 = self.font.render("frameCount: " + str(self.frame_count), True, (255, 255, 255))
        self.screen.blit(text1, (10,10))
        self.screen.blit(text2, (420,10))

        self.frame_count += 1

    def is_over(self):
        hands_pos = self.hand_tracking.get_hand_pos()
        
        _left_hand_pos = hands_pos["left"]
        if _left_hand_pos == None:
            left_hand_pos = {"x": -1, "y": -1}
        else:
            left_hand_pos = self.convert_pos_hand_screen(_left_hand_pos["x"], _left_hand_pos["y"])
        
        _right_hand_pos = hands_pos["right"]
        if _right_hand_pos == None:
            right_hand_pos = {"x": -1, "y": -1}
        else:
            right_hand_pos = self.convert_pos_hand_screen(_right_hand_pos["x"], _right_hand_pos["y"])
        for enemy in self.enemies:
            if (
                    self.is_overlap(left_hand_pos, self.player_radius, {"x": enemy.pos.x, "y": enemy.pos.y}, enemy.radius) or\
                    self.is_overlap(right_hand_pos, self.player_radius, {"x": enemy.pos.x, "y": enemy.pos.y}, enemy.radius) or\
                    enemy.pos.y - enemy.radius/2.0 > self.SCREEN_HEIGHT\
            ):
                    return True
        return False

    def is_overlap(self, pos1, radius1, pos2, radius2):
        return self.check_collision(pos1["x"], pos1["y"], radius1, pos2["x"], pos2["y"], radius2)

    def check_collision(self, x1, y1, r1, x2, y2, r2):
            # 二つの円の中心の距離を計算
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # 中心の距離が二つの円の半径の和以下であれば衝突している
        if distance <= r1 + r2:
            return True
        else:
            return False

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
                self.player_radius,
            )

        if not right_hand_pos == None:
            pos = self.convert_pos_hand_screen(right_hand_pos["x"], right_hand_pos["y"])
            pygame.draw.circle(
                self.screen,
                (255, 200, 255) if is_hands_rock["right"] else (150, 100, 150),
                (pos["x"], pos["y"]),
                self.player_radius,
            )

    def convert_pos_hand_screen(self, x, y):
        return {"x": (x/100.0)*self.SCREEN_WIDTH, "y": (y/100.0)*self.SCREEN_HEIGHT}