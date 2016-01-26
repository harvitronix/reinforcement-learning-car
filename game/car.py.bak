import pygame
import math
import random
xs = 600
ys = 450
xt = xs - 100
yt = ys + 100
dt = 1.0
font = pygame.font.Font(None,24)
msg = []
msg += ["STOP"]
msg += ["GEAR 1"]
msg += ["GEAR 2"]
msg += ["GEAR 3"]
msg += ["GEAR 4"]
n = len(msg)
gears = []
for i in range(n):
    gears += [font.render(msg[i],1,(250,250,250))]
speedo = []
laps = []
for i in range(101):
    speedo += [font.render("SPEED "+str(i),1,(250,250,250))]
    laps += [font.render("LAP "+str(i),1,(250,250,250))]
pygame.mixer.init()
sound = pygame.mixer.Sound("sound/racing_car.wav")
sound.set_volume(.5)
sound.play(loops=-1)
shiftup_sound = pygame.mixer.Sound("sound/shift_up.wav")
idle_sound = pygame.mixer.Sound("sound/idle_rev.wav")
idle_sound.set_volume(0)
idle_sound.play(loops=-1)
                                
class Sprite():
    def Load(self,path,NF):
        self.view = 270
        self.images = []
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
            name = path+'/fr_'
            if nv == 1:
                name += '000'
            if nv == 2:
                name += '00'
            if nv == 3:
                name += '0'
            self.images += [pygame.image.load(name+str(f+1)+'.png')]
    def Draw(self,x,y,screen):
        view = self.view + int(random.gauss(0,self.wobble))
#        print 'wobble = ',self.wobble
        if view < 0 :
            view = view + 360
        view = view%360
        screen.blit(self.images[view],(x-32,y-32))
        screen.blit(gears[self.gear],(xt,yt))
        indicated = int(10.0*self.speed)
        screen.blit(speedo[indicated],(xt+100,yt))
        screen.blit(laps[self.lap],(xt,yt+50))
        if self.lap > MAX_LAPS :
            elapsed_time = font.render(str(frames/24),1,(250,250,250))
            screen.blit(elapsed_time,(xt+100,yt+50))
#        self.view = (self.view+2)%360
    def Update(self):
        self.speed = .95*self.speed + .05*(2.5*self.gear)
        print self.gear,'\t',int(10.0*self.speed),'\t',self.lap
        
        theta = self.view/57.296
        if self.wobble :
            idle_sound.set_volume(1.)
        else :
            idle_sound.set_volume(0)
        vx = self.speed*math.sin(theta)
        vy = -self.speed*math.cos(theta)
        self.xf = self.xf + vx*dt
        self.yf = self.yf + vy*dt
        self.xc = int(self.xf)
        self.yc = int(self.yf)
        sound.set_volume(self.speed/10)
    def Shift_Up(self):
        shiftup_sound.play()
        
        
