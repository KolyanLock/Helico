from utils import randcell

UPGRADE_COST_SCALE = 100
HEAL_COST = 100

class Helicopter:
    def __init__(self, w, h):
        rc = randcell(w, h)
        rx, ry = rc[0], rc[1]
        self.w = w
        self.h = h
        self.x = rx
        self.y = ry
        self.tank = 0
        self.maxtank = 1
        self.money = 0
        self.lives = 30
        self.maxlives = 30
        self.upgrade_cost = (UPGRADE_COST_SCALE * self.maxtank + UPGRADE_COST_SCALE * self.maxlives) // 2

    def move(self, dx, dy):
        nx = dx + self.x
        ny = dy + self.y
        if self.check_bounds(nx, ny):
            self.x ,self.y = nx, ny

    def check_bounds(self, x, y):
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True

    def update_upgrade_cost(self):
        self.upgrade_cost = (UPGRADE_COST_SCALE * self.maxtank + UPGRADE_COST_SCALE * self.maxlives) // 2

    def print_stats(self):
        print('🌊 ', self.tank, '/', self.maxtank, ' 💲', self.money, ' 🛠️ ', self.upgrade_cost, '$', ' 🏥 ', HEAL_COST, '$', sep='', end=' ')
        for i in range(9, self.maxlives, 10):
            if i < self.lives:
                print('❤️', end='')
            elif i - self.lives < 4:
                print('🧡', end='')
            elif i - self.lives < 9:
                print('💛', end='')
            else:
                print('🖤', end='')
        print()

    def export_data(self):
        return{'money': self.money,
                'lives': self.lives,
                'maxlives': self.maxlives,
                'tank': self.tank,
                'maxtank': self.maxtank,
                'x': self.x, 'y': self.y}

    def import_data(self, data):
        self.x = data['x'] or 0
        self.y = data['y'] or 0
        self.money = data['money'] or 0
        self.lives = data['lives'] or 30
        self.maxlives = data['maxlives'] or 30
        self.tank = data['tank'] or 1
        self.maxtank = data['maxtank'] or 1