from clouds import Clouds
from utils import randbool, randcell, randcell2
from helicopter import HEAL_COST, Helicopter as Helico

# 0 - поле
# 1 - дерево
# 2 - река
# 3 - госпиталь
# 4 - апгрейд-шоп
# 5 - огонь

TREE_COST = 100
MAXTANK_LIMIT = 10
MAXLIVES_LIMIT = 10

class Map(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.clouds = Clouds(w, h)
        self.helico = Helico(w, h)
        self.check_helico()
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(3, 10)
        self.generate_river(10, 3)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True

    def check_helico(self):
        while self.clouds.cells[self.helico.x][self.helico.y] != 0:
            rc = randcell(self.w, self.h)
            rx, ry = rc[0], rc[1]
            self.helico.x, self.helico.y = rx, ry

    def pritn_map(self):
        print('🔳' * (self.w + 2))
        for ri in range(self.h):
            print('🔳', end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if self.clouds.cells[ri][ci] == 1:
                    print('☁️', end='')
                elif self.clouds.cells[ri][ci] == 2:
                    print('⛈️', end='')
                elif self.helico.x == ri and self.helico.y == ci:
                    print('🚁', end='')
                elif cell == 0:
                    print('🟩', end='')
                elif cell == 1:
                    print('🌲', end='')
                elif cell == 2:
                    print('🌊', end='')
                elif cell == 3:
                    print('🏥', end='')
                elif cell == 4:
                    print('🛠️', end='')
                elif cell == 5:
                    print('🔥', end='')
            print('🔳')
        print('🔳' * (self.w + 2))

    def generate_river(self, l, count):
        for i in range(count):
            rc = randcell(self.w, self.h)
            rx, ry = rc[0], rc[1]
            self.cells[rx][ry] = 2
            lantgh = l
            while lantgh > 0:
                rc2 = randcell2(rx, ry)
                rx2, ry2 = rc2[0], rc2[1]
                if self.check_bounds(rx2, ry2):
                    self.cells[rx2][ry2] = 2
                    rx, ry = rx2, ry2
                    lantgh -= 1
    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1
    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 0:
            self.cells[cx][cy] = 1
    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 0 or self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 4
        else:
            self.generate_upgrade_shop()
    def generate_hospital(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 0 or self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.check_bounds(cx, cy) and self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5
    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        for i in range(5):
            self.add_fire()

    def process_helicopter(self):
        c = self.cells[self.helico.x][self.helico.y]
        d = self.clouds.cells[self.helico.x][self.helico.y]
        if d ==2:
            self.helico.lives -= 1
        if c == 2:
            self.helico.tank = self.helico.maxtank
        elif c == 3 and self.helico.money >= HEAL_COST and self.helico.lives < self.helico.maxlives:
            self.helico.money -= HEAL_COST
            self.helico.lives += 10
            if self.helico.lives > self.helico.maxlives:
                self.helico.lives = self.helico.maxlives
        elif c == 4 and self.helico.money >= self.helico.upgrade_cost and self.helico.maxtank < MAXTANK_LIMIT and self.helico.maxlives < MAXLIVES_LIMIT:
            self.helico.money -= self.helico.upgrade_cost
            if self.helico.maxtank < MAXTANK_LIMIT:
                self.helico.maxtank += 1
            if (self.helico.maxtank > self.helico.maxlives or self.helico.maxtank == MAXTANK_LIMIT) and (self.helico.maxlives < MAXLIVES_LIMIT):
                self.helico.maxlives +=10
            self.helico.update_upgrade_cost()
        elif c == 5 and self.helico.tank > 0:
            self.helico.tank -= 1
            self.cells[self.helico.x][self.helico.y] = 1
            self.helico.money += TREE_COST

    def export_data(self):
        return {'cells': self.cells}

    def import_data(self, data):
        self.cells = data['cells']
