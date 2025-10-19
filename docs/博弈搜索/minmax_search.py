# 最原始的博弈树实现，节点与树的进一步实现需要自行完成

from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self):
        self.value : int = None
        self.parent: Node = None
        self.children = []
        self.is_terminal = False
        self.catgory = "max"

    @abstractmethod
    def expand(self) -> list["Node"]:
        raise NotImplementedError("Expand method must be implemented by subclasses.")

    @abstractmethod
    def evaluate(self) -> int:
        raise NotImplementedError("Evaluate method must be implemented by subclasses.")
    
    def expand_node(self) -> None:
        self.children = self.expand()
        if len(self.children) == 0 or (self.value() != 0 if self.value is not None else False):
            self.is_terminal = True
            return
        
        for child in self.children:
            child.parent = self
        if self.catgory == "max":
            for child in self.children:
                child.catgory = "min"

class Tree(ABC):
    def __init__(self, root : Node):
        self.root = root

    # def search(self) -> None:
    #     node_queue = [self.root]
    #     num = 0
    #     while len(node_queue) > 0:
    #         curr = node_queue.pop(0)
    #         num += 1

    #         curr.expand_node()
    #         node_queue = node_queue + curr.children
    #         if curr.is_terminal:
    #             curr.value = curr.evaluate()
        
    #     # 反向赋值
    #     def backpropagate(node: Node) -> None:
    #         if node.is_terminal:
    #             return
    #         for child in node.children:
    #             backpropagate(child)
            
    #         if node.catgory == "max":
    #             node.value = max([child.value for child in node.children])
    #         else:
    #             node.value = min([child.value for child in node.children])

    #     backpropagate(self.root)
    #     print(f"best value: {self.root.value}")
    #     print(f"num of nodes: {num}")
    # 上方的做法极其不便利

    def search(self) -> None:
        num1 = 0
        def backpropagate(node: Node,) -> None:
            nonlocal num1
            num1 += 1
            node.expand_node()
            
            if node.is_terminal:
                node.value = node.evaluate()
                return
            for child in node.children:
                backpropagate(child)
            
            if node.catgory == "max":
                node.value = max([child.value for child in node.children])
            else:
                node.value = min([child.value for child in node.children])

        backpropagate(self.root)
        print(f"best value: {self.root.value}")
        print(f"searched nodes: {num1}")
            
    def alpha_beta_search(self) -> None:
        searched_nodes = 0

        def alpha_beta(node: Node, alpha: float, beta: float) -> float:
            nonlocal searched_nodes
            searched_nodes += 1
            node.expand_node()
            if node.is_terminal:
                node.value = node.evaluate()
                return node.value

            if node.catgory == "max":
                value = float('-inf')
                for child in node.children:
                    value = max(value, alpha_beta(child, alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                node.value = value
                return value

            else:
                value = float('inf')
                for child in node.children:
                    value = min(value, alpha_beta(child, alpha, beta))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                node.value = value
                return value

        best_value = alpha_beta(self.root, float('-inf'), float('inf'))

        print(f"best value: {best_value}")
        print(f"searched nodes: {searched_nodes}")                
            
        


    