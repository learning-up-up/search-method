from math import sqrt, log
from abc import ABC, abstractmethod
C = 2.0
class Montecarlo_node(ABC):
    def __init__(self):
        self.visited = 0
        self.score = 0
        self.parent = None
        self.children = []
        self.is_terminal = False
        self.catgory = "max"
    
    def ucb1(self, N: int) -> float:
        if self.catgory == "max":
            return -(self.score / self.visited) + C * sqrt(log(N) / self.visited)
        return self.score / self.visited + C * sqrt(log(N) / self.visited)
    
    @abstractmethod
    def expand(self) -> list["Montecarlo_node"]:
        raise NotImplementedError("Expand method must be implemented by subclasses.")
    
    def select(self, N: int) -> "Montecarlo_node":
        if self.children == []:
            raise ValueError("No children to select from.")
        best_ucb1 = -float('inf')
        best_child = None
        
        for child in self.children:
            if child.visited == 0:
                return child
            if child.ucb1(N) > best_ucb1:
                best_ucb1 = child.ucb1(N)
                best_child = child

        return best_child

    def expand_node(self) -> None:
        self.children = self.expand()
        if len(self.children) == 0:
            self.is_terminal = True
            return
        
        for child in self.children:
            child.parent = self
    
    # 随机游走模拟出结果
    @abstractmethod
    def rollout(self) -> int:
        raise NotImplementedError("Rollout method must be implemented by subclasses.")

    def backpropagate(self, result) -> None:
        self.visited += 1
        self.score += result
        
        if self.parent is not None:
            self.parent.backpropagate(result)
        
class Montecarlo_tree:
    def __init__(self, root: Montecarlo_node):
        self.root = root
    
    def search(self, interation : int):
        for _ in range(interation):
            curr = self.root
            while curr.children != []:
                if curr.is_terminal:
                    break
                curr = curr.select(self.root.visited)
            
            if curr.visited != 0 and curr.is_terminal == False:
                curr.expand_node()
                curr = curr.select(self.root.visited)

            result = curr.rollout()

            curr.backpropagate(result)

import numpy as np
from copy import deepcopy
class Map(Montecarlo_node):
    def __init__(self):
        super().__init__()

        self.state = np.zeros((3, 3))

    def expand(self) -> list["Montecarlo_node"]:
        children = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    child = Map()
                    child.state = deepcopy(self.state)
                    if self.catgory == "max":
                        child.state[i][j] = 1
                        child.catgory = "min"
                    else:
                        child.state[i][j] = -1
                    if child.simulation() is not None:
                        child.is_terminal = True
                    children.append(child)
        return children

    def simulation(self) -> int:
        # 检查胜负
        for i in range(3):
            if sum(self.state[i, :]) == 3 or sum(self.state[:, i]) == 3:
                return 1  # max 赢
            if sum(self.state[i, :]) == -3 or sum(self.state[:, i]) == -3:
                return -1  # min 赢
        
        diag1 = sum(self.state[i, i] for i in range(3))
        diag2 = sum(self.state[i, 2 - i] for i in range(3))
        if diag1 == 3 or diag2 == 3:
            return 1  # max 赢
        if diag1 == -3 or diag2 == -3:
            return -1  # min 赢
        
        if np.all(self.state != 0):
            return 0  # 平局
        
        return None  # 游戏未结束  
      
    def rollout(self) -> int:
        curr = deepcopy(self)
        result = curr.simulation()
        while result is None:
            children = curr.expand()
            curr = np.random.choice(children)
            result = curr.simulation()
        
        return result
            
initial = Map()
# initial.map = np.array([[ -1, 0, 0],
#                         [ 0, 1, 0],
#                         [0, 0, 0]])
tree = Montecarlo_tree(initial)
a1 = Map()
a2 = Map()
a3 = Map()
a1.catgory = "min"
a2.catgory = "min"
a3.catgory = "min"
a1.parent = tree.root
a2.parent = tree.root
a3.parent = tree.root
a1.state = np.array([[ 1, 0, 0],
               [ 0, 0, 0],
               [ 0, 0, 0]])
a2.state = np.array([[ 0, 0, 0],
               [ 1, 0, 0],
               [ 0, 0, 0]])
a3.state = np.array([[ 0, 0, 0],
               [ 0, 1, 0],
               [ 0, 0, 0]])

tree.root.children = [a1, a2, a3]
tree.search(10000)

best_choice = tree.root
while True:
    best_choice = max(best_choice.children, key=lambda x: x.score)
    print(best_choice.state)
    if best_choice.children == []:
        break