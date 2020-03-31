import pygame

pygame.init()
clock = pygame.time.Clock()

sizeX = 504
sizeY = 350
speed = 7

win = pygame.display.set_mode((sizeX, sizeY))
pygame.display.set_caption('Naruto Shippuden Video Game')
pygame.mixer.music.load('sound/main_theme.mp3')
pygame.mixer.music.play(-1)


class Hero:
    def __init__(self, pictures, x=50):
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
    def act(self):
        keys = pygame.key.get_pressed()
        if not self.isAttacking:
            if keys[pygame.K_j]:
                self.attackCount = 0
                self.attackType = 0
                self.isAttacking = True
        else:
            self.attackCount += 1
            if self.attackCount == 8:
                if keys[pygame.K_j]:
                    self.attackType += 1
                    if(self.attackType == 3):
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

    def animate(self):
        global win
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
                win.blit(self.pictures['runR'][self.animCount // 5], (self.x + (14 if (self.animCount // 5) % 3 == 0 else 0), self.y))
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
imgPlayerJumpRight = [#pygame.image.load('img/naruto_jump_right/naruto_jump_right_1.png'),
                  pygame.image.load('img/naruto_jump_right/naruto_jump_right_2.png'),
                  pygame.image.load('img/naruto_jump_right/naruto_jump_right_3.png'),
                  pygame.image.load('img/naruto_jump_right/naruto_jump_right_4.png'),
                  pygame.image.load('img/naruto_jump_right/naruto_jump_right_5.png')]
imgPlayerJumpLeft = [#pygame.image.load('img/naruto_jump_left/naruto_jump_left_1.png'),
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

narutoImg = {'runR': imgPlayerWalkRight, 'runL': imgPlayerWalkLeft, 'idleR': imgPlayerStandRight, 'idleL': imgPlayerStandLeft,
             'jumpR': imgPlayerJumpRight, 'jumpL': imgPlayerJumpLeft, 'attackR': imgPlayerAttackRight, 'attackL': imgPlayerAttackLeft}
imgBackground = pygame.image.load('img/background_konoha.png')


def DrawWindow(objects):
    win.blit(imgBackground, (0, 0))
    for obj in objects:
        obj.animate()
    pygame.display.update()


run = True
objects = [Hero(narutoImg)]
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for obj in objects:
        obj.act()
    DrawWindow(objects)
    if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
        pygame.quit()
        break
