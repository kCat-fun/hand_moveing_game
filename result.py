import pygame

class Result:
    def __init__(self, score, high_score):
        self.score = score
        self.high_score = high_score

        # フォントを設定する
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.antialias = True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render("Score      : " + str(self.score), True, (255, 255, 255))
        text2 = self.font.render("Hight Score: " + str(self.high_score), True, (255, 255, 255))
        screen.blit(text1, (250, 350))
        screen.blit(text2, (250, 450))
