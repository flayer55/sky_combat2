# dachnik4@mail.ru

import arcade
import random
from math import sin, cos, acos, asin, radians, degrees

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DASH_WIDTH = 200
DASH_HEIGHT = 150

x = 19
y = 60 - 20
tx = SCREEN_WIDTH - x
ty = SCREEN_HEIGHT - y

img_aircraft = arcade.load_texture('img/mig.png')
img_enemy1 = arcade.load_texture('img/F4.png')
img_enemy2 = arcade.load_texture('img/enemy.png')
weapon = arcade.load_texture('img/bul.png')
weapon_2 = arcade.load_texture('img/Оружие.png')
# img_enemy2 = arcade.load_texture()
radius =15

class Base:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ang = 0
        self.speed = 0
        self.img = None
        self.size = 0
        self.soil = 0

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, self.size , self.size,
                                      self.img, 360 - self.ang)


    def move(self):
        self.dx = sin(radians(self.ang))
        self.dy = cos(radians(self.ang))

        self.x += self.speed * self.dx
        self.y += self.speed * self.dy

    def turn_left(self):
        self.ang -= 10
        if self.ang < 0:
            self.ang += 360

    def turn_right(self):
        self.ang += 10
        self.ang %= 360

    def look_to(self, x, y):
        dx_ = self.x - x
        dy_ = self.y - y
        dist = (dx_ ** 2 + dy_ ** 2) ** 0.5
        if self.y < y:
            self.ang = -90 + degrees(acos(dx_ / dist))
        else:
            self.ang = 270 - degrees(acos(dx_ / dist))

        self.ang %= 360
        if self.ang < 0:
            self.ang += 360

    # def look_to(self, obj):
    #     dx_ = self.x - obj.x
    #     dy_ = self.y - obj.y
    #     dist = (dx_ ** 2 + dy_ ** 2) ** 0.5
    #     if self.y < obj.y:
    #         self.ang = -90 + degrees(acos(dx_ / dist))
    #     else:
    #         self.ang = 270 - degrees(acos(dx_ / dist))
    #
    #     self.ang %= 360
    #     if self.ang < 0:
    #         self.ang += 360


class Bullet(Base):
    def __init__(self, x, y, ang):
        super().__init__()
        self.x = x
        self.y = y
        self.ang = ang
        self.size = 20
        self.speed = 8
        self.way = 0
        self.img = weapon
        self.dx = sin(radians(ang))
        self.dy = cos(radians(ang))
        self.fd = 400

    # def draw(self):
    #     arcade.draw_texture_rectangle(self.x, self.y, self.size , self.size + 2, self.img, self.ang)

    def move(self):
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy

    def should_remove(self):
        out_x =  not self.size < self.x< SCREEN_WIDTH - self.size * 2
        out_y = not self.size< self.y < SCREEN_HEIGHT - self.size * 2
        return  out_x or out_y


class Rocket(Bullet):
    def __init__(self, x, y, ang):
        super().__init__(Enemy().x, Enemy().y, Enemy().ang)
        self.img = weapon_2
        self.speed = 32

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, self.size, self.size, self.img)

    def move(self):
            # self.x += self.speed * self.dx
            self.y += self.speed * self.dy
    def should_remove(self):
        out_x =  not self.size < self.x< SCREEN_WIDTH - self.size
        out_y = not self.size< self.y < self.fd - self.size
        return  out_x or out_y
#

class Base_animation:
    def __init__(self, img_name):
        self.x = 100
        self.y = 100
        self.size = 100
        self.img_list = []
        self.img_name = img_name
        self.cur_page = 0
        self.counter_max = 5
        self.counter = 0

        for i in range(6):
            fname = 'img/'+ self.img_name + str(i + 1) + '.png'
            self.img_list.append(arcade.load_texture(fname))
        self.img = self.img_list[0]

    def next_page(self):
        self.cur_page += 1
        self.cur_page %= 6
        self.img = self.img_list[self.cur_page]

    def update_counter(self):
        self.counter += 1
        if self.counter >= self.counter_max:
            self.counter = 0
            self.next_page()

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, self.size , self.size, self.img)
        self.update_counter()


class Aircraft(Base):
    def __init__(self, type='fighter'):
        super().__init__()
        self.power = 60
        self.speed = 2
        self.size = 60
        self.type = type
        # self.title = 'wingman'
        if self.type == 'hero':
            self.fd = 400
            self.hp = 2600
            self.damage = 1700
            self.img = img_aircraft
        elif self.type == 'fighter':
            self.fd = 600
            self.hp = 3400
            self.damage = 100
            self.img = img_enemy1
        else:
            self.fd = 100
            self.hp = 100
            self.damage = 100
            self.img = img_enemy2

        self.hero = None

    # def draw(self):
    #     super().draw()
    #     arcade.draw_text('{}'.format(round(self.ang, 2)), self.x, self.y + 50, arcade.color.RED)

        # self.dx = sin(radians(self.ang))
        # self.dy = cos(radians(self.ang))
        # arcade.draw_line(self.x, self.y,
        #                  self.x + self.dx * self.size,
        #                  self.y + self.dy * self.size,
        #                  arcade.color.BLACK, 2)

    def power_up(self):
        if self.power <= 95:
            self.power += 5

    def power_down(self):
        if self.power >= 5:
            self.power -= 5

    def shoot(self):
        return Bullet(self.x, self.y,  self.ang)

    def is_strike(self, bullet):
        is_strike_x =  self.x - self.size / 2 < bullet.x < self.x + self.size / 2
        is_strike_y =  self.y - self.size / 2 < bullet.y < self.y + self.size / 2
        return is_strike_x and is_strike_y


class Hero(Aircraft):
    def __init__(self):
        super().__init__('hero')
        self.x = random.randint(SCREEN_WIDTH / 2, SCREEN_WIDTH - (self.size + 20))
        self.y = 50
        self.move_dir = ''
        # self.ang = 0


    def draw(self):
        super().draw()
        arcade.draw_text('{}'.format(self.hp), self.x, self.y + self.size / 2, arcade.color.DARK_GREEN)

    def move(self):
        if self.move_dir == 'right' and self.x < SCREEN_WIDTH - self.size:
            self.x += self.power * self.speed / 100
        if self.move_dir == 'left' and self.x > 0 + self.size:
            self.x -= (self.power * self.speed / 100)

    def move_stop(self):
        self.move_dir = ''

    def move_left(self):
        self.move_dir = 'left'

    def move_right(self):
        self.move_dir = 'right'


class Enemy(Aircraft):
    type_list = ['fighter', 'bomber']
    def __init__(self):
        type_aircraft = random.choice(Enemy.type_list)
        super().__init__(type_aircraft)
        self.x = random.randint(30, SCREEN_WIDTH - 30)
        self.y = SCREEN_HEIGHT - self.size * 2
        # self.y = random.randint(self.size* 2, SCREEN_HEIGHT - self.size * 2)
        self.ang = 180
        # self.move_dir = ''
        self.power = random.randint(60, 100)
        self.speed *= self.power / 100
        self.hp = 5300



    def move(self):
        super().move()
        if self.y < 0:
            self.y += SCREEN_HEIGHT
        if self.y > (20 + SCREEN_HEIGHT - 20) and self.y <= DASH_HEIGHT:
            self.y -= DASH_HEIGHT

    def rock_shoot(self):
        return Rocket(self.x, self.y, 90 - self.ang)
class Background(Base):
    def __init__(self):
        super().__init__()
        self.img = arcade.load_texture('img/background.png')
    def draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.img)
# class Telemetry():
#     def __init__(self):
#             self.x = x
#             self.y = y
#             self.radius = radius
#             self.color = [30, 250, 50]
#             s.Foil = 80000
#
#     def draw(self):
#         arcade.draw_rectangle_filled(10 + SCREEN_WIDTH - 10, 20 + SCREEN_HEIGHT - 20,
#                                      DASH_WIDTH, DASH_HEIGHT, [5, 0, 0])
#         arcade.draw_circle_outline(tx, ty, 15, arcade.color.GRAY)
        # for Tang in range(0, 360, 90):
        #     Tdx = sin(radians(Tang))
        #     Tdy = cos(radians(Tang))
        #     arcade.draw_line(tx + Tdx * 0.78 * radius, ty + Tdy * 0.78 * radius, tx + Tdx * 0.93 *
        #                      radius, ty + Tdy * 0.93 * radius, arcade.color.WHITE)
        #     if Tang == 0:
        #         arcade.draw_text('N',tx +Tdx*radius - 7, ty + Tdy*radius - 12, arcade.color.RED)
        #
        #     if Tang == 90:
        #         arcade.draw_text('E', tx + Tdx * radius - 7, ty + Tdy * radius - 7, arcade.color.RED)
        #     if Tang == 180:
        #         arcade.draw_text('S', tx + Tdx * radius - 6, y + Tdy * radius - 1, arcade.color.RED)
        #     if Tang == 270:
        #         arcade.draw_text('W', tx + Tdx * radius , y + Tdy * radius - 7, arcade.color.RED)
            # arcade.draw_circle_outline(x + self.radius*2 + 3, y, self.radius, arcade.color.GRAY)
            # for Sang in range(0, 360, 90):
            #     Sdx = sin(radians(Sang))
            #     Sdy = cos(radians(Sang))
            #     arcade.draw_line(x + radius*2+3 + Sdx * 0.78 * radius, y + Sdy * 0.78 * radius,
            #                      x +radius * 2+3 + Sdx * 0.93 *
            #                      radius, y + Sdy * 0.93 * radius, arcade.color.WHITE)
            #     if Sang == 90:
            #         arcade.draw_text('25', x + radius*2+3 + Sdx * radius - 7, y + Sdy * radius - 7,
            #                          arcade.color.RED)
            #     if Sang == 180:
            #         arcade.draw_text('50', x + radius * 2+ 3 +Tdx * radius - 6, y + Sdy * radius - 1, arcade.color.RED)
            #     if Sang == 270:
            #         arcade.draw_text('100', x + radius*2 + 3 + Sdx * radius, y + Sdy * radius - 7, arcade.color.RED)
            # arcade.draw_rectangle_filled(x+ radius*2, y - (radius - 5), 350,
            #                              150,
            #                              [20, 200, 50])

        # y = SCREEN_HEIGHT - radius/2
        # x = SCREEN_WIDTH - (radius*5.5)
        # for i in range(2):
        #     arcade.draw_rectangle_filled(x, y, 15, 10,
        #                                  self.color)
        #     y -= radius
        #     x += radius* 2
        # # ax = SCREEN_WIDTH - radius / 2 + 5
        # # ay = y + 5
        #
        # for a in range(2):
        #     rect = arcade.draw_rectangle_filled(SCREEN_WIDTH - radius * 4.4, y + radius + 15, 15, 10,
        #                                  self.color)
        #     y -= radius
        #




class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.max_enemy_count = 30
        self.buls = []
        self.enemy_list =[]
        self.rocks = []
        self.aircrafts = []
        self.background = Background()

        self.oil = []
        self.color = [30, 250, 50]
        self.out_color = [200, 0, 0]
        self.fuel = 8
        self.fc = 50 * (Aircraft().power * Aircraft().speed / 100)






    def setup(self):
        # Настроить игру здесь
        self.hero = Hero()
        self.enemy = Enemy()
        self.coin = Base_animation('coins')
        self.oil = []
        # self.buls.append
        # (Bulet(self.aircraft.x, self.aircraft.y, self.aircraft.ang))
        # for i in range(30):
        #     self.enemy_list.append(Enemy())
        #     self.enemy_nymber += 1
        for a in range(1):
            self.aircrafts.append(Hero())

    def draw_telemetry(self):
        arcade.draw_rectangle_filled(10 + SCREEN_WIDTH - 10, 20 + SCREEN_HEIGHT - 20,
                                    DASH_WIDTH, DASH_HEIGHT, [5, 0, 0])
        y = SCREEN_HEIGHT - radius / 2
        x = SCREEN_WIDTH - (radius * 5.5)
        for i in range(2):
            arcade.draw_rectangle_filled(x, y, 15, 10,
                                         self.color)
            y -= radius
            # x += radius* 2


        for a in range(2):
                arcade.draw_rectangle_filled(SCREEN_WIDTH - radius * 4.4, y + radius + 15, 15, 10,
                                                self.color)
                y -= radius
        while self.fuel > 0:
            self.fuel -= self.fc
            if self.fuel - self.fc == self.fuel* 3/4:
                arcade.draw_rectangle_filled(x, y, 15, 10,
                                         self.out_color)
                print(self.fc)





    # arcade.draw_circle_outline(tx, ty, 15, arcade.color.GRAY)


    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.background.draw()
        self.hero.draw()
        self.draw_telemetry()
        # self.dash.draw()


        # self.coin.draw()
        for bulet in self.buls:
            bulet.draw()

        for enemy in self.enemy_list:
            enemy.draw()


        # self.draw_telemetry()
        # for rocket in self.rocks:
        #     rocket.draw()





    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        # self.enemy.look_to(self.aircraft)
        self.hero.move()
        if random.randint(0, 1000) < 50 and len(self.enemy_list) < self.max_enemy_count:
            self.enemy_list.append(Enemy())
            for enemy in self.enemy_list:

                arcade.draw_point(350/4, 150/4, arcade.color.RED, 10)



        # self.enemy.look_to()
        for enemy in self.enemy_list:
            enemy.move()
        # self.buls.append(self.enemy.shoot())
        for bulet in self.buls:
            bulet.move()
            if bulet.should_remove():
                self.buls.remove(bulet)
                print(len(self.buls))


        # for rocket in self.rocks:
        #     rocket.move()


            for enemy in self.enemy_list:
                for bulet in self.buls:
                        if enemy.is_strike(bulet):
                                enemy.hp -= 1767
                                self.buls.remove(bulet)


                                if enemy.hp <=0:
                                    self.enemy_list.remove(enemy)
        #                 self.enemy_nymber -= 1
        #                 print(enemy.f4_hp)
        #             if self.hero.y + bulet.y > self.hero.FD:
        #                 self.buls.remove(bulet)
        #                 print(self.hero.y - bulet.y)
        #             # for rocket in self.rocks:
        #             #     if self.hero.is_strike(rocket):
        #             #         self.hero.Mig_hp = 0
        #                 if self.hero.Mig_hp == 0:
        #                     self.aircrafts.remove(self.hero)


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.hero.move_left()
        elif symbol == arcade.key.RIGHT:
            self.hero.move_right()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.hero.move_stop()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.hero.look_to(x, y)

    # self.aircraft.ang).y + 20, arcade.color.BLACK)
    # self.aircraft.look_to(self.aircraft.x - 20, self.aircraft.y)
    #     self.rocks.append(self.enemy.rock_shoot())

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.buls.append(self.hero.shoot())
        # print(len(self.rocks))

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if scroll_y < 0:
            self.hero.power_down()
        else:
            self.hero.power_up()
            # print(self.aircraft.power)
            # print(self.aircraft.gear)

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()

print(__name__)
if __name__ == "__main__":
    main()