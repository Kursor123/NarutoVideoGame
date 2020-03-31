import pygame
import random

#pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
clock = pygame.time.Clock()
random.seed()

sizeX = 504
sizeY = 350
speed = 7
botSpeed = 5
objects = []
sound = {'hit': pygame.mixer.Sound('sound/hit.wav'), 'punch': pygame.mixer.Sound('sound/punch.wav')}

win = pygame.display.set_mode((sizeX, sizeY))
pygame.display.set_caption('Naruto Shippuden Video Game')
pygame.mixer.music.load('sound/main_theme.mp3')
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
        self.img = pictures['idleR'][0]
        self.isAttacking = False
        self.isJump = False
        self.jumpCount = 10
        self.animCount = 0
        self.attackCount = 0
        self.attackType = 0
        self.friendly = friendly
        self.hp = 300
        self.isDead = False

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
                        obj.damage(10 * (self.attackType + 1))
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
            self.x -= speed
            self.isLeft = True
            self.isIdle = False
        elif keys[pygame.K_d] and self.x < sizeX - self.width - 5:
            self.x += speed
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
        x = self.x
        y = self.y
        res = obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        x += self.width
        res |= obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        y += self.height
        res |= obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        x -= self.width
        res |= obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        return res

    def animate(self):
        global win
        if self.isDead:
            win.blit(self.pictures['dead'], (self.x, self.y))
            return
        pygame.draw.rect(win, (255, 0, 0), (20, 20, 300, 10))
        pygame.draw.rect(win, (0, 255, 0), (20, 20, self.hp, 10))
        pygame.draw.rect(win, (0, 0, 0), (20, 20, 300, 10), 1)
        if self.isLeft:
            if self.isAttacking:
                win.blit(self.pictures['attackL'][self.attackType][self.attackCount // 2], (self.x, self.y))
            elif self.isJump:
                win.blit(self.pictures['jumpL'][(self.jumpCount + 10) // 7], (self.x, self.y))
            elif self.isIdle:
                win.blit(self.pictures['idleL'][self.animCount // 5], (self.x, self.y))
                self.animCount += 1
                self.animCount %= 30
            else:
                win.blit(self.pictures['runL'][self.animCount // 5], (self.x, self.y))
                self.animCount += 1
                self.animCount %= 30
        else:
            if self.isAttacking:
                win.blit(self.pictures['attackR'][self.attackType][self.attackCount // 2], (self.x, self.y))
            elif self.isJump:
                win.blit(self.pictures['jumpR'][(self.jumpCount + 10) // 7], (self.x, self.y))
            elif self.isIdle:
                win.blit(self.pictures['idleR'][self.animCount // 5], (self.x, self.y))
                self.animCount += 1
                self.animCount %= 30
            else:
                win.blit(self.pictures['runR'][self.animCount // 5],
                         (self.x + (14 if (self.animCount // 5) % 3 == 0 else 0), self.y))
                self.animCount += 1
                self.animCount %= 30


class Bot:
    def __init__(self, pictures, friendly=False):
        self.width = 43
        self.height = 58 if friendly else 43
        self.x = 250 + (2 * random.randint(0, 1) - 1) * 300
        self.y = sizeY - self.height - 15
        self.isIdle = True
        self.isLeft = False
        self.pictures = pictures
        self.img = pictures['idleR'][0]
        self.isAttacking = False
        self.isJump = False
        self.jumpCount = 10
        self.animCount = 0
        self.attackCount = 0
        self.attackType = 0
        self.friendly = friendly
        self.isTargetChosen = False
        self.hp = 50
        self.isDead = False

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
        x = self.x
        y = self.y
        res = obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        x += self.width
        res |= obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        y += self.height
        res |= obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        x -= self.width
        res |= obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height
        return res

    def act(self):
        if(self.isDead):
            return
        self.chooseTarget()
        atProb = random.randint(1, 100) <= 5
        if not self.isAttacking:
            if self.isTargetChosen and self.collide(self.target) and atProb:
                self.attackCount = 0
                self.attackType = 0
                self.isAttacking = True
        else:
            if(self.attackCount == 0):
                sound['punch'].play()
            self.attackCount += 1
            if(self.attackCount == 4):
                self.target.damage(10 * (self.attackType + 1))
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
            self.x += (botSpeed + 2 * random.randint(0, 1) - 1)
            self.isLeft = False
            self.isIdle = False
        else:
            self.x -= (botSpeed + 2 * random.randint(0, 1) - 1)
            self.isLeft = True
            self.isIdle = False
        jumpProb = random.randint(1, 100) <= 3
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
        if self.hp <= 0:
            self.isDead = True

    def animate(self):
        global win
        if self.isDead:
            win.blit(self.pictures['dead'], (self.x, sizeY - self.height + 15))
            return
        if self.isLeft:
            if self.isAttacking:
                win.blit(self.pictures['attackL'][self.attackType][self.attackCount // 2], (self.x, self.y))
            elif self.isJump:
                win.blit(self.pictures['jumpL'][(self.jumpCount + 10) // 7], (self.x, self.y))
            elif self.isIdle:
                win.blit(self.pictures['idleL'][self.animCount // (5 if self.friendly else 8)], (self.x, self.y))
                self.animCount += 1
                self.animCount %= 30
            else:
                win.blit(self.pictures['runL'][self.animCount // 5], (self.x, self.y))
                self.animCount += 1
                self.animCount %= 30
        else:
            if self.isAttacking:
                win.blit(self.pictures['attackR'][self.attackType][self.attackCount // 2], (self.x, self.y))
            elif self.isJump:
                win.blit(self.pictures['jumpR'][(self.jumpCount + 10) // 7], (self.x, self.y))
            elif self.isIdle:
                win.blit(self.pictures['idleR'][self.animCount // (5 if self.friendly else 8)], (self.x, self.y))
                self.animCount += 1
                self.animCount %= 30
            else:
                win.blit(self.pictures['runR'][self.animCount // 5],
                         (self.x + (14 if (self.animCount // 5) % 3 == 0 else 0), self.y))
                self.animCount += 1
                self.animCount %= 30


imgPlayerWalkRight = [pygame.image.load('img/naruto_run_right/naruto_run_right_1.png'),
                      pygame.image.load('img/naruto_run_right/naruto_run_right_2.png'),
                      pygame.image.load('img/naruto_run_right/naruto_run_right_3.png'),
                      pygame.image.load('img/naruto_run_right/naruto_run_right_4.png'),
                      pygame.image.load('img/naruto_run_right/naruto_run_right_5.png'),
                      pygame.image.load('img/naruto_run_right/naruto_run_right_6.png')]
imgPlayerWalkLeft = [pygame.image.load('img/naruto_run_left/naruto_run_left_1.png'),
                     pygame.image.load('img/naruto_run_left/naruto_run_left_2.png'),
                     pygame.image.load('img/naruto_run_left/naruto_run_left_3.png'),
                     pygame.image.load('img/naruto_run_left/naruto_run_left_4.png'),
                     pygame.image.load('img/naruto_run_left/naruto_run_left_5.png'),
                     pygame.image.load('img/naruto_run_left/naruto_run_left_6.png')]
imgPlayerStandRight = [pygame.image.load('img/naruto_stand_right/naruto_stand_right_1.png'),
                       pygame.image.load('img/naruto_stand_right/naruto_stand_right_2.png'),
                       pygame.image.load('img/naruto_stand_right/naruto_stand_right_3.png'),
                       pygame.image.load('img/naruto_stand_right/naruto_stand_right_4.png'),
                       pygame.image.load('img/naruto_stand_right/naruto_stand_right_5.png'),
                       pygame.image.load('img/naruto_stand_right/naruto_stand_right_6.png')]
imgPlayerStandLeft = [pygame.image.load('img/naruto_stand_left/naruto_stand_left_1.png'),
                      pygame.image.load('img/naruto_stand_left/naruto_stand_left_2.png'),
                      pygame.image.load('img/naruto_stand_left/naruto_stand_left_3.png'),
                      pygame.image.load('img/naruto_stand_left/naruto_stand_left_4.png'),
                      pygame.image.load('img/naruto_stand_left/naruto_stand_left_5.png'),
                      pygame.image.load('img/naruto_stand_left/naruto_stand_left_6.png')]
imgPlayerJumpRight = [  # pygame.image.load('img/naruto_jump_right/naruto_jump_right_1.png'),
    pygame.image.load('img/naruto_jump_right/naruto_jump_right_2.png'),
    pygame.image.load('img/naruto_jump_right/naruto_jump_right_3.png'),
    pygame.image.load('img/naruto_jump_right/naruto_jump_right_4.png'),
    pygame.image.load('img/naruto_jump_right/naruto_jump_right_5.png')]
imgPlayerJumpLeft = [  # pygame.image.load('img/naruto_jump_left/naruto_jump_left_1.png'),
    pygame.image.load('img/naruto_jump_left/naruto_jump_left_2.png'),
    pygame.image.load('img/naruto_jump_left/naruto_jump_left_3.png'),
    pygame.image.load('img/naruto_jump_left/naruto_jump_left_4.png'),
    pygame.image.load('img/naruto_jump_left/naruto_jump_left_5.png')]
imgPlayerAttackRight = [[pygame.image.load('img\\naruto_light_attack_right\\naruto_light_attack_right_1.png'),
                         pygame.image.load('img\\naruto_light_attack_right\\naruto_light_attack_right_2.png'),
                         pygame.image.load('img\\naruto_light_attack_right\\naruto_light_attack_right_3.png'),
                         pygame.image.load('img\\naruto_light_attack_right\\naruto_light_attack_right_4.png')], [pygame.image.load('img\\naruto_head_attack_right\\naruto_head_attack_right_1.png'),
                         pygame.image.load('img\\naruto_head_attack_right\\naruto_head_attack_right_2.png'),
                         pygame.image.load('img\\naruto_head_attack_right\\naruto_head_attack_right_3.png'),
                         pygame.image.load('img\\naruto_head_attack_right\\naruto_head_attack_right_4.png')], [pygame.image.load('img\\naruto_heavy_attack_right\\naruto_heavy_attack_right_1.png'),
                         pygame.image.load('img\\naruto_heavy_attack_right\\naruto_heavy_attack_right_2.png'),
                         pygame.image.load('img\\naruto_heavy_attack_right\\naruto_heavy_attack_right_3.png'),
                         pygame.image.load('img\\naruto_heavy_attack_right\\naruto_heavy_attack_right_4.png')]]
imgPlayerAttackLeft = [[pygame.image.load('img\\naruto_light_attack_left\\naruto_light_attack_left_1.png'),
                        pygame.image.load('img\\naruto_light_attack_left\\naruto_light_attack_left_2.png'),
                        pygame.image.load('img\\naruto_light_attack_left\\naruto_light_attack_left_3.png'),
                        pygame.image.load('img\\naruto_light_attack_left\\naruto_light_attack_left_4.png')], [pygame.image.load('img\\naruto_head_attack_left\\naruto_head_attack_left_1.png'),
                        pygame.image.load('img\\naruto_head_attack_left\\naruto_head_attack_left_2.png'),
                        pygame.image.load('img\\naruto_head_attack_left\\naruto_head_attack_left_3.png'),
                        pygame.image.load('img\\naruto_head_attack_left\\naruto_head_attack_left_4.png')], [pygame.image.load('img\\naruto_heavy_attack_left\\naruto_heavy_attack_left_1.png'),
                        pygame.image.load('img\\naruto_heavy_attack_left\\naruto_heavy_attack_left_2.png'),
                        pygame.image.load('img\\naruto_heavy_attack_left\\naruto_heavy_attack_left_3.png'),
                        pygame.image.load('img\\naruto_heavy_attack_left\\naruto_heavy_attack_left_4.png')]]
imgDead = pygame.image.load('img/dead.png')
narutoImg = {'runR': imgPlayerWalkRight, 'runL': imgPlayerWalkLeft, 'idleR': imgPlayerStandRight,
             'idleL': imgPlayerStandLeft,
             'jumpR': imgPlayerJumpRight, 'jumpL': imgPlayerJumpLeft, 'attackR': imgPlayerAttackRight,
             'attackL': imgPlayerAttackLeft, 'dead': imgDead}

imgSNWalkRight = [pygame.image.load('img/enemy_run_right/enemy_run_right_1.png'),
                      pygame.image.load('img/enemy_run_right/enemy_run_right_2.png'),
                      pygame.image.load('img/enemy_run_right/enemy_run_right_3.png'),
                      pygame.image.load('img/enemy_run_right/enemy_run_right_4.png'),
                      pygame.image.load('img/enemy_run_right/enemy_run_right_5.png'),
                      pygame.image.load('img/enemy_run_right/enemy_run_right_6.png')]
imgSNWalkLeft = [pygame.image.load('img/enemy_run_left/enemy_run_left_1.png'),
                      pygame.image.load('img/enemy_run_left/enemy_run_left_2.png'),
                      pygame.image.load('img/enemy_run_left/enemy_run_left_3.png'),
                      pygame.image.load('img/enemy_run_left/enemy_run_left_4.png'),
                      pygame.image.load('img/enemy_run_left/enemy_run_left_5.png'),
                      pygame.image.load('img/enemy_run_left/enemy_run_left_6.png')]
imgSNStandRight = [pygame.image.load('img/enemy_stand_right/enemy_stand_right_1.png'),
                      pygame.image.load('img/enemy_stand_right/enemy_stand_right_2.png'),
                      pygame.image.load('img/enemy_stand_right/enemy_stand_right_3.png'),
                      pygame.image.load('img/enemy_stand_right/enemy_stand_right_4.png')]
imgSNStandLeft = [pygame.image.load('img/enemy_stand_left/enemy_stand_left_1.png'),
                      pygame.image.load('img/enemy_stand_left/enemy_stand_left_2.png'),
                      pygame.image.load('img/enemy_stand_left/enemy_stand_left_3.png'),
                      pygame.image.load('img/enemy_stand_left/enemy_stand_left_4.png')]
imgSNAttackRight = [[pygame.image.load('img/enemy_attack_right/enemy_attack_right_1.png'),
                     pygame.image.load('img/enemy_attack_right/enemy_attack_right_2.png'),
                     pygame.image.load('img/enemy_attack_right/enemy_attack_right_3.png'),
                     pygame.image.load('img/enemy_attack_right/enemy_attack_right_4.png')],
                    [pygame.image.load('img/enemy_attack_right/enemy_attack_right_5.png'),
                     pygame.image.load('img/enemy_attack_right/enemy_attack_right_6.png'),
                     pygame.image.load('img/enemy_attack_right/enemy_attack_right_7.png'),
                     pygame.image.load('img/enemy_attack_right/enemy_attack_right_8.png')],
                    [pygame.image.load('img/enemy_knife_attack_right/enemy_knife_attack_right_1.png'),
                     pygame.image.load('img/enemy_knife_attack_right/enemy_knife_attack_right_2.png'),
                     pygame.image.load('img/enemy_knife_attack_right/enemy_knife_attack_right_3.png'),
                     pygame.image.load('img/enemy_knife_attack_right/enemy_knife_attack_right_4.png')]]
imgSNAttackLeft = [[pygame.image.load('img/enemy_attack_left/enemy_attack_left_1.png'),
                     pygame.image.load('img/enemy_attack_left/enemy_attack_left_2.png'),
                     pygame.image.load('img/enemy_attack_left/enemy_attack_left_3.png'),
                     pygame.image.load('img/enemy_attack_left/enemy_attack_left_4.png')],
                    [pygame.image.load('img/enemy_attack_left/enemy_attack_left_5.png'),
                     pygame.image.load('img/enemy_attack_left/enemy_attack_left_6.png'),
                     pygame.image.load('img/enemy_attack_left/enemy_attack_left_7.png'),
                     pygame.image.load('img/enemy_attack_left/enemy_attack_left_8.png')],
                    [pygame.image.load('img/enemy_knife_attack_left/enemy_knife_attack_left_1.png'),
                     pygame.image.load('img/enemy_knife_attack_left/enemy_knife_attack_left_2.png'),
                     pygame.image.load('img/enemy_knife_attack_left/enemy_knife_attack_left_3.png'),
                     pygame.image.load('img/enemy_knife_attack_left/enemy_knife_attack_left_4.png')]]
enemyImg = {'runR': imgSNWalkRight, 'runL': imgSNWalkLeft, 'idleR': imgSNStandRight,
             'idleL': imgSNStandLeft,
             'jumpR': imgSNStandRight, 'jumpL': imgSNStandLeft, 'attackR': imgSNAttackRight,
             'attackL': imgSNAttackLeft, 'dead': pygame.image.load('img/enemy_under_attack_left/enemy_under_attack_left_4.png')}
imgBackground = pygame.image.load('img/background_konoha.png')


def DrawWindow(objects):
    win.blit(imgBackground, (0, 0))
    for obj in objects:
        obj.animate()
    pygame.display.update()


run = True
objects.append(Hero(narutoImg))
enemiesCounter = 0

while run:
    clock.tick(30)
    enemiesCounter += 1
    if enemiesCounter == 200:
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
