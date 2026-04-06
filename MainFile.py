import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Fsh Tank")
Game_Screen = pygame.display.set_mode((800, 800))
Sand_Img = pygame.image.load("Sand.png").convert_alpha()
Chest_Img_Open = pygame.image.load("Chest_Open.png").convert_alpha()
Chest_Img_Closed = pygame.image.load("Chest_Closed.png").convert_alpha()
SandBob = pygame.image.load("SandBob.png").convert_alpha()
PatRick = pygame.image.load("PatRick.png").convert_alpha()
Chest_Open = 0
Font = pygame.font.SysFont(None, 20)

class Fish:
    def __init__(self):
        
        if random.randint(0, 100) == 0:   self.Shiny = True
        else:   self.Shiny = False
        if self.Shiny == False:   self.Image = pygame.image.load("Blue Fish.png").convert_alpha()
        else:   self.Image = pygame.image.load("Shiny Blue Fish.png").convert_alpha()

        self.FlipedImage = pygame.transform.flip(self.Image, True, False)
        self.DeadImage = pygame.transform.flip(self.Image, False, True)
        self.FlipedDeadImage = pygame.transform.flip(self.Image, True, True)
        pygame.Surface.set_colorkey(self.Image, [255, 0, 255])
        self.FlipImg = False
        self.X_Pos = random.randint(0, 750)
        self.Y_Pos = random.randint(200, 780)
        self.Height = self.Image.get_height()
        self.Width = self.Image.get_width()
        self.Speed = 1
        self.X_Direct = random.randint(-1, 1)
        self.Y_Direct = random.randint(-1, 1)
        self.Moveing = True
        self.Time_Alive = 0
        self.Life_Time = random.randint(600, 1200)
        self.Death_Timer = 0
        self.Max_Hunger = random.randint(400, 1000)
        if self.Shiny == True:
            self.Life_Time *= 2
            self.Max_Hunger *= 2
        self.Hunger = self.Max_Hunger // 2
        self.Alive = True
        self.Hovered_Over = 0
    
    def Time_Updates(self):
        self.Time_Alive += 1
        if self.Alive == True:
            if self.Time_Alive % 40 == 0:
                Bubble_Creation(self.X_Pos + self.Width, self.Y_Pos)
            if self.Time_Alive % 120 == 0:
                self.X_Direct = random.randint(-1, 1)
                self.Y_Direct = random.randint(-1, 1)
            if (self.X_Direct or self.Y_Direct) != 0 and self.Time_Alive % 4 == 0:
                self.Hunger -= self.Speed
        
        if self.X_Direct == 1:
            self.FlipImg = False
        elif self.X_Direct == -1:
            self.FlipImg = True
        if self.Alive == False:
            self.Death_Timer += 1
        if self.Time_Alive >= self.Life_Time:
            self.Alive = False
        if self.Hunger < 0:
            self.Alive = False
        if self.Hovered_Over > 0:
            self.Hovered_Over -= 1

    def Move(self):
        if self.Alive == True:
            self.X_Pos += self.X_Direct
            self.Y_Pos += self.Y_Direct
            
            if 0 >= self.X_Pos:
                self.X_Direct = 1
            elif self.X_Pos >= 790:
                self.X_Direct = -1

            if 20 >= self.Y_Pos:
                self.Y_Direct *= 1
            elif self.Y_Pos + self.Height >= 800:
                self.Y_Direct = -1

    def Mouse_Interact(self):
        if ((self.X_Pos) < Mouse_X < (self.X_Pos + self.Width)) and ((self.Y_Pos) < Mouse_Y < (self.Y_Pos + self.Height)):
            self.Hovered_Over = 20

    def Stat_Sheet(self):
        if self.Hovered_Over > 0:
            self.Fish_Stats = {0: Font.render(f"Time left to live: {self.Life_Time - self.Time_Alive}", True, (200, 200, 200)),
                          1: Font.render(f"Hunger level: {self.Hunger }/{self.Max_Hunger}", True, (200, 200, 200))}
            pygame.draw.rect(Game_Screen, (40, 40, 40), (330, 15, 150, 45))
            for Key, Value in self.Fish_Stats.items():
                Game_Screen.blit(Value, (340, 20 + 20*Key))

    def Draw(self):
        if self.Alive == True:
            if self.FlipImg == False:
                Game_Screen.blit(self.Image, (self.X_Pos, self.Y_Pos))
            else:
                Game_Screen.blit(self.FlipedImage, (self.X_Pos, self.Y_Pos))
        else:
            if self.FlipImg == False:
                Game_Screen.blit(self.DeadImage, (self.X_Pos, self.Y_Pos))
            else:
                Game_Screen.blit(self.FlipedDeadImage, (self.X_Pos, self.Y_Pos))

School =[]

for _ in range(10):
    School.append(Fish())

class Bubble:
    def __init__(self, X, Y, Y_End):
        self.Y_Pos = Y
        self.X_Pos = X
        self.Y_End = Y - Y_End
        self.Radius = random.randrange(2, 10)
        self.Speed = self.Radius//2
    def Move_Draw(self):
        self.Y_Pos -= self.Speed
        pygame.draw.circle(Game_Screen, (140, 140, 250), (self.X_Pos, self.Y_Pos), self.Radius)

Bubbles = []

def Bubble_Creation(X, Y, Y_End = 100):
    Bubbles.append(Bubble(X, Y, Y_End))

def Bubble_Up_Keep():
    for _ in range(len(Bubbles)):
        Bubbles[_].Move_Draw()

def Bubble_Destruction():
    for _ in range(len(Bubbles)):
        if Bubbles[_].Y_End > Bubbles[_].Y_Pos:
            Bubbles.pop(_)
            break

class seaweed:
    def __init__(self,X, Y):
        self.X_Pos_List = [X for _ in range(3)]
        self.Y_Pos_List = [Y - (_ * 10) for _ in range(3)]
        self.X_Max_Right = X + 10
        self.X_Max_Left = X - 10
        self.Height = 100
        self.Width = 8
        self.Color = (0,100,0)
        self.Direction_List = [_ for _ in range(3)]
       
    def Update(self):
        for _ in range(3):
            if self.X_Pos_List[_] > self.X_Max_Right:
                self.Direction_List[_] *= -1
            elif self.X_Pos_List[_] < self.X_Max_Left:
                self.Direction_List[_] *= -1

            self.X_Pos_List[_] += self.Direction_List[_] / 2
       
    def Draw(self):
        for _ in range(len(self.X_Pos_List)):
            pygame.draw.rect(Game_Screen, self.Color, (self.X_Pos_List[_], self.Y_Pos_List[_], 10, 10))
        pygame.draw.rect(Game_Screen, self.Color, (self.X_Pos_List[1], self.Y_Pos_List[1], 10, 10))
        pygame.draw.rect(Game_Screen, self.Color, (self.X_Pos_List[2], self.Y_Pos_List[2], 10, 10))

Seaweed = [seaweed(random.randrange(10, 790), random.randrange(620, 760)) for _ in range(3)]


Mouse_X, Mouse_Y = 0, 0
Clock = pygame.time.Clock()
Ticker = 0
Running = True
while Running == True:
    Clock.tick(60)
    Ticker += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.MOUSEMOTION:
            Mouse_X, Mouse_Y = pygame.mouse.get_pos()
            if Ticker % 10 == 0:
                Bubble_Creation(Mouse_X, Mouse_Y)
            for _ in range(len(School)):
                School[_].Mouse_Interact()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (700 >= Mouse_X >= 640) and (780 >= Mouse_Y >= 720):
                Chest_Open = 30
    
    for _ in range(len(School)):
        School[_].Time_Updates()
        School[_].Move()

    for _ in range(len(School)):
        if School[_].Alive == False and School[_].Death_Timer >= 60:
            School.pop(_)
            break
    if Ticker % 20 == 0:
        Bubble_Creation(random.randrange(0, 800), 820, 820)
    Bubble_Destruction()
    Game_Screen.fill((40, 40, 200))
    Game_Screen.blit(Sand_Img, (0, 660))
    
    if Chest_Open > 0:
        Game_Screen.blit(Chest_Img_Open, (600, 640))
        Chest_Open -= 1
    else:
        Game_Screen.blit(Chest_Img_Closed, (600, 640))

    Game_Screen.blit(PatRick, (50, 620))
    Game_Screen.blit(SandBob, (250, 720))

    for _ in Seaweed:
        _.Update()
        _.Draw()

    Bubble_Up_Keep()

    for _ in range(len(School)):
        School[_].Draw()
        School[_].Stat_Sheet()

    pygame.display.flip()

pygame.quit()
