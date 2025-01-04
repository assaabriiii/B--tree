class Node:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
        self.next_leaf = None
        self.parent = None

class BPlusTree:
    def __init__(self, degree):
        self.root = Node(is_leaf=True)
        self.degree = degree

    def search(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while i < len(current_node.keys) and key > current_node.keys[i]:
                i += 1
            current_node = current_node.children[i]

        if key in current_node.keys:
            return True
        return False

    def find_leaf(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while i < len(current_node.keys) and key > current_node.keys[i]:
                i += 1
            current_node = current_node.children[i]
        return current_node

    def insert_into_leaf(self, leaf, key):
        if key not in leaf.keys:
            leaf.keys.append(key)
            leaf.keys.sort()

    def split_node(self, node):
        mid_index = len(node.keys) // 2
        mid_key = node.keys[mid_index]

        new_node = Node(is_leaf=node.is_leaf)
        new_node.keys = node.keys[mid_index + 1:]
        node.keys = node.keys[:mid_index]

        if not node.is_leaf:
            new_node.children = node.children[mid_index + 1:]
            node.children = node.children[:mid_index + 1]

        for child in new_node.children:
            child.parent = new_node

        return mid_key, new_node

    def insert_into_parent(self, node, mid_key, new_node):
        if node == self.root:
            new_root = Node(is_leaf=False)
            new_root.keys = [mid_key]
            new_root.children = [node, new_node]
            node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
            return

        parent = node.parent
        insert_index = parent.children.index(node)
        parent.keys.insert(insert_index, mid_key)
        parent.children.insert(insert_index + 1, new_node)
        new_node.parent = parent

        if len(parent.keys) >= self.degree:
            mid_key, new_node = self.split_node(parent)
            self.insert_into_parent(parent, mid_key, new_node)

    def insert(self, key):
        leaf = self.find_leaf(key)
        self.insert_into_leaf(leaf, key)

        if len(leaf.keys) >= self.degree:
            mid_key, new_node = self.split_node(leaf)
            self.insert_into_parent(leaf, mid_key, new_node)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("Level", level, ":", node.keys)
        if not node.is_leaf:
            for child in node.children:
                self.print_tree(child, level + 1)
    
    def getDictTree(self):
        if self.root == None:
            return {'root': {}}
        return {'root': self.root.getDict()}

    def delete(self, key):
        pass


if __name__ == "__main__":
    bpt = BPlusTree(3)
    for i in range(1, 10):
        bpt.insert(i)
    bpt.print_tree()
    print(bpt.search(5))
    print(bpt.search(10))
    print(bpt.search(3))
    print(bpt.search(7))
    print(bpt.search(1))
    print(bpt.search(9))
    print(bpt.search(12))
    print(bpt.print_tree())

