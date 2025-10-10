import numpy as np

class Point:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        if parent is None:
            self.g = 0
        else:
            self.g = parent.g + 1
   
class Map:
    def __init__(self, length, width, begin, target):
        self.length = length
        self.width = width
        self.info = np.ones((self.length, self.width), dtype=int)
        self.begin = begin
        self.target = target
        
        # 1是路，0是墙
    
    def set_wall(self, x, y):
        self.info[x, y] = 0
    
def h(x, y, target):
        return abs(x - target[0]) + abs(y - target[1])
    
def search(map):
    begin = Point(None, map.begin[0], map.begin[1])
    group = [begin]
    # W为启发式函数的权重，对于W>1的情况，启发式函数会被放大，搜索速度更快，但可能不最优
    w = 10
    # 搜索次数
    search_count = 0
    while search_count < 10000:
        search_count += 1
        group.sort(key = lambda point: point.g + w * h(point.x, point.y, map.target))
        point = group.pop(0)
        if (point.x, point.y) == map.target:
            print(search_count)
            return point
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x = point.x + dx
            new_y = point.y + dy
            if 0 <= new_x < map.length and 0 <= new_y < map.width and map.info[new_x, new_y] == 1:
                group.append(Point(point, new_x, new_y))

    print("Search failed")
    
    return None

# 输出路线
map = Map(10, 10, (2, 0), (2, 9))
map.set_wall(0, 1)
map.set_wall(1, 1)
map.set_wall(2, 1)
map.set_wall(5, 1)
map.set_wall(6, 1)
map.set_wall(7, 1)
map.set_wall(3, 3)
map.set_wall(4, 3)
map.set_wall(5, 3)
map.set_wall(8, 3)
map.set_wall(1, 4)
map.set_wall(8, 4)
map.set_wall(1, 5)
map.set_wall(4, 5)
map.set_wall(5, 5)
map.set_wall(6, 5)
map.set_wall(5, 7)
map.set_wall(7, 7)
map.set_wall(1, 8)
map.set_wall(2, 8)
map.set_wall(3, 8)
map.set_wall(7, 8)

end = search(map)
path = []
while end:
    path.append((end.x, end.y))
    end = end.parent
path.reverse()
if path:
    print(path)
