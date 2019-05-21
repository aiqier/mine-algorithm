# -*- coding: utf-8 -*-
# 蚁群算法
import random
class Ant(object):
    """
    蚂蚁
    """
    # 上
    UP = 0
    # 左
    LEFT = 1
    # 下
    DOWN = 2
    # 右
    RIGHT = 3
    # 信息素类型:
    HOME_SMELL = 0
    FOOD_SMELL = 1
    # 最大信息素
    MAX_SMELL = 15000
    # 最大记忆
    MAX_MEMORY = 100
    # 视野
    VISION = 6
    # 信息素释放率
    SMELL_LEAVE_RATE = 0.05
    def __init__(self, map):
        """
        :param map: 地图
        :param dir: 方向
        """
        self.__map = map
        self.__map.add_ant(self)
        self.__dir = random.choice([Ant.UP, Ant.LEFT, Ant.DOWN, Ant.RIGHT])
        self.__memory = []
        self.__food = False
        self.x, self.y = self.__map.get_home_coor()
        self.__smell_home = Ant.MAX_SMELL
        self.__smell_food = 0
        self.__speed = random.choice([1, 2, 3])
        self.time = 0
    def initial_home(self):
        self.__memory = []
        self.__food = False
        self.__smell_home = Ant.MAX_SMELL
        self.__smell_food = 0
        self.__dir = self.go_back()
    def initial_food(self):
        self.__memory = []
        self.__food = True
        self.__smell_home = 0
        self.__smell_food = Ant.MAX_SMELL
        self.__dir = self.go_back()
    def show_home_smell(self):
        """
        所剩的家信息素
        :return:
        """
        return self.__smell_home
    def show_food_smell(self):
        """
        所剩的食物信息素
        :return:
        """
        return self.__smell_food
    def move(self, dir):
        """
        移动到x, y
        :param x:
        :param y:
        :return:
        """
        self.__dir = dir
        self.x, self.y = self.calcu_dire_coor(dir)
        # print "ant %s : go to (%s, %s)" % (id(self), self.x, self.y)
        if len(self.__memory) >= self.MAX_MEMORY:
            self.__memory.pop(0)
        self.__memory.append((self.x, self.y))
    def can_go_dires(self):
        """
        根据当前方向，计算出前，左，右，三个方向中可达的方向
        :return:
        """
        cango_dirs = []
        dirs = None
        assert self.__dir in [Ant.UP, Ant.DOWN, Ant.LEFT, Ant.RIGHT]
        if self.__dir == Ant.UP:
            dirs = (Ant.UP, Ant.LEFT, Ant.RIGHT)
        elif self.__dir == Ant.LEFT:
            dirs = (Ant.LEFT, Ant.DOWN, Ant.UP)
        elif self.__dir == Ant.DOWN:
            dirs = (Ant.DOWN, Ant.RIGHT, Ant.LEFT)
        elif self.__dir == Ant.RIGHT:
            dirs = (Ant.RIGHT, Ant.UP, Ant.DOWN)
        for dir in dirs:
            x, y = self.calcu_dire_coor(dir)
            if self.__map.can_go(x, y):
                cango_dirs.append(dir)
        return cango_dirs
    def calcu_vision(self, dir):
        """
        计算此方向的视野
        :return:
        """
        coors = []
        if dir == Ant.UP:
            for i in range(self.x - Ant.VISION, self.x + Ant.VISION + 1):
                for j in range(self.y - Ant.VISION, self.y + 1):
                    coors.append((i, j))
        elif dir == Ant.LEFT:
            for i in range(self.x - Ant.VISION, self.x + 1):
                for j in range(self.y - Ant.VISION, self. y + 3 + 1):
                    coors.append((i, j))
        elif dir == Ant.DOWN:
            for i in range(self.x - Ant.VISION, self.x + Ant.VISION + 1):
                for j in range(self.y, self.y + Ant.VISION + 1):
                    coors.append((i, j))
        elif dir == Ant.RIGHT:
            for i in range(self.x, self.x + Ant.VISION + 1):
                for j in range(self.y - Ant.VISION, self.y + Ant.VISION + 1):
                    coors.append((i, j))
        return coors
    def turn_left(self):
        """
        按照当前方向的逆时针转动
        :return:
        """
        if self.__dir == Ant.UP:
            return Ant.LEFT
        elif self.__dir == Ant.LEFT:
            return Ant.DOWN
        elif self.__dir == Ant.DOWN:
            return Ant.RIGHT
        else:
            return Ant.UP
    def turn_right(self):
        """
        按照当前方向的顺时针转动
        :return:
        """
        if self.__dir == Ant.UP:
            return Ant.RIGHT
        elif self.__dir == Ant.RIGHT:
            return Ant.DOWN
        elif self.__dir == Ant.DOWN:
            return Ant.LEFT
        else:
            return Ant.UP
    def go_back(self):
        """
        转向回头
        :return:
        """
        if self.__dir == Ant.UP:
            return Ant.DOWN
        elif self.__dir == Ant.DOWN:
            return Ant.UP
        elif self.__dir == Ant.LEFT:
            return Ant.RIGHT
        else:
            return Ant.LEFT
    def has_food(self):
        return self.__food
    def memory(self):
        """
        返回这只蚂蚁的记忆坐标
        :return:
        """
        return self.__memory
    def calcu_dire_coor(self, dir):
        """
        计算如果按照此方向移动后，将会到达的坐标
        :param dir:
        :return:
        """
        if dir == Ant.UP:
            return self.x, self.y - 1
        elif dir == Ant.DOWN:
            return self.x, self.y + 1
        elif dir == Ant.LEFT:
            return self.x - 1, self.y
        else:
            return self.x + 1, self.y
    def ramble(self, dirs):
        """
        漫游的选择一个方向
        :return:
        """
        if len(dirs) == 3:
            roll = random.randrange(1, 101)
            if 1 <= roll <= 90:
                return self.__dir
            elif 90 <= roll <= 95:
                return self.turn_left()
            else:
                return self.turn_right()
        elif len(dirs) == 2:
            if self.__dir in dirs:
                roll = random.randrange(1, 101)
                if 1 <= roll <= 90:
                    return self.__dir
                else:
                    for i in dirs:
                        if i != self.__dir:
                            return i
            else:
                roll = random.randrange(1, 101)
                if 1 <= roll <= 50:
                    return dirs[0]
                else:
                    return dirs[1]
        elif len(dirs) == 1:
            return dirs[0]
        else:
            return self.go_back()
    def calcu_next_dire(self):
        """
        计算下一步移动方向
        :return:
        """
        # 计算可达的方向
        cango_dirs = self.can_go_dires()
        max_smell = {}
        for i in cango_dirs:
            max_smell[i] = 0
        for dir in cango_dirs:
            visoins = self.calcu_vision(dir)
            if self.has_food():
                smell_type = Ant.HOME_SMELL
            else:
                smell_type = Ant.FOOD_SMELL
            max_smell[dir] = self.__map.calcu_max_smell(visoins, self.memory(), smell_type)
        # 选择信息素最大的方向
        will_dir = None
        max_s = 0
        for dir, smell in max_smell.iteritems():
            if smell > max_s:
                will_dir = dir
                max_s = smell
        # 没有则漫游
        if will_dir is not None:
            return will_dir
        else:
            return self.ramble(cango_dirs)
    def print_smell(self):
        """
        打印这只蚂蚁的信息素含量
        :return:
        """
        print "%s,家信息素%s， 食物信息素：%s" % (id(self) , self.__smell_home, self.__smell_food)
    def one_step(self):
        """
        行动一步
        :return:
        """
        self.time += 1
        if self.time < self.__speed:
            return
        self.time = 0
        dire = self.calcu_next_dire()
        self.move(dire)
        # 遇到家或者食物的时候需要执行的动作
        if self.has_food():
            if self.__map.is_home(self.x, self.y):
                self.__map.put_food_to_home()
                self.initial_home()
            elif self.__map.is_food(self.x, self.y):
                self.__smell_food = Ant.MAX_SMELL
        else:
            if self.__map.is_food(self.x, self.y) and not self.__map.food_empty():
                self.__map.take_a_food()
                self.initial_food()
            elif self.__map.is_home(self.x, self.y):
                self.__smell_home = Ant.MAX_SMELL
        # 在地图上洒下信息素
        # 不在家或者食物上撒任何信息素
        if self.has_food():
            if self.__smell_food > 0 and not self.__map.is_food(self.x, self.y) and not self.__map.is_home(self.x, self.y):
                smell = self.__smell_food * Ant.SMELL_LEAVE_RATE
                self.__smell_food -= smell
                self.__map.leave_smell(self.x, self.y,  Ant.FOOD_SMELL, smell)
        else:
            if self.__smell_home > 0 and not self.__map.is_home(self.x, self.y) and not self.__map.is_food(self.x, self.y):
                smell = self.__smell_home * Ant.SMELL_LEAVE_RATE
                self.__smell_home -= smell
                self.__map.leave_smell(self.x, self.y, Ant.HOME_SMELL, smell)
class Map(object):
    """
    地图
    """
    # 草地
    LAWN = 0
    # 障碍物
    OBSTACLE = 1
    # 家
    HOME = 2
    # 食物
    FOOD = 3
    # 蚂蚁
    ANT = 4
    # 信息素消失速度
    SMELL_GONE_SPEED = 50
    # 信息素消失比率
    SMELL_GONE_RATE = 0.05
    # 障碍物数量
    OBSTACLE_COUNT = 30
    # 草地
    P_LAWN = " "
    # 石头
    P_OBSTACLE = "@"
    # 蚁巢
    P_HOME = "#"
    # 奶酪
    P_FOOD = "$"
    # 蚂蚁
    P_ANT = "*"
    def __init__(self, x, y, food_counts):
        """
        :param x:
        :param y:
        """
        self.__data = []
        for i in range(x):
            temp = []
            for j in range(y):
                temp.append(Map.LAWN)
            self.__data.append(temp)
        self.__data[0][0] = Map.HOME
        self.__data[x-1][y-1] = Map.FOOD
        # 家在左上角
        self.__home_coor = (0, 0)
        # 食物在右下角
        self.__food_coor = (x-1, y-1)
        # 放几个障碍物
        for i in range(Map.OBSTACLE_COUNT):
            x1 = random.choice(range(x))
            y1 = random.choice(range(y))
            if self.is_home(x1, y1) or self.is_food(x1, y1):
                continue
            self.__data[x1][y1] = Map.OBSTACLE
        self.__ants = []
        self.__home_food = 0
        self.__food_foods = food_counts
        # 初始化每个草地的默认信息素值
        self.__smells = {}
        for x, i in enumerate(self.__data):
            for y, j in enumerate(i):
                if j == Map.LAWN:
                    self.__smells[(x, y)] = {Ant.HOME_SMELL: 0, Ant.FOOD_SMELL: 0}
        self.X = x
        self.Y = y
        self.time = 0
    def landform(self):
        return self.__data
    def get_food_count(self):
        """
        获得地图上，家和食物所包含的食物个数
        :return:
        """
        return self.__home_food, self.__food_foods
    def food_empty(self):
        return self.__food_foods <= 0
    def take_a_food(self):
        """
        拿走一个食物
        :return:
        """
        self.__food_foods -= 1
    def put_food_to_home(self):
        """
        向家中放一个食物
        :return:
        """
        self.__home_food += 1
    def can_go(self, x, y):
        """
        判断这个坐标是否可达
        :param x:
        :param y:
        :return:
        """
        if 0 <= x <= self.X and 0 <= y <= self.Y and not self.is_obstacle(x, y):
            return True
        return False
    def is_obstacle(self, x, y):
        """
        判断一个坐标是否为障碍物
        :param x:
        :param y:
        :return:
        """
        return self.__data[x][y] == Map.OBSTACLE
    def is_home(self, x, y):
        """
        坐标是否为家
        :param x:
        :param y:
        :return:
        """
        return self.__data[x][y] == Map.HOME
    def get_home_coor(self):
        """
        获得家的坐标
        :return:
        """
        return self.__home_coor
    def get_food_coor(self):
        """
        获得食物的坐标
        :return:
        """
        return self.__food_coor
    def is_food(self, x, y):
        """
        坐标是否为食物
        :param x:
        :param y:
        :return:
        """
        return self.__data[x][y] == Map.FOOD
    def calcu_max_smell(self, coors, memory, smell_type):
        """
        计算一个坐标范围内的最大信息素
        :return:
        """
        smell = 0
        for coor in coors:
            x, y = coor
            if not self.can_go(x, y):
                continue
            if smell_type == Ant.FOOD_SMELL and self.is_food(x, y):
                smell = Ant.MAX_SMELL
                break
            if smell_type == Ant.HOME_SMELL and self.is_home(x, y):
                smell = Ant.MAX_SMELL
                break
            if (x, y) in memory:
                continue
            if self.is_food(x, y) or self.is_home(x, y):
                continue
            if smell_type == Ant.FOOD_SMELL:
                if self.__smells[(x, y)][Ant.FOOD_SMELL] > smell:
                    smell = self.__smells[(x, y)][Ant.FOOD_SMELL]
            if smell_type == Ant.HOME_SMELL:
                if self.__smells[(x, y)][Ant.HOME_SMELL] > smell:
                    smell = self.__smells[(x, y)][Ant.HOME_SMELL]
        return smell
    def leave_smell(self, x, y, smell_type, n):
        """
        在坐标x，y上留下信息素
        :return:
        """
        if self.__smells[(x, y)][smell_type] < n:
            self.__smells[(x, y)][smell_type] = n
    def wastage(self):
        """
        信息素随着时间，不断的流逝
        :return:
        """
        self.time += 1
        if self.time > Map.SMELL_GONE_SPEED:
            self.time = 0
            for k, v in self.__smells.iteritems():
                if v[Ant.HOME_SMELL] > 0:
                    v[Ant.HOME_SMELL] -= 1 + (v[Ant.HOME_SMELL] * Map.SMELL_GONE_RATE)
                if v[Ant.HOME_SMELL] < 0:
                    v[Ant.HOME_SMELL] = 0
                if v[Ant.FOOD_SMELL] > 0:
                    v[Ant.FOOD_SMELL] -= 1 + (v[Ant.FOOD_SMELL] * Map.SMELL_GONE_RATE)
                if v[Ant.FOOD_SMELL] < 0:
                    v[Ant.FOOD_SMELL] = 0
    def add_ant(self, ant):
        """
        在地图上添加一直蚂蚁
        :param ant:
        :return:
        """
        self.__ants.append(ant)
    def get_ants(self):
        """
        获得所有蚂蚁
        :return:
        """
        return self.__ants
    def get_ants_coors(self):
        """
        获得地图中每一只蚂蚁的坐标
        :return:
        """
        return [(ant.x, ant.y) for ant in self.__ants]
    def show_ant(self):
        for r, item in enumerate(self.__data):
            row = []
            for c, i in enumerate(item):
                if i == Map.LAWN:
                    number = 0
                    for ant in self.__ants:
                        if ant.x == r and ant.y == c:
                            number += 1
                    if number == 0:
                        row.append(Map.P_LAWN)
                    else:
                        row.append(str(number))
                elif i == Map.OBSTACLE:
                    row.append(Map.P_OBSTACLE)
                elif i == Map.HOME:
                    row.append(str(self.__home_food))
                elif i == Map.FOOD:
                    row.append(str(self.__food_foods))
            print "[%s]" % ("".join(row),)
    def show_smell(self, smell_type):
        """
        展示地图上家的信息素分布
        :return:
        """
        for r, item in enumerate(self.__data):
            row = []
            for c, i in enumerate(item):
                if i == Map.LAWN:
                    number = 0
                    if (r, c) in self.__smells:
                        number = self.__smells[(r, c)][smell_type]
                    if number == 0:
                        row.append(Map.P_LAWN)
                    else:
                        row.append(str(number))
                elif i == Map.OBSTACLE:
                    row.append(Map.P_OBSTACLE)
                elif i == Map.HOME:
                    row.append(Map.P_HOME)
                elif i == Map.FOOD:
                    row.append(Map.P_FOOD)
            print "[%s]" % ("".join(row),)
    def get_smells(self):
        """
        获得地图上家和食物的信息素分布
        :return:
        """
        return self.__smells
    def print_smell(self, smell_type):
        """
        打印smell
        :return:
        """
        for k, item in self.__smells.iteritems():
            print k, item[smell_type]
    def change(self):
        """
        世界发生一次变化
        :param map:
        :param ants:
        :return:
        """
        for ant in self.get_ants():
            ant.one_step()
        self.wastage()
    def snapshot(self):
        """
        快照
        :return:
        """
        return self.landform(), self.get_ants(), self.get_food_count(), self.get_smells()
class World(object):
    def __init__(self, x, y , ant_counts, food_counts):
        self.__map = Map(x, y, food_counts)
        for i in range(ant_counts):
            ant = Ant(self.__map)
    def run(self):
        while True:
            self.__map.change()
            yield self.__map.snapshot()
