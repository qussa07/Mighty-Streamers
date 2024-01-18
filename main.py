import pygame

clock = pygame.time.Clock()
fps = 60
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Mighty Streamer')
background = pygame.image.load('images/bg.jpg')

count = 0

colide = []

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
let_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()

tile_images = {
    'block': pygame.image.load('images/blocks/blockDirth1.png'),
    'box': pygame.image.load('images/blocks/blockPrepatstvie.png'),
    'clouds': pygame.image.load('images/blocks/Clouds.png')
}
tile_width = tile_height = 70


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Mob:
    def __init__(self, x, y):
        self.base_height = y
        self.mframe = 0
        skin = pygame.image.load('images/MobSprite/MobLeft/MobLethalLeft1.png')
        self.mob = pygame.sprite.Sprite()
        self.mob.image = skin
        self.mob.rect = self.mob.image.get_rect()
        self.render = pygame.sprite.Group()
        self.render.add(self.mob)
        self.mob.rect.x = x
        self.mob.rect.y = y
        self.hp = 3

    def attack_left(self, sc, mframe):
        if mframe == 7:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackLeft/MobAttackLeft1.png')

        elif mframe == 14:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackLeft/MobAttackLeft2.png')
        elif mframe == 21:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackLeft/MobAttackLeft3.png')
        elif mframe == 28:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackLeft/MobAttackLeft4.png')

    def attack_right(self, sc, mframe):
        if mframe == 7:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackRight/MobAttackRight1.png')
        elif mframe == 14:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackRight/MobAttackRight2.png')
        elif mframe == 21:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackRight/MobAttackRight3.png')
        elif mframe == 28:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobAttackRight/MobAttackRight4.png')

    def rendering(self, screen, player):
        if self.mob.rect.x > player.player.rect.x:
            self.mob_left(self.mframe)
        elif self.mob.rect.x < player.player.rect.x:
            self.mob_right(self.mframe)
        self.render.draw(screen)

    def mob_left(self, mframe):
        if mframe == 7:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobLeft/MobLethalLeft1.png')
        elif mframe == 14:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobLeft/MobLethalLeft2.png')
        elif mframe == 21:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobLeft/MobLethalLeft3.png')
        elif mframe == 28:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobLeft/MobLethalLeft4.png')
        self.mob.rect.x -= 2

    def mob_right(self, mframe):
        if mframe == 7:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobRight/MobLethalRight1.png')
        elif mframe == 14:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobRight/MobLethalRight2.png')
        elif mframe == 21:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobRight/MobLethalRight3.png')
        elif mframe == 28:
            self.mob.image = pygame.image.load(f'images/MobSprite/MobRight/MobLethalRight3.png')
        self.mob.rect.x += 2

    def check(self, mframe):
        if mframe == 28:
            mframe = 0

        return mframe

    def follow_player(self, player):
        player_rect = player.get_rect()
        mob_rect = self.mob.rect

        # Проверяем столкновение
        if mob_rect.colliderect(player_rect):
            if self.mob.rect.x > player.player.rect.x:
                self.attack_left(screen)
            else:
                self.attack_right(screen)
            return

        # Оставляем ваш текущий код для перемещения моба
        if self.mframe < 28:
            self.mframe += 1
        else:
            self.mframe = 0

        if self.mob.rect.x > player.player.rect.x:
            self.mob_left(self.mframe)
        elif self.mob.rect.x < player.player.rect.x:
            self.mob_right(self.mframe)


class Player:
    def __init__(self, x, y):
        skin = pygame.image.load('images/Player/PlayerLeft/playerleft1.png')
        self.player = pygame.sprite.Sprite()
        self.player.image = skin
        self.player.rect = self.player.image.get_rect(bottomright=(x, y))
        self.x = x
        self.y = y
        self.render = pygame.sprite.Group()
        self.render.add(self.player)
        self.health_points = 3
        self.count = 0
        self.flag = 1
        self.side = 0
        self.jumping = 0
        self.move = 0
        self.sides = ['Left', 'Right']
        self.playerleft1 = pygame.image.load(f'images/Player/PlayerLeft/playerleft1.png').convert_alpha()
        self.playerleft2 = pygame.image.load(f'images/Player/PlayerLeft/playerleft2.png').convert_alpha()
        self.playerleft3 = pygame.image.load(f'images/Player/PlayerLeft/playerleft3.png').convert_alpha()
        self.playerleft4 = pygame.image.load(f'images/Player/PlayerLeft/playerleft4.png').convert_alpha()
        self.playerRight1 = pygame.image.load(f'images/Player/PlayerRight/playerRight1.png').convert_alpha()
        self.playerRight2 = pygame.image.load(f'images/Player/PlayerRight/playerRight2.png').convert_alpha()
        self.playerRight3 = pygame.image.load(f'images/Player/PlayerRight/playerRight3.png').convert_alpha()
        self.playerRight4 = pygame.image.load(f'images/Player/PlayerRight/playerRight4.png').convert_alpha()
        self.hp0 = pygame.image.load(f'images/hp/0HP.png').convert_alpha()
        self.hp1 = pygame.image.load(f'images/hp/1HP.png').convert_alpha()
        self.hp2 = pygame.image.load(f'images/hp/2HP.png').convert_alpha()
        self.hp3 = pygame.image.load(f'images/hp/FullHP.png').convert_alpha()
        self.on_floor = 1

    def rendering(self, screen, frame):
        if self.flag == 2:
            if frame == 2:
                self.player.image = pygame.image.load(
                    f'images/Player/Player{self.sides[self.side]}Sword/PlayerAttack{self.sides[self.side]}1.png').convert_alpha()
            elif frame == 4:
                self.player.image = pygame.image.load(
                    f'images/Player/Player{self.sides[self.side]}Sword/PlayerAttack{self.sides[self.side]}2.png').convert_alpha()
            elif frame == 6:
                self.player.image = pygame.image.load(
                    f'images/Player/Player{self.sides[self.side]}Sword/PlayerAttack{self.sides[self.side]}3.png').convert_alpha()
            elif frame == 8:
                self.player.image = pygame.image.load(
                    f'images/Player/Player{self.sides[self.side]}Sword/PlayerAttack{self.sides[self.side]}4.png').convert_alpha()
                self.player.rect = self.player.image.get_rect(bottomleft=(self.x, self.y))
                self.flag = 1
                self.y -= 10
        elif self.flag == 1:
            if self.side == 1:
                self.player.image = self.playerRight1
                self.flag = 0
            else:
                self.player.image = self.playerleft1
                self.flag = 0
        elif self.flag == 3:
            self.jumping += 1
            if self.jumping <= 6:
                self.y -= 15
            elif 6 <= self.jumping <= 10:
                self.y -= 5
            elif 10 <= self.jumping <= 20 and self.stop:
                self.y += 11
            else:
                self.flag = 1
                self.jumping = 0

        if pygame.sprite.spritecollide(self.player, let_group, False, pygame.sprite.collide_mask):
            self.stop = 0
        else:
            self.stop = 1

        if pygame.sprite.spritecollide(self.player, floor_group, False, pygame.sprite.collide_mask):
            pass
        else:
            if self.flag != 3 and self.stop:
                self.y += 10
        if self.side:
            self.player.rect = self.player.image.get_rect(bottomleft=(self.x, self.y))
        else:
            self.player.rect = self.player.image.get_rect(bottomright=(self.x, self.y))
        self.render.draw(screen)
        self.dead()

    def walk_left(self, frame):
        if frame == 7:
            self.player.image = self.playerleft1
        elif frame == 14:
            self.player.image = self.playerleft2
        elif frame == 21:
            self.player.image = self.playerleft3
        elif frame == 28:
            self.player.image = self.playerleft4
        if self.player.rect.x > 150:
            self.x -= 4
        else:
            self.move += 2
        self.side = 0

    def walk_right(self, frame):
        if frame == 7:
            self.player.image = self.playerRight1
        elif frame == 14:
            self.player.image = self.playerRight2
        elif frame == 21:
            self.player.image = self.playerRight3
        elif frame == 28:
            self.player.image = self.playerRight4
        if self.player.rect.x < 1000:
            self.x += 4
        else:
            self.move -= 2
        self.side = 1

    def check(self, frame):
        if frame == 28:
            frame = 0

        return frame

    def attack(self):
        if self.flag != 3:
            self.flag = 2

    def jump(self):
        if self.flag != 2:
            self.flag = 3

    def dead(self):
        if self.y > 1300:
            pygame.quit()
            exit()


def generate_level(level, screen, move=0):
    global count
    floor_group.empty()
    all_sprites.empty()
    tiles_group.empty()
    enemy_group.empty()
    let_group.empty()
    x, y = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                screen.blit(tile_images['block'], (tile_width * x + move, tile_height * y))
                a = pygame.sprite.Sprite()
                a.image = tile_images['block']
                a.rect = a.image.get_rect(topleft=(tile_width * x + move, tile_height * y))
                floor_group.add(a)
            elif level[y][x] == '*':
                screen.blit(tile_images['box'], (tile_width * x + move, tile_height * y))
                a = pygame.sprite.Sprite()
                a.image = tile_images['box']
                a.rect = a.image.get_rect(topleft=(tile_width * x + move, tile_height * y))
                let_group.add(a)
            elif level[y][x] == '!':
                a = Mob(tile_width * x + move, tile_height * y - 120)
                enemy_group.add(a.mob)
            elif level[y][x] == '^':
                screen.blit(
                    tile_images['clouds'].get_rect(topleft=(tile_width * x + move, tile_height * y)))
            elif level[y][x] == '@':
                d = Player(tile_width * x, tile_height * y)
            count = 1
    return d

class up:
    def __init__(self):
        self.sp = []
    def add(self, a):
        for i in a:
            self.sp.append(i)
    def update(self, pla):
        """for i in self.sp:
            i.foo"""

size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
main_character = generate_level(load_level('maps/map.txt'), screen)
frame = 0
running = True
while running:
    frame += 1
    screen.blit(background, (0, 0))
    generate_level(load_level('maps/map.txt'), screen, main_character.move)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP and (event.key == pygame.K_d or event.key == pygame.K_a):
            if keys[pygame.K_d]:
                main_character.walk_right(7)
            if keys[pygame.K_a]:
                main_character.walk_left(7)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                main_character.attack()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            main_character.jump()
    main_character.rendering(screen, frame)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        main_character.walk_right(frame)
    if keys[pygame.K_a]:
        main_character.walk_left(frame)
    frame = main_character.check(frame)
    clock.tick(fps)
    enemy_group.draw(screen)
    pygame.display.flip()
