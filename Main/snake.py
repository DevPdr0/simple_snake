import random

while True:
    try:
        import pygame
        break
    except ModuleNotFoundError:
        import pip
        pip.main(["install", "pygame"])

class SnakeWindow:

    def __init__(self, title: str, size: tuple[int, int], speed: int = 44) -> None:
        self.title, self.size, self.speed = title, size, speed

        # colors
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)

        # body square edge
        self.edge = 16

        # initialize pygame
        pygame.font.init()
        pygame.mixer.init()

        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(size)
        while True: self.run()

    def fill(self, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.screen.fill(color)

    def square(self, color: tuple[int, int, int], pos: tuple[int, int]) -> None:
        pygame.draw.rect(self.screen, color, (pos[0], pos[1], self.edge, self.edge))

    def checkBodyCollision(self) -> bool:
        if len(set(self.pos)) != len(self.pos):
            return True
        return False

    def checkExitWindow(self) -> bool:
        if self.pos[0][0] < 0 or self.pos[0][0] > 368 or self.pos[0][1] < 0 or self.pos[0][1] > 368:
            return True
        return False

    def DRAWsnakeBODY(self, size: list[tuple[int, int]]) -> list[int]:
        for i in size:
            self.square(self.green, i)

        return size

    def genFood(self) -> tuple[int, int]:
        x = random.randint(0, 23) * self.edge
        y = random.randint(0, 23) * self.edge

        for a in self.pos:
            if x == a[0] and y == a[1]:
                return self.genFood()

        return (x, y)

    def handleInput(self, event: pygame.event) -> None:
        if event == pygame.K_RIGHT and self.dirx != -1:
            self.dirx, self.diry = 1, 0
        elif event == pygame.K_LEFT and self.dirx != 1:
            self.dirx, self.diry = -1, 0
        elif event == pygame.K_UP and self.diry != 1:
            self.dirx, self.diry = 0, -1
        elif event == pygame.K_DOWN and self.diry != -1:
            self.dirx, self.diry = 0, 1

    def createHead(self) -> None:
        self.pos.insert(0, (self.pos[0][0] + self.dirx * self.edge, self.pos[0][1] + self.diry * self.edge))
        if self.pos[0] == self.food:
            self.food = self.genFood()
            self.sound("../ost/eat.wav")
            self.points += 16
        else:
            self.pos.pop()

    def update(self, FPS: int = 24) -> None:
        pygame.time.wait(FPS)
        pygame.display.update()

    def snakeInit(self) -> None:
        self.pos = [(32,32)]
        self.food = self.genFood()
        self.dirx, self.diry = 1, 0
        self.goalpha = 0
        self.playSound, self.updateScore = True, True
        self.points = 0

    def iText(self, message: str, pos: tuple[int, int], color: tuple[int, int, int, int] = (255, 255, 255, 255), fontSize: int = 22) -> None:
        font = pygame.font.Font("../font/PressStart.ttf", fontSize)
        textSurface = font.render(message, True, color)
        textSurface.set_alpha(color[3])
        textRect = textSurface.get_rect(center = pos)
        self.screen.blit(textSurface, textRect)

    def game(self):
        # draw head
        self.createHead()

        # draw food
        self.square(self.red, self.food)
        self.DRAWsnakeBODY(self.pos)

    def scoreSHOW(self) -> None:
        pygame.display.set_caption(f"Snake | Score: {self.points}")

    def gameover(self):
        self.score() if self.updateScore else None
        self.updateScore = False
        self.isEnd = True

        self.iText("GAME OVER", (self.size[0] // 2, self.size[1] // 2 - 64), (255, 0, 0, self.goalpha), 33)
        self.iText(f"Score: {self.points}", (self.size[0] // 2, self.size[1] // 2 - 32), (255, 255, 255, self.goalpha))
        self.iText(f"Best: {self.best_value}", (self.size[0] // 2, self.size[1] // 2), (255, 255, 255, self.goalpha))
        self.iText("PRESS SPACE TO RESTART", (self.size[0] // 2, self.size[1] // 2 + 128), (255, 255, 255, self.goalpha), 12)
        self.sound("../ost/gameover.wav") if self.playSound else None

    def score(self) -> None:
        with open("../score/save.txt", "r+") as file:
            self.best_value = int(file.read())

            if self.points > self.best_value:
                self.best_value: int = self.points
                file.seek(0)
                file.write(str(self.best_value))

    def sound(self, path: str) -> None:
        sound = pygame.mixer.Sound(path)
        sound.play()

    def run(self) -> None:
        self.snakeInit()

        self.isEnd = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.isEnd:
                        pygame.mixer.stop()
                        running = False
                        self.isEnd = False

                    self.handleInput(event.key)

            if self.checkBodyCollision() or self.checkExitWindow():
                self.goalpha += 3 if self.goalpha < 255 else 0
                self.gameover()
                self.playSound = False
            else:
                self.scoreSHOW()
                self.game()

            self.update(self.speed)
            self.fill()

SnakeWindow("Snake", (384, 384), 55)