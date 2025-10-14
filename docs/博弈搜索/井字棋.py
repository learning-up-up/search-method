# 对于井字棋游戏进行模拟实现

from alpha_beta_searh import Node, Tree
import numpy as np
class Map(Node):
    def __init__(self):
        super().__init__()
        self.map = np.zeros((3, 3), dtype = int)

    def expand(self) -> list["Node"]:
        children = []
        for i in range(3):
            for j in range(3):
                if self.map[i][j] == 0:
                    child = Map()
                    child.map = self.map.copy()
                    if self.catgory == "max":
                        child.map[i][j] = 1
                    else:
                        child.map[i][j] = -1
                    children.append(child)
        return children

    def evaluate(self) -> int:
        for i in range(3):
            if sum(self.map[i, :]) == 3 or sum(self.map[:, i]) == 3:
                return 1  # max 赢
            if sum(self.map[i, :]) == -3 or sum(self.map[:, i]) == -3:
                return -1  # min 赢
        
        # 检查对角线
        diag1 = sum(self.map[i, i] for i in range(3))
        diag2 = sum(self.map[i, 2 - i] for i in range(3))
        if diag1 == 3 or diag2 == 3:
            return 1  # max 赢
        if diag1 == -3 or diag2 == -3:
            return -1  # min 赢
        
        # 检查平局
        if np.all(self.map != 0):
            return 0  # 平局
        
        # 游戏未结束
        return 0
        
    
initial = Map()
tree = Tree(initial)
tree.search()