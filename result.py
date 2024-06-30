import pygame

class Result:
    def __init__(self, score, high_score, new_record_flag):
        self.score = score
        self.high_score = high_score
        self.new_record_flag = new_record_flag

        # フォントを設定する
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.antialias = True

    def draw(self, screen, restart_percent):
        screen.fill((0, 0, 0))
        text1 = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        text2 = self.font.render("Hight Score: " + str(self.high_score), True, (255, 255, 255))
        text4 = self.font.render("Restart To Both Hands Rock: " + str(min(round(restart_percent*100), 100)) + "%", True, (255, 255, 255))
        screen.blit(text1, (200, 350))
        screen.blit(text2, (200, 450))
        screen.blit(text4, (50, 600))
        if self.new_record_flag:
            text3 = self.font.render("NEW RECORD", True, (230, 230, 50))
            screen.blit(text3, (200, 500))
        screen.fill((255,255,255), (48, 648, 554, 54))
        screen.fill((0, 0, 0), (50, 650, 550, 50))
        screen.fill((100,255,100), (50, 650, 550*restart_percent, 50))

