"""
Data Structures: Binary Tree and BST.
"""

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return f"TreeNode({self.val})"

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert(node.right, val)

    def search(self, val):
        return self._search(self.root, val)

    def _search(self, node, val):
        if node is None:
            return False
        if val == node.val:
            return True
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    # Traversals
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.val)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.val)

    def level_order(self):
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if not node:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def min_value(self):
        node = self.root
        while node.left:
            node = node.left
        return node.val

    def max_value(self):
        node = self.root
        while node.right:
            node = node.right
        return node.val

    def display(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root
        if node is not None:
            print(" " * (level * 4) + prefix + str(node.val))
            if node.left or node.right:
                if node.left:
                    self.display(node.left, level + 1, "L--- ")
                if node.right:
                    self.display(node.right, level + 1, "R--- ")

if __name__ == "__main__":
    print("=== Binary Search Tree ===")
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for v in values:
        bst.insert(v)

    print("Tree structure:")
    bst.display()

    print(f"\nInorder:     {bst.inorder()}")
    print(f"Preorder:    {bst.preorder()}")
    print(f"Postorder:   {bst.postorder()}")
    print(f"Level-order: {bst.level_order()}")
    print(f"Height: {bst.height()}")
    print(f"Min: {bst.min_value()}, Max: {bst.max_value()}")
    print(f"Search 40: {bst.search(40)}")
    print(f"Search 99: {bst.search(99)}")