import pygame
import math
import random

pygame.init()

xs = 600
ys = 450
xt = xs - 100
yt = ys + 100
dt = 1.0
font = pygame.font.Font(None, 24)
msg = ["STOP", "GEAR 1", "GEAR 2", "GEAR 3", "GEAR 4"]
n = len(msg)
gears = []
for i in range(n):
    gears += [font.render(msg[i], 1, (250, 250, 250))]
speedo = []
laps = []
for i in range(101):
    speedo += [font.render("SPEED "+str(i), 1, (250, 250, 250))]
    laps += [font.render("LAP "+str(i), 1, (250, 250, 250))]
pygame.mixer.init()


class Sprite():

    speed = 0
    gear = 1
    lap = 0
    view = 270
    xf = 912
    xc = 912
    yc = 1410
    yf = 1410
    images = []
    wobble = 0

    def Load(self, path, NF):
        self.view = 270
        self.NF = NF
        self.xc = 912
        self.yc = 1410
        self.xf = 912.0
        self.yf = 1410.0
        self.speed = 0
        self.gear = 1
        self.wobble = 0
        self.lap = 0
        for f in range(NF):
            nv = len(str(f+1))
            name = './game/' + path + '/fr_'
            if nv == 1:
                name += '000'
            if nv == 2:
                name += '00'
            if nv == 3:
                name += '0'
            self.images += [pygame.image.load(name+str(f+1)+'.png')]
        print("AAAA")
        print(self.images)

    def Draw(self, x, y, screen):
        view = self.view + int(random.gauss(0, self.wobble))

        if view < 0:
            view = view + 360

        view = view % 360
        screen.blit(self.images[view], (x-32, y-32))
        screen.blit(gears[self.gear], (xt, yt))
        indicated = int(10.0 * self.speed)
        screen.blit(speedo[indicated], (xt + 100, yt))
        screen.blit(laps[self.lap], (xt, yt + 50))

    def Update(self):
        self.speed = 0.95 * self.speed + .05 * (2.5 * self.gear)
        print(self.gear, '\t', int(10.0 * self.speed), '\t', self.lap)

        theta = self.view/57.296
        vx = self.speed*math.sin(theta)
        vy = -self.speed*math.cos(theta)
        self.xf = self.xf + vx*dt
        self.yf = self.yf + vy*dt
        self.xc = int(self.xf)
        self.yc = int(self.yf)

        return self.speed
