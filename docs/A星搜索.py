import numpy as np
import matplotlib.pyplot as plt

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
        self.info = np.zeros((self.length, self.width), dtype = float)
        self.begin = begin
        self.target = target
        
        # 0是路，-1是墙
    
    def set_wall(self, x, y):
        self.info[x, y] = -1
    
def h(x, y, target):
        return abs(x - target[0]) + abs(y - target[1])

def draw_map(map, path = None):
    plt.figure(figsize = (map.length, map.width))
    plt.imshow(map.info, cmap = 'gray_r')
    plt.grid(color = 'black', linestyle = '-', linewidth = 0.5)  # 添加网格线
    plt.xticks(np.arange(-0.5, map.width, 1), [])  # 设置 x 轴网格
    plt.yticks(np.arange(-0.5, map.length, 1), [])  # 设置 y 轴网格
    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_y, path_x, color = 'red')
    plt.scatter(map.begin[1], map.begin[0], color = 'blue', s = 100, label = 'Start')
    plt.scatter(map.target[1], map.target[0], color = 'green', s = 100, label = 'Target')
    plt.legend()
    plt.show()  
  
def search(map):
    begin = Point(None, map.begin[0], map.begin[1])
    group = [begin]
    # W为启发式函数的权重，对于W>1的情况，启发式函数会被放大，搜索速度更快，但可能不最优
    w = 1 # w 可以调整为大于1的值来减少搜索次数
    # 搜索次数
    search_count = 0
    while search_count < 10000:
        search_count += 1
        group.sort(key = lambda point: point.g + w * h(point.x, point.y, map.target))
        point = group.pop(0)
        if (point.x, point.y) == map.target:
            print(search_count)
            path = []
            while point:
                path.append((point.x, point.y))
                point = point.parent
            path.reverse()
            print(path)
            map.info[map.info == -1] = np.max(map.info) + 10
            map.info = map.info / np.max(map.info)
                
            draw_map(map, path)
            return
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x = point.x + dx
            new_y = point.y + dy
            if 0 <= new_x < map.length and 0 <= new_y < map.width and map.info[new_x, new_y] >= 0 and ((new_x, new_y) != (point.parent.x, point.parent.y) if point.parent else True):
                map.info[new_x, new_y] += 3
                group.append(Point(point, new_x, new_y))

    print("Search failed")
    
    return None

# 输出路线
map = Map(10, 10, (2, 0), (5, 9))
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
map.set_wall(6, 7)
map.set_wall(7, 7)
map.set_wall(1, 8)
map.set_wall(2, 8)
map.set_wall(3, 8)
map.set_wall(7, 8)


search(map)
