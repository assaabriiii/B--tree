import math

class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

    def get_dict(self):
        if self.is_leaf:
            return {'keys': self.keys, 'children': [], 'is_leaf': True}
        return {'keys': self.keys, 'children': [child.get_dict() for child in self.children], 'is_leaf': False}

    def __repr__(self):
        return f"Node({self.keys})"


class BPlusTree:
    def __init__(self, degree):
        self.root = Node(is_leaf=True)
        self.degree = degree

    def search(self, key):
        if key == None or self.root == None:
            return None
        current_node = self._find_leaf(key)
        for i,j in enumerate(current_node.keys):
            if j == key:
                return (current_node, i)
        return None

    def _find_leaf(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while i < len(current_node.keys) and key >= current_node.keys[i]:
                i += 1
            current_node = current_node.children[i]
        return current_node

    def insert(self, key, child):
        if key == None or child == None:
            return
        leaf = None
        
        if self.root == None:
            self.root = Node(is_leaf=True)
            leaf = self.root

        else:
            leaf = self._find_leaf(key)

        if len(leaf.keys) < self.degree - 1:
            self._insert_in_leaf(leaf, key, child)

        else:
            leaf_temp = Node(is_leaf=True)
            temp = self._get_copy_temp(leaf)
            self._insert_in_leaf(temp, key, child)

            if(leaf.children[-1] is Node):
                leaf_temp.children.append(leaf.children[-1])

            leaf.children = [leaf_temp]
            leaf.keys.clear()

            border = int(math.ceil(self.degree/2))

            leaf.keys = temp.keys[:border]
            leaf.children = temp.children[:border] + leaf.children

            leaf_temp.keys = temp.keys[border:]
            leaf_temp.children += temp.children[border:]

            kite = leaf_temp.keys[0]
            self._insert_in_parent(leaf, kite, leaf_temp)

    def _get_copy_temp(self, node, full=False):
        temp = Node(is_leaf=node.is_leaf)
        check = 0 if full else 1
        if self._is_right_edge(node):
            check = 0
        temp.keys = node.keys[check:]
        temp.children = node.children[:len(node.children)-check]
        return temp

    def _insert_in_leaf(self, leaf, key, child):
        if leaf == self.root and len(leaf.keys) == 0:
            leaf.keys = [key]
            leaf.children = [child]
            return
        
        if key < leaf.keys[0]:
            leaf.keys.insert(0, key)
            leaf.children.insert(0, child)

        else:
            self._add_key_child(leaf, key, child)

    def _insert_in_parent(self, node, kite, node_temp):
        if node == self.root:
            node_right = Node()
            node_right.keys = [kite]
            node_right.children = [node, node_temp]
            self.root = node_right
            return

        node_parent = self.parent(node)

        if len(node_parent.children) < self.degree:
            index = node_parent.children.index(node)
            node_parent.children.insert(index+1, node_temp)
            node_parent.keys.insert(index, kite)

        else:
            temp = self._get_copy_temp(node_parent, full=True)
            index = temp.children.index(node)
            temp.children.insert(index+1, node_temp)
            temp.keys.insert(index, kite)
            node_parent.keys.clear()
            node_parent.children.clear()
            node_parent_temp = Node()
            border = int(math.ceil((self.degree+1)/2))
            node_parent.keys = temp.keys[:border-1]
            node_parent.children = temp.children[:border]
            kite_temp = temp.keys[border-1]
            node_parent_temp.children = temp.children[border:]
            self._insert_in_parent(node_parent, kite_temp, node_parent_temp)

    def _add_key_child(self, node, key, child):
        i = 0
        while i < len(node.keys):
            if node.keys[i] > key:
                node.keys.insert(i, key)
                node.children.insert(i, child)
                return i
            i += 1
            node.keys.append(key)
            node.children.append(child)
            return i

    def _is_right_edge(self, node):
        current = self.root
        while not(current.is_leaf):
            current = current.children[-1]
        return current == node


    def parent(self, node):
        if self.root == node:
            return None
        return self._find_parent(self.root, node)

    def _find_parent(self, current_node, child_node):
        if current_node.is_leaf:
            return None
        for child in current_node.children:
            if child == child_node:
                return current_node
            parent = self._find_parent(child, child_node)
            if parent:
                return parent
        return None
    
    # BUG: Defintly not working as expected
    def get_dict(self):
        if self.root == None:
            return {'root': {}}
        return {'root': self.root.get_dict()}

    def print_tree(self):
        if self.root == None:
            return
        self._print_tree(self.root)

    def _print_tree(self, node, indent=0):
        print(' ' * indent, node.keys)
        if not node.is_leaf:
            for child in node.children:
                self._print_tree(child, indent + 2)

    def __str__(self):
        pass

    def get_level_size(self):
        pass

    def get_sibling(self):
        pass

    def find_key(self):
        pass

    def is_predecessor(self):
        pass

    def _delete_entry(self):
        pass

    def _add_only_key(self):
        pass

    def _merge_leaf_nodes(self):
        pass

    def _merge(self):
        pass

    def delete(self):
        pass


if __name__ == "__main__":
    bpt = BPlusTree(4)
    bpt.insert(1, 1)
    bpt.insert(2, 2)
    bpt.insert(3, 3)
    bpt.insert(4, 4)
    bpt.insert(5, 5)
    bpt.insert(6, 6)
    bpt.insert(7, 7)
    bpt.insert(9, 9)
    bpt.insert(8, 8)
    bpt.insert(10, 10)
    bpt.insert(11, 11)
    bpt.insert(12, 12)
    bpt.insert(13, 13)
    bpt.insert(14, 14)
    bpt.insert(15, 15)
    bpt.insert(16, 16)
    bpt.insert(17, 17)
    bpt.insert(18, 18)
    bpt.insert(19, 19)
    bpt.insert(20, 20)
    bpt.insert(21, 21)
    bpt.insert(22, 22)
    bpt.insert(23, 23)
    bpt.insert(24, 24)
    bpt.insert(25, 25)
    print(bpt.get_dict())
    print(bpt.print_tree())
