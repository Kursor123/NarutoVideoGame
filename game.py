import pygame
import random

pygame.init()
clock = pygame.time.Clock()
random.seed()
FONTS = pygame.font.get_fonts()
usedFont = pygame.font.Font(None, 30)

sizeX = 1022
sizeY = 480
score = 0
objects = []
sound = {'hit': pygame.mixer.Sound('sound/hit.wav'),
         'punch': pygame.mixer.Sound('sound/punch.wav')}

win = pygame.display.set_mode((sizeX, sizeY))
pygame.display.set_caption('Naruto Shippuden Video Game')
pygame.mixer.music.load('sound/main_theme.wav')
pygame.mixer.music.play(-1)


class Hero:
    def __init__(self, pictures, x=50, friendly=True):
        self.width = 43
        self.height = 58
        self.x = x
        self.y = sizeY - self.height - 15
        self.isIdle = True
        self.isLeft = False
        self.pictures = pictures
        self.isAttacking = False
        self.isJump = False
        self.jumpCount = 10
        self.animCount = 0
        self.attackCount = 0
        self.attackType = 0
        self.friendly = friendly
        self.hp = 300
        self.isDead = False
        self.deadCount = 0
        # self.underAttack = False
        # self.uaCount = 0
        self.dmg = 10
        self.speed = 8

    def act(self):
        if self.isDead:
            return
        keys = pygame.key.get_pressed()
        if not self.isAttacking:
            if keys[pygame.K_j]:
                self.attackCount = 0
                self.attackType = 0
                self.isAttacking = True
        else:
            if (self.attackCount == 0):
                sound['punch'].play()
            self.attackCount += 1
            if self.attackCount == 4:
                for obj in objects:
                    if obj.friendly != self.friendly and self.collide(obj):
                        obj.damage(self.dmg * (self.attackType + 1))
            if self.attackCount == 8:
                if keys[pygame.K_j]:
                    self.attackType += 1
                    if (self.attackType == 3):
                        self.attackType = 0
                        self.isAttacking = False
                    self.attackCount = 0
                else:
                    self.isAttacking = False
                    self.attackCount = 0
                    self.attackType = 0

        if keys[pygame.K_a] and self.x > 5:
            self.x -= self.speed
            self.isLeft = True
            self.isIdle = False
        elif keys[pygame.K_d] and self.x < sizeX - self.width - 5:
            self.x += self.speed
            self.isLeft = False
            self.isIdle = False
        else:
            self.isIdle = True
        if not self.isJump:
            if keys[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                self.y -= 2 * self.jumpCount
                self.jumpCount -= 1
            else:
                self.jumpCount = 10
                self.isJump = False

    def damage(self, dmg):
        self.hp -= dmg
        sound['hit'].play()
        if self.hp <= 0:
            self.isDead = True

    def collide(self, obj):
        if obj.isDead:
            return

        def isInRect(x, y, obj):
            return obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height

        res = isInRect(self.x, self.y, obj)
        res |= isInRect(self.x + self.width, self.y, obj)
        res |= isInRect(self.x + self.width, self.y + self.height, obj)
        res |= isInRect(self.x, self.y + self.height, obj)
        return res

    def animate(self):
        global win
        pygame.draw.rect(win, (255, 0, 0), (20, 20, 300, 10))
        if not self.isDead:
            pygame.draw.rect(win, (0, 255, 0), (20, 20, self.hp, 10))
        pygame.draw.rect(win, (0, 0, 0), (20, 20, 300, 10), 1)
        if self.isDead:
            win.blit(self.pictures['dead{}'.format('L' if self.isLeft else 'R')]
                     [self.deadCount // 6], (self.x + (self.deadCount // 6) * 25,
                                             self.y + (self.deadCount // 6) * 10))
            if self.deadCount < 29:
                self.deadCount += 1
        elif self.isAttacking:
            win.blit(self.pictures['attack{}'.format('L' if self.isLeft else 'R')]
                     [self.attackType][self.attackCount // 2], (self.x, self.y))
        elif self.isJump:
            win.blit(self.pictures['jump{}'.format('L' if self.isLeft else 'R')]
                     [(self.jumpCount + 10) // 7], (self.x, self.y))
        elif self.isIdle:
            win.blit(self.pictures['idle{}'.format('L' if self.isLeft else 'R')]
                     [self.animCount // 5], (self.x, self.y))
            self.animCount += 1
            self.animCount %= 30
        else:
            win.blit(self.pictures['run{}'.format('L' if self.isLeft else 'R')]
                     [self.animCount // 5], (self.x, self.y))
            self.animCount += 1
            self.animCount %= 30


class Bot:
    def __init__(self, pictures, friendly=False, lvl=1):
        self.width = 43
        self.height = 58 if friendly else 43
        self.x = (sizeX // 2) + (2 * random.randint(0, 1) - 1) * (sizeX // 2 + 50)
        self.y = sizeY - self.height - 15
        self.isIdle = True
        self.isLeft = False
        self.pictures = pictures
        self.isAttacking = False
        self.isJump = False
        self.jumpCount = 10
        self.animCount = 0
        self.attackCount = 0
        self.attackType = 0
        self.friendly = friendly
        self.isTargetChosen = False
        self.hp = 30
        self.isDead = False
        self.underAttack = False
        self.uaCount = 0
        self.dmg = 5
        self.lvl = lvl
        self.speed = 4

    def chooseTarget(self):
        if self.isTargetChosen:
            if self.target.isDead:
                self.isTargetChosen = False
            return
        enemies = []
        for obj in objects:
            if self.friendly != obj.friendly and not obj.isDead:
                enemies.append(obj)
        if len(enemies):
            self.isTargetChosen = True
            self.target = enemies[random.randint(0, len(enemies) - 1)]

    def collide(self, obj):
        if obj.isDead:
            return

        def isInRect(x, y, obj):
            return obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height

        res = isInRect(self.x, self.y, obj)
        res |= isInRect(self.x + self.width, self.y, obj)
        res |= isInRect(self.x + self.width, self.y + self.height, obj)
        res |= isInRect(self.x, self.y + self.height, obj)
        return res

    def act(self):
        if (self.isDead):
            return
        self.chooseTarget()
        atProb = random.randint(1, 200) <= 9
        if not self.isAttacking:
            if self.isTargetChosen and self.collide(self.target) and atProb:
                self.attackCount = 0
                self.attackType = 0
                self.isAttacking = True
        else:
            if (self.attackCount == 0):
                sound['punch'].play()
            self.attackCount += 1
            if (self.attackCount == 4):
                self.target.damage(self.dmg * (self.attackType + 1))
            if self.attackCount == 8:
                if self.isTargetChosen and self.collide(self.target):
                    self.attackType += 1
                    if self.attackType == 3:
                        self.attackType = 0
                        self.isAttacking = False
                    self.attackCount = 0
                else:
                    self.isAttacking = False
                    self.attackCount = 0
                    self.attackType = 0
        if not self.isTargetChosen:
            self.isIdle = True
            return
        if self.collide(self.target):
            self.isLeft = self.x >= self.target.x
            self.isIdle = True
        elif self.x <= self.target.x:
            self.x += (self.speed + 2 * random.randint(0, 1) - 1)
            self.isLeft = False
            self.isIdle = False
        else:
            self.x -= (self.speed + 2 * random.randint(0, 1) - 1)
            self.isLeft = True
            self.isIdle = False
        jumpProb = random.randint(1, 100) <= 2
        if self.isTargetChosen and not self.isJump and jumpProb:
            self.isJump = True
        if self.isJump:
            if self.jumpCount >= -10:
                self.y -= self.jumpCount
                self.jumpCount -= 1
            else:
                self.jumpCount = 10
                self.isJump = False

    def damage(self, dmg):
        self.hp -= dmg
        sound['hit'].play()
        self.underAttack = True
        if self.hp <= 0:
            global score
            if not self.friendly:
                score += 10
            self.isDead = True

    def animate(self):
        global win
        if self.isDead:
            win.blit(self.pictures['dead{}'.format('L' if self.isLeft else 'R')]
                     [0], (self.x, sizeY - self.height + 15))
            return
        if self.isAttacking:
            win.blit(self.pictures['attack{}'.format('L' if self.isLeft else 'R')]
                     [self.attackType][self.attackCount // 3], (self.x, self.y))
        elif self.underAttack:
            win.blit(self.pictures['und_at{}'.format('L' if self.isLeft else 'R')]
                     [self.uaCount // 10], (self.x, self.y))
            self.uaCount += 1
            if self.uaCount == 20:
                self.uaCount = 0
                self.underAttack = False
        elif self.isJump:
            win.blit(self.pictures['jump{}'.format('L' if self.isLeft else 'R')]
                     [(self.jumpCount + 10) // 7], (self.x, self.y))
        elif self.isIdle:
            win.blit(self.pictures['idle{}'.format('L' if self.isLeft else 'R')]
                     [self.animCount // (5 if self.friendly else 8)], (self.x, self.y))
            self.animCount += 1
            self.animCount %= 30
        else:
            win.blit(self.pictures['run{}'.format('L' if self.isLeft else 'R')]
                     [self.animCount // 5], (self.x, self.y))
            self.animCount += 1
            self.animCount %= 30


narutoImg = {'runR': [], 'runL': [], 'idleR': [], 'idleL': [],
             'jumpR': [], 'jumpL': [], 'attackR': [[], [], []],
             'attackL': [[], [], []], 'deadL': [], 'deadR': []}
for i in range(6):
    for key in narutoImg.keys():
        try:
            if key == 'attackL' or key == 'attackR':
                narutoImg[key][0].append(pygame.image.load('img/{}_{}/1{}.png'.format('naruto', key, str(i + 1))))
                narutoImg[key][1].append(pygame.image.load('img/{}_{}/2{}.png'.format('naruto', key, str(i + 1))))
                narutoImg[key][2].append(pygame.image.load('img/{}_{}/3{}.png'.format('naruto', key, str(i + 1))))
            else:
                narutoImg[key].append(pygame.image.load('img/{}_{}/{}.png'.format('naruto', key, str(i + 1))))
        except:
            pass
enemyImg = {'runR': [], 'runL': [], 'idleR': [],
            'idleL': [], 'jumpR': [], 'jumpL': [],
            'attackR': [[], [], []], 'attackL': [[], [], []], 'deadL': [],
            'deadR': [], 'und_atL': [], 'und_atR': []}
for i in range(6):
    for key in enemyImg.keys():
        try:
            if key == 'attackL' or key == 'attackR':
                enemyImg[key][0].append(pygame.image.load('img/{}_{}/1{}.png'.format('enemy', key, str(i + 1))))
                enemyImg[key][1].append(pygame.image.load('img/{}_{}/2{}.png'.format('enemy', key, str(i + 1))))
                enemyImg[key][2].append(pygame.image.load('img/{}_{}/3{}.png'.format('enemy', key, str(i + 1))))
            else:
                enemyImg[key].append(pygame.image.load('img/{}_{}/{}.png'.format('enemy', key, str(i + 1))))
        except:
            pass
imgBackground = pygame.image.load('img/bg.png')


def DrawWindow(objects):
    win.blit(imgBackground, (0, 0))
    for obj in objects:
        obj.animate()
    win.blit(usedFont.render('Score: ' + str(score), 0, (0, 0, 0)), (20, 40))
    if objects[0].isDead:
        win.blit(usedFont.render('GAME OVER! Press ESC to quit', 0, (0, 0, 0)), (100, 90))
    pygame.display.update()


run = True
objects.append(Hero(narutoImg))
enemiesCounter = 0
bodiesCounter = 0

while run:
    clock.tick(30)
    enemiesCounter += 1
    bodiesCounter += 1
    if bodiesCounter == 900:
        i = 0
        while i < len(objects):
            if objects[i].isDead and i > 0:
                objects[i] = objects[-1]
                objects.pop()
            if i < len(objects) and not objects[i].isDead:
                i += 1
        bodiesCounter = 0
    if enemiesCounter == 70:
        objects.append(Bot(enemyImg))
        enemiesCounter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for obj in objects:
        obj.act()
    DrawWindow(objects)
    if (pygame.key.get_pressed()[pygame.K_ESCAPE]):
        pygame.quit()
        break
