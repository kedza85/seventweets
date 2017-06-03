from model import Node


class NodeRegistry:
    def __init__(self):
        self.nodes = set()

    def add(self, name, address):
        node = Node(name, address)
        self.nodes.add(node)
        return [node for node in self.nodes]

    def remove(self, name):
        for node in self.nodes:
            if node.name == name:
                self.nodes.remove(node)
                break

    def get_all(self):
        return [node for node in self.nodes]

    def contains(self, name):
        for node in self.nodes:
            if node.name == name:
                return True

        return False
