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

class Character:
    def __init__(self, pictures, x, friendly, hp, speed):
        self.pictures = pictures
        self.width = 43
        self.height = 58 if friendly else 43
        self.x = x
        self.y = sizeY - self.height - 15
        self.isIdle = True
        self.isLeft = False
        self.isDead = False
        self.isAttacking = False
        self.isJump = False
        self.underAttack = False
        self.uaCount = 0
        self.jumpCount = 10
        self.animCount = 0
        self.attackCount = 0
        self.deadCount = 0
        self.attackType = 0
        self.friendly = friendly
        self.hp = hp
        self.speed = speed

    def damage(self, dmg):
        self.hp -= dmg
        sound['hit'].play()
        self.underAttack = True
        if self.hp <= 0:
            global score
            if not self.friendly:
                score += 10
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

    def attack(self, cnd1, cnd2):
        if not self.isAttacking:
            if cnd1:
                self.attackCount = 0
                self.attackType = 0
                self.isAttacking = True
        else:
            if self.attackCount == 0:
                sound['punch'].play()
            self.attackCount += 1
            if self.attackCount == 4:
                for obj in objects:
                    if obj.friendly != self.friendly and self.collide(obj):
                        obj.damage(self.dmg * (self.attackType + 1))
            if self.attackCount == 8:
                if cnd2:
                    self.attackType += 1
                    if (self.attackType == 3):
                        self.attackType = 0
                        self.isAttacking = False
                    self.attackCount = 0
                else:
                    self.isAttacking = False
                    self.attackCount = 0
                    self.attackType = 0

    def jump(self, cnd):
        if not self.isJump:
            if cnd:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                self.y -= 2 * self.jumpCount
                self.jumpCount -= 1
            else:
                self.jumpCount = 10
                self.isJump = False

    def animate_char(self):
        global win
        if self.isDead:
            win.blit(self.pictures['dead{}'.format('L' if self.isLeft else 'R')]
                     [3 if self.friendly else 0], (self.x, sizeY - self.height + 15))
            return
        if self.isAttacking:
            win.blit(self.pictures['attack{}'.format('L' if self.isLeft else 'R')]
                     [self.attackType][self.attackCount // 2 if self.friendly else 3], (self.x, self.y))
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

class Hero(Character):
    def __init__(self, pictures, x=50, friendly=True):
        super().__init__(pictures, x, friendly, 300, 8)
        self.dmg = 10
        self.cp = 2000

    def shadow_clone_jutsu(self):
        if self.cp <= 1500:
            return
        amount = random.randint(1, 4)
        self.cp //= (amount + 1)
        global narutoImg
        pygame.mixer.Sound('sound/shadow_clone_jutsu.wav').play()
        for i in range(amount):
            objects.append(Bot(narutoImg, friendly=True, x=self.x, lvl=2))

    def act(self):
        if self.isDead:
            return

        self.cp += 1 if self.cp < 3000 else 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_k]:
            self.shadow_clone_jutsu()

        cnd1 = cnd2 = keys[pygame.K_j]
        self.attack(cnd1, cnd2)

        cnd1 = keys[pygame.K_a] and self.x > 5
        cnd2 = keys[pygame.K_d] and self.x < sizeX - self.width - 5
        self.isIdle = not (cnd1 or cnd2)
        self.isLeft = cnd1 if not self.isIdle else self.isLeft
        self.x += (0 if self.isIdle else 1) * (-1 if cnd1 else 1) * self.speed

        cnd = keys[pygame.K_SPACE]
        self.jump(cnd)

    def animate(self):
        global win
        win.blit(self.pictures['prof'][0], (20, 20))
        pygame.draw.rect(win, (255, 0, 0), (90, 43, 300, 10))
        pygame.draw.rect(win, (0, 200, 255), (90, 53, self.cp // 10, 10))
        pygame.draw.rect(win, (0, 0, 0), (90, 53, self.cp // 10, 10), 1)
        if not self.isDead:
            pygame.draw.rect(win, (0, 255, 0), (90, 43, self.hp, 10))
            pygame.draw.rect(win, (0, 0, 0), (90, 43, self.hp, 10), 1)
        pygame.draw.rect(win, (0, 0, 0), (90, 43, 300, 10), 1)
        pygame.draw.rect(win, (0, 0, 0), (90, 53, 300, 10), 1)
        self.animate_char()


class Bot(Character):
    def __init__(self, pictures, friendly=False, lvl=1, x = 'nt'):
        self.lvl = lvl
        self.dmg = 5 * lvl
        self.isTargetChosen = False
        x = (sizeX // 2) + (2 * random.randint(0, 1) - 1) * (
                sizeX // 2 + 50) if x == 'nt' else x
        super().__init__(pictures, x, friendly, 10 + 20 * lvl, 4 if lvl < 5 else 6)

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

    def act(self):
        if self.isDead:
            return

        self.chooseTarget()

        at_prob = random.randint(1, 200) <= 9
        cnd2 = self.isTargetChosen and self.collide(self.target)
        cnd1 = cnd2 and at_prob
        self.attack(cnd1, cnd2)

        if not self.isTargetChosen:
            self.isIdle = True
            return

        self.isLeft = (self.x > self.target.x)
        self.isIdle = self.collide(self.target)
        self.x += (-1 if self.isLeft else 1) * (0 if self.isIdle else 1) * (
            self.speed + 2 * random.randint(0, 1) - 1)

        jumpProb = random.randint(1, 200) <= 3
        cnd = self.isTargetChosen and not self.isJump and jumpProb
        self.jump(cnd)

    def animate(self):
        self.animate_char()


narutoImg = {'runR': [], 'runL': [], 'idleR': [], 'idleL': [],
             'jumpR': [], 'jumpL': [], 'attackR': [[], [], []],
             'attackL': [[], [], []], 'deadL': [], 'deadR': [], 'prof': [],
             'und_atL': [], 'und_atR': []}
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
    win.blit(usedFont.render('Score: ' + str(score), 0, (0, 0, 0)), (20, 100))
    if objects[0].isDead:
        win.blit(usedFont.render('GAME OVER! Press ESC to quit', 0, (0, 0, 0)), (350, 90))
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
    if enemiesCounter == 30:
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
