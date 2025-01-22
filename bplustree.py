import math


class Node:
    def __init__(self, is_leaf=False):
        """
        A Class to represent a node in a B+ tree

        Attributes:
            is_leaf (bool): A boolean to indicate if the node is a leaf node
        """
        self.is_leaf = is_leaf
        self.keys = []
        self.pointers = []


    def getDict(self):
        """
        returns a dictionary representation of the node

        Returns:
            dict: A dictionary representation of the node
        """
        if self.is_leaf:
            return {'keys': self.keys, 'children': [], 'is_leaf': True}
        return {'keys': self.keys, 'children': [n.getDict() for n in self.pointers], 'is_leaf': False}


    def __repr__(self):
        """
        String representation of the node

        Returns:
            str: A string representation of the node
        """
        return f"Node({self.keys})"


class BPlusTree:
    def __init__(self, order):
        """
        A Class to represent a B+ tree

        Attributes:
            order (int): The order of the B+ tree
            root (Node): The root node of the B+ tree
        """
        self.order = order
        self.root = None


    def search(self, key):
        """
        Search for a key in the tree

        Args:
            key (int): The key to search for
        """
        if key == None or self.root == None:
            return None
        current_node = self.__find_leaf(key)
        for i, k in enumerate(current_node.keys):
            if k == key:
                return (current_node, i)
        return None


    def test_find(self, key):
        """
        Test function to find the leaf node that contains the key

        Args:
            key (int): The key to search for in the tree

        Returns:
            Node: The leaf node that contains the key
        """
        """Test function to find the leaf node that contains the key"""
        return self.__find_leaf(key)


    def __find_leaf(self, key):
        """
        Find the leaf node that contains the key

        Args:
            key (int): The key to search for in the tree

        Returns:
            Node: The leaf node that contains the key
        """
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while i < len(current_node.keys) and key >= current_node.keys[i]:
                i+=1
            current_node = current_node.pointers[i]
        return current_node


    def insert(self, key, pointer):
        """
        Insert a key and a pointer into the tree

        Args:
            key (int): The key to insert
            pointer (int): The pointer to insert

        Returns:
            Node: The leaf node that contains the key
        """
        if key == None or pointer == None:
            print('Inserting None?')
            return
        leaf = None
        if self.root == None:
            self.root = Node(is_leaf=True)
            leaf = self.root
        else:
            leaf = self.__find_leaf(key)

        if len(leaf.keys) < self.order-1:
            self.__insert_in_leaf(leaf, key, pointer)
        else:
            leaf_t = Node(is_leaf=True)
            temp = self.__get_copy_temp(leaf)
            self.__insert_in_leaf(temp, key, pointer)

            if(leaf.pointers[-1] is Node): 
                leaf_t.pointers.append(leaf.pointers[-1])
            leaf.pointers = [leaf_t]
            leaf.keys.clear()

            border = int(math.ceil(self.order/2))

            leaf.keys = temp.keys[:border]
            leaf.pointers = temp.pointers[:border] + leaf.pointers

            leaf_t.keys = temp.keys[border:]
            leaf_t.pointers += temp.pointers[border:]   # changed this from book

            k_t = leaf_t.keys[0] 
            self.__insert_in_parent(leaf, k_t, leaf_t)


    def __get_copy_temp(self, node, full=False):
        """
        Get a copy of a node

        Args:
            node (Node): The node to copy
            full (bool): A boolean to indicate if the copy should be full

        Returns:
            Node: A copy of the node
        """
        temp = Node(is_leaf= node.is_leaf)
        c = 0 if full else 1
        if self.__is_right_edge(node):
            c = 0
        temp.keys = node.keys[:]
        temp.pointers = node.pointers[:len(node.pointers)-c]
        return temp


    def __insert_in_leaf(self, leaf, key, pointer):
        """
        Insert a key and a pointer into a leaf node

        Args:
            leaf (Node): The leaf node to insert the key and pointer
            key (int): The key to insert
            pointer (int): The pointer to insert

        Returns:
            int: The index of the key in the leaf node
        """
        if leaf == self.root and len(leaf.keys) == 0:
            leaf.keys = [key]
            leaf.pointers = [pointer]
            return

        if key < leaf.keys[0]:
            leaf.keys.insert(0, key)
            leaf.pointers.insert(0, pointer)
        else:
            self.__add_key_pointer(leaf, key, pointer)


    def __insert_in_parent(self, node, k_t, node_t):
        """
        Insert a key and a pointer into the parent node

        Args:
            node (Node): The node to insert the key and pointer
            k_t (int): The key to insert
            node_t (Node): The pointer to

        Returns:
            Node: The parent node
        """
        if node == self.root:
            node_r = Node()
            node_r.keys = [k_t]
            node_r.pointers = [node, node_t]
            self.root = node_r
            return

        node_p = self.parent(node)
        if len(node_p.pointers) < self.order:
            index = node_p.pointers.index(node)
            node_p.pointers.insert(index+1, node_t)
            node_p.keys.insert(index, k_t)
        else:

            temp = self.__get_copy_temp(node_p, full=True)
            index = temp.pointers.index(node)
            temp.pointers.insert(index+1, node_t) # test if +1 is needed
            temp.keys.insert(index, k_t)

            node_p.keys.clear()
            node_p.pointers.clear()
            node_p_t = Node()
            border = int(math.ceil((self.order+1)/2))
            node_p.keys = temp.keys[:border-1]
            node_p.pointers = temp.pointers[:border]
            k_tt = temp.keys[border-1]
            node_p_t.keys = temp.keys[border:]
            node_p_t.pointers = temp.pointers[border:]

            self.__insert_in_parent(node_p, k_tt, node_p_t)


    def parent(self, node):
        """
        Get the parent of a node

        Args:
            node (Node): The node to get the parent of

        Returns:
            Node: The parent node
        """
        if self.root == node:
            return None
        return self.__find_parent(self.root, node)


    def __find_parent(self, current_node, child_node):
        """
        Find the parent of a node

        Args:
            current_node (Node): The current node
            child_node (Node): The child node

        Returns:
            Node: The parent node
        """
        if current_node.is_leaf:
            return None
        for child in current_node.pointers:
            if child == child_node:
                return current_node
            parent = self.__find_parent(child, child_node)
            if parent:
                return parent
        return None


    def delete(self, key, pointer):
        """
        Delete an entry from the tree

        Args:
            key (int): The key to delete
            pointer (int): The pointer to delete from the tree

        Returns:
            Node: The leaf node that contains the key
        """
        leaf = self.__find_leaf(key)
        self.__delete_entry(leaf, key, pointer)


    def __add_last_merge_pointer(self, node_t, pointer):
        """
        Add the last pointer to a node

        Args:
            node_t (Node): The node to add the pointer to
            pointer (int): The pointer to add to the node

        Returns:
            int: The index of the pointer in the node
        """
        elem = pointer.keys[-1]
        pos = 0
        for node in node_t.pointers:
            comp = node.keys[0]
            if elem < comp:
                break
            pos += 1
        node_t.pointers.insert(pos, pointer)


    def __merge(self, node_t, node, k_t):
        """
        Merge two nodes

        Args:
            node_t (Node): The node to merge into
            node (Node): The node to merge
            k_t (int): The key to merge

        Returns:
            Node: The parent node
        """
        if not(node.is_leaf):
            self.__add_only_key(node_t, k_t)

            for i in range(0, len(node.keys)):
                self.__add_key_pointer(node_t, node.keys[i], node.pointers[i])

            self.__add_last_merge_pointer(node_t, node.pointers[-1])

        else:
            if len(node.keys) > 0:
                self.__merge_leaf_nodes(node_t, node)
                node_t.pointers[-1] = node.pointers[-1]


            if self.__is_right_edge(node):
                node_t.pointers.pop()


    def __is_right_edge(self, node):
        """
        Check if a node is the right edge of the tree

        Args:
            node (Node): The node to check

        Returns:
            bool: A boolean to indicate if the node is the right edge of the tree
        """
        cur = self.root
        while not(cur.is_leaf):
            cur = cur.pointers[-1]
        return cur == node


    def __merge_leaf_nodes(self, node_t, node):
        """
        Merge two leaf nodes

        Args:
            node_t (Node): The node to merge into
            node (Node): The node to merge

        Returns:
            Node: The parent node
        """
        index = 0
        while index < len(node_t.keys):
            if node_t.keys[index] > node.keys[0]:
                break
            index+=1
        for i in range(0, len(node.keys)):
            node_t.keys.insert(index+i, node.keys[i])
            node_t.pointers.insert(index+i, node.pointers[i])


    def __add_only_key(self, node, key):
        """
        Add a key to a node

        Args:
            node (Node): The node to add the key to
            key (int): The key to add to the node

        Returns:
            int: The index of the key in the node
        """
        i = 0
        while i < len(node.keys):
            if node.keys[i] > key:
                node.keys.insert(i, key)
                return
            i += 1
        node.keys.append(key)


    def __add_key_pointer(self, node, key, pointer):
        """
        Add a key and a pointer to a node

        Args:
            node (Node): The node to add the key and pointer to
            key (int): The key to add to the node
            pointer (int): The pointer to add to the node

        Returns:
            int: The index of the key in the node
        """
        i = 0
        while i < len(node.keys):
            if node.keys[i] > key:
                node.keys.insert(i, key)
                node.pointers.insert(i, pointer)
                return i
            i+=1
        node.keys.append(key)
        node.pointers.append(pointer)
        return i


    def __delete_entry(self, node, key, pointer):
        """
        Delete an entry from the tree

        Args:
            node (Node): The node to delete the entry from
            key (int): The key to delete
            pointer (int): The pointer to delete from the tree

        Returns:
            Node: The parent node
        """
        node.keys.remove(key)
        node.pointers.remove(pointer)

        if self.root == node and self.root.is_leaf:
            if len(self.root.keys) == 0:
                del node
                self.root = None
            return

        elif_cond = len(node.pointers) < int(math.ceil(self.order/2))
        if node.is_leaf:
            elif_cond = len(node.keys) < int(math.ceil((self.order-1)/2))

        if node == self.root and len(node.pointers) == 1:
            self.root = node.pointers[0]
            del node
        elif elif_cond:
            node_t = self.__get_sibling(node)
            parent = self.parent(node)
            index = parent.pointers.index(node_t)
            index2 = parent.pointers.index(node)
            k_t = parent.keys[index] if index < index2 else parent.keys[index2] # questionable!!!

            if len(node.keys)+len(node_t.keys) <= self.order-1:
                if self.is_pred(node, node_t):
                    node, node_t = node_t, node

                self.__merge(node_t, node, k_t)

                self.__delete_entry(self.parent(node), k_t, node)

                del node
            else:
                if self.is_pred(node_t, node): # borrow from left
                    if not(node.is_leaf) and not(node == self.root):
                        m_key = node_t.keys.pop()
                        m = node_t.pointers.pop()

                        node.keys.insert(0, k_t)
                        node.pointers.insert(0, m)

                        parent.keys[parent.keys.index(k_t)] = m_key #node_t.keys[-1]
                    else:
                        m_key = node_t.keys.pop()
                        m_pointer = node_t.pointers.pop()

                        node.keys.insert(0, m_key)
                        node.pointers.insert(0, m_pointer)

                        parent.keys[parent.keys.index(k_t)] = m_key
                else: 
                    if not(node.is_leaf) and not(node == self.root):
                        node_t.keys.pop(0)
                        m = node_t.pointers.pop(0)

                        node.keys.append(k_t)
                        node.pointers.append(m)

                        parent.keys[parent.keys.index(k_t)] =  node_t.keys[0]
                    else:
                        m_key = node_t.keys.pop(0)
                        m_pointer = node_t.pointers.pop(0)

                        node.keys.append(m_key)
                        node.pointers.append(m_pointer)

                        parent.keys[parent.keys.index(k_t)] = node_t.keys[0]


    def is_pred(self, node, node_t):
        """
        Check if a node is a predecessor of another node

        Args:
            node (Node): The first node
            node_t (Node): The second node

        Returns:
            bool: A boolean to indicate if the first node is a predecessor of the second node
        """
        cur = self.root
        while cur is not node_t:
            idx = self.__find_key(cur, node_t.keys[0])
            if idx > 0 and cur.pointers[idx - 1] is node:
                return True
            cur = cur.pointers[idx]
        return False


    def __find_key(self, x, k):
        """
        Find a key in a node

        Args:
            x (Node): The node to search for the key
            k (int): The key to search for in the node

        Returns:
            int: The index of the key in the node
        """
        idx = 0
        while idx < len(x.keys) and x.keys[idx] <= k:
            idx += 1
        return idx


    def __get_sibling(self, node):
        """
        Get the sibling of a node

        Args:
            node (Node): The node to get the sibling of

        Returns:
            Node: The sibling node
        """
        parent = self.parent(node)
        index = parent.pointers.index(node)
        if index > 0:
            return parent.pointers[index-1]
        else:
            return parent.pointers[index+1]


    def print_tree(self, debugLeaves = False, showPointers = False):
        """
        Print the tree

        Args:
            debugLeaves (bool): A boolean to indicate if the leaves should be printed
            showPointers (bool): A boolean to indicate if the pointers should be shown

        Returns:
            str: The string representation of the tree
        """
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
                nodes += [(level+1, node.pointers[i]) for i in range(len(node.pointers))]
            else:
                leaves += node.pointers
            last_level = level

        print()
        if debugLeaves:
            print(leaves)


    def __str__(self):
        """
        String representation of the tree

        Returns:
            str: The string representation of the tree
        """
        if self.root == None:
            return "Empty Tree"
        result = ""
        nodes = [(0, self.root)]
        last_level = 0
        while len(nodes) != 0:
            (level, node) = nodes.pop(0)
            if last_level != level:
                result += "\n"
            result += f"{node.keys} "
            if not(node.is_leaf):
                nodes += [(level+1, node.pointers[i]) for i in range(len(node.pointers))]
            last_level = level
        return result


    def getDictTree(self):
        """
        Get a dictionary representation of the tree

        Returns:
            dict: A dictionary representation of the tree
        """
        if self.root == None:
            return {'root': {}}
        return {'root': self.root.getDict()}


    def getLevelSizes(self):
        """
        Get the sizes of the levels in the tree

        Returns:
            list: A list of the sizes of the levels in the tree
        """
        levels = {0:1}
        nodes = [(0,self.root)]
        while len(nodes) != 0:
            (level, cur) = nodes.pop()

            if not(level+1 in levels.keys()): 
                levels[level+1] = 0

            levels[level+1] += len(cur.pointers)
            if not(cur.is_leaf):
                nodes+=[(level+1, p) for p in cur.pointers]

        return [levels[key] for key in levels.keys()][:-1]


if __name__ == "__main__":
    bpt = BPlusTree(3)
    bpt.insert(1, 1)
    bpt.insert(2, 2)
    bpt.insert(3, 3)
    bpt.insert(4, 4)
    bpt.insert(5, 5)
    bpt.insert(6, 6)
    bpt.insert(7, 7)
    bpt.insert(9, 9)

