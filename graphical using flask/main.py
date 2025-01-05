class Node:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
        self.next_leaf = None
        self.parent = None

    def getDict(self):
        if self.is_leaf:
            return {'keys': self.keys, 'children': [], 'is_leaf': True}
        return {'keys': self.keys, 'children': [n.getDict() for n in self.children], 'is_leaf': False}

    def __repr__(self):
        return f"Node({self.keys})"


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

        return key in current_node.keys




    def _search(self, key):
        if key == None or self.root == None:
            return None
        current_node = self._find_leaf(key)
        for i, k in enumerate(current_node.keys):
            if k == key:
                return (current_node, i)
        return None

    def test_find(self, key):
        return self.__find_leaf(key)

    def _find_leaf(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while i < len(current_node.keys) and key >= current_node.keys[i]:
                i+=1
            current_node = current_node.children[i]
        return current_node



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

        if node.is_leaf:
            new_node.next_leaf = node.next_leaf
            node.next_leaf = new_node

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
        print(f"INSERTED {key}")
        leaf = self.find_leaf(key)
        self.insert_into_leaf(leaf, key)

        if len(leaf.keys) >= self.degree:
            mid_key, new_node = self.split_node(leaf)
            self.insert_into_parent(leaf, mid_key, new_node)


    def print_tree(self, debugLeaves = False, showPointers = False):
        if self.root == None:
            print("Empty Tree")
            return
        nodes = [(0, self.root)]
        leaves = []
        print("=====[Tree]=====")
        last_level = 0
        while len(nodes) != 0:
            (level, node) = nodes.pop(0)
            if last_level != level:
                print()
            if not(showPointers):
                print(node.keys,end=' ')
            else:
                print(node, node.pointers, end=' ')
            if not(node.is_leaf):
                nodes += [(level+1, node.children[i]) for i in range(len(node.children))]
            else:
                leaves += node.children
            last_level = level


    def getDictTree(self):
        if self.root is None:
            return {'root': {}}
        return {'root': self.root.getDict()}

    def delete(self, key):
        leaf = self.find_leaf(key)
        if key not in leaf.keys:
            print(f"Key {key} not found in tree")
            return
        leaf.keys.remove(key)
        if len(leaf.keys) < (self.degree - 1) // 2:
            self.rebalance_after_deletion(leaf)

    def rebalance_after_deletion(self, node):
        if node == self.root and len(node.keys) == 0:
            if not node.is_leaf:
                self.root = node.children[0]
                self.root.parent = None
            else:
                self.root = Node(is_leaf=True)
            return

        parent = node.parent
        if parent is None:
            return

        index = parent.children.index(node)

        if index > 0:
            left_sibling = parent.children[index - 1]
            if len(left_sibling.keys) > (self.degree - 1) // 2:
                borrowed_key = left_sibling.keys.pop(-1)
                if not node.is_leaf:
                    borrowed_child = left_sibling.children.pop(-1)
                    node.children.insert(0, borrowed_child)
                    borrowed_child.parent = node
                parent.keys[index - 1] = borrowed_key
                node.keys.insert(0, borrowed_key)
                return

        if index < len(parent.children) - 1:
            right_sibling = parent.children[index + 1]
            if len(right_sibling.keys) > (self.degree - 1) // 2:
                borrowed_key = right_sibling.keys.pop(0)
                if not node.is_leaf:
                    borrowed_child = right_sibling.children.pop(0)
                    node.children.append(borrowed_child)
                    borrowed_child.parent = node
                parent.keys[index] = right_sibling.keys[0]
                node.keys.append(borrowed_key)
                return

        if index > 0:
            left_sibling = parent.children[index - 1]
            merge_key = parent.keys.pop(index - 1)
            parent.children.pop(index)
            left_sibling.keys.append(merge_key)
            left_sibling.keys.extend(node.keys)

            if not node.is_leaf:
                left_sibling.children.extend(node.children)
                for child in node.children:
                    child.parent = left_sibling

            if parent == self.root and len(parent.keys) == 0:
                self.root = left_sibling
                self.root.parent = None
            else:
                self.rebalance_after_deletion(parent)

        else:
            right_sibling = parent.children[index + 1]
            merge_key = parent.keys.pop(index)
            parent.children.pop(index)
            node.keys.append(merge_key)
            node.keys.extend(right_sibling.keys)

            if not node.is_leaf:
                node.children.extend(right_sibling.children)
                for child in right_sibling.children:
                    child.parent = node

            if parent == self.root and len(parent.keys) == 0:
                self.root = node
                self.root.parent = None
            else:
                self.rebalance_after_deletion(parent)


if __name__ == "__main__":
    bpt = BPlusTree(3)
    bpt.insert(5)
    print(bpt.print_tree())
    bpt.insert(2)
    print(bpt.print_tree())
    bpt.insert(4)
    print(bpt.print_tree())
    bpt.insert(12)
    bpt.insert(13)
    bpt.insert(14)
    bpt.insert(15)
    bpt.insert(16)
    bpt.insert(17)
    bpt.insert(18)
    print(bpt.print_tree())
    getDictTree = bpt.getDictTree()
    print(getDictTree)
