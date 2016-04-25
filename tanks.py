import math
import pygame

class Tank:
    def __init__(self, x = 100, y = 100, vx = 0, vy = 0, a = 500, b = 20):
        """Constructor of Tank class"""
        """self.a - acceleration"""
        """self.b - site of square"""
        self.x, self.y, self.vx, self.vy, self.a, self.b = x, y, vx, vy, a, b

    def update(self, game):
        """Update Player state"""
        if game.pressed[pygame.K_LEFT]:
            self.vx -= game.delta * self.a
            self.vy = 0
        if game.pressed[pygame.K_RIGHT]:
            self.vx += game.delta * self.a
            self.vy = 0
        if game.pressed[pygame.K_UP]:
            self.vy -= game.delta * self.a
            self.vx = 0
        if game.pressed[pygame.K_DOWN]:
            self.vy += game.delta * self.a
            self.vx = 0

        self.vx -= game.delta * self.vx
        self.vy -= game.delta * self.vy

        self.x += self.vx * game.delta
        self.y += self.vy * game.delta

        """Do not let Tank get out of the Game window"""
        if self.x < self.b:
            if self.vx < 0:
                self.vx = 0
            self.x = self.b
        if self.y < self.b:
            if self.vy < 0:
                self.vy = 0
            self.y = self.b
        if self.x > game.width - self.b:
            if self.vx > 0:
                self.vx = 0
            self.x = game.width - self.b
        if self.y > game.height - self.b:
            if self.vy > 0:
                self.vy = 0
            self.y = game.height - self.b

    def render(self, game):
        """Draw Player on the Game window"""
        pygame.draw.rect(game.screen, [150, 75, 0], [self.x - self.b, self.y - self.b, 50, 50], 0)
        if game.pressed[pygame.K_RIGHT] and not game.pressed[pygame.K_DOWN] \
        and not game.pressed[pygame.K_LEFT] and not game.pressed[pygame.K_UP]:
            pygame.draw.rect(game.screen, [150, 100, 0], [self.x + 30, self.y, 20, 10], 0)
        if game.pressed[pygame.K_DOWN] and not game.pressed[pygame.K_UP] \
        and not game.pressed[pygame.K_RIGHT] and not game.pressed[pygame.K_LEFT]:
            pygame.draw.rect(game.screen, [150, 100, 0], [self.x, self.y + 30, 10, 20], 0)
        if game.pressed[pygame.K_LEFT] and not game.pressed[pygame.K_UP] \
        and not game.pressed[pygame.K_RIGHT]:
            pygame.draw.rect(game.screen, [150, 100, 0], [self.x - 40, self.y, 20, 10], 0)
        if game.pressed[pygame.K_UP]:
            pygame.draw.rect(game.screen, [150, 100, 0], [self.x, self.y - 40, 10, 20], 0)


class Bullet:
    def __init__(self, flag = 0, x1 = 100, y1 = 100, vx1 = 0, vy1 = 0):
        self.flag, self.x1, self.y1, self.vx1, self.vy1 = flag, x1, y1, vx1, vy1

    def update(self, game, tank):
        """Update Player state"""
        if game.pressed[pygame.K_SPACE]:
            if game.pressed[pygame.K_LEFT]:
                self.vx1 = -1000
                self.vy1 = 0
            if game.pressed[pygame.K_RIGHT]:
                self.vx1 = 1000
                self.vy1 = 0
            if game.pressed[pygame.K_UP]:
                self.vy1 = -1000
                self.vx1 = 0
            if game.pressed[pygame.K_DOWN]:
                self.vy1 = 1000
                self.vx1 = 0

        self.x1 += self.vx1 * game.delta
        self.y1 += self.vy1 * game.delta

        tank.x += tank.vx * game.delta
        tank.y += tank.vy * game.delta


        """Do not let Bullet get out of the Game window"""
        if self.x1 < -20:
            if self.vx1 < 0:
                self.vx1 = 0
            self.x1 = -20
        if self.y1 < -20:
            if self.vy1 < 0:
                self.vy1 = 0
            self.y1 = -20
        if self.x1 > game.width + 10:
            if self.vx1 > 0:
                self.vx1 = 0
            self.x1 = game.width + 10
        if self.y1 > game.height + 10:
            if self.vy1 > 0:
                self.vy1 = 0
            self.y1 = game.height + 10

    def shot(self, game, tank):
        """Draw bullet on the Game window"""
        if game.pressed[pygame.K_SPACE]:
            self.x1, self.y1 = tank.x, tank.y
            if game.pressed[pygame.K_RIGHT] or game.pressed[pygame.K_LEFT]:
                pygame.draw.ellipse(game.screen, [200, 200, 200],[self.x1, self.y1, 20, 10], 0)
                self.flag = 1
            if game.pressed[pygame.K_UP] or game.pressed[pygame.K_DOWN]:
                pygame.draw.ellipse(game.screen, [200, 200, 200],[self.x1, self.y1, 10, 20], 0)
                self.flag = 0
            if (game.pressed[pygame.K_UP] or game.pressed[pygame.K_DOWN]) and \
                (game.pressed[pygame.K_RIGHT] or game.pressed[pygame.K_LEFT]):
                pygame.draw.ellipse(game.screen, [150, 75, 0],[self.x1, self.y1, 20, 10], 0)
        if self.flag == 1:
            pygame.draw.ellipse(game.screen, [200, 200, 200],[self.x1, self.y1, 20, 10], 0)
        if self.flag == 0:
            pygame.draw.ellipse(game.screen, [200, 200, 200],[self.x1, self.y1, 10, 20], 0)


class Game:
    def tick(self):
        """Return time in seconds since previous call
        and limit speed of the game to 50 fps"""
        self.delta = self.clock.tick(50) / 1000.0

    def __init__(self):
        """Constructor of the Game"""
        self._running = True
        self.size = self.width, self.height = 640, 400
        # create main display - 640x400 window
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        # set window caption
        pygame.display.set_caption('TANKS')
        # get object to help track time
        self.clock = pygame.time.Clock()
        # set default tool
        self.tool = 'run'
        self.player = Tank()
        self.bullet = Bullet()
        self.ar = pygame.PixelArray(self.screen)

    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        elif event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                self.exit()

    def move(self):
        """Here game objects update their positions"""
        self.tick()
        self.pressed = pygame.key.get_pressed()

        self.player.update(self)
        self.bullet.update(self, tank)

    def render(self):
        """Render the scene"""
        self.screen.fill((0, 0, 0))
        self.player.render(self)
        self.bullet.shot(self, tank)
        self.ar[int(self.player.x/10.0),int(self.player.y/10.0)] = (200,200,200)
        pygame.display.flip()

    def exit(self):
        """Exit the game"""
        self._running = False

    def cleanup(self):
        """Cleanup the Game"""
        pygame.quit()

    def execute(self):
        """Execution loop of the game"""
        while(self._running):
            # get all pygame events from queue
            for event in pygame.event.get():
                self.event_handler(event)
            self.move()
            self.render()

        self.cleanup()

if __name__ == "__main__":
    game = Game()
    tank = Tank()
    game.execute()
