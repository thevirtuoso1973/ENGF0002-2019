class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def insert(self, key, value):
        if self.key == key:
            self.value = value
            return
        if key < self.key:  #left
            if self.left is None:
                self.left = TreeNode(key, value)
            else:
                self.left.insert(key, value)
        else:  # right
            if self.right is None:
                self.right = TreeNode(key, value)
            else:
                self.right.insert(key, value)

    def __str__(self):
        s = ""
        if self.left is not None:
            s += str(self.left) + "\n"
        s += str(self.key) + ": " + str(self.value)
        if self.right is not None:
            s += "\n" + str(self.right)
        return s
        
    def find(self, key):
        if self.key == key:
            return self.value
        if key < self.key:  #left
            if self.left is None:
                return None
            else:
                return self.left.find(key)
        else:  # right
            if self.right is None:
                return None
            else:
                return self.right.find(key)

    def maxnode(self):
        if self.right is None:
            return self
        return self.right.maxnode()
    
    def delete(self, key):
        if self.key == key:
            if self.left is None:  #handle right child only and no children
                return self.right
            if self.right is None:  #handle left child only
                return self.left
            # we had two children
            maxn = self.left.maxnode()
            self.key = maxn.key
            self.value = maxn.value
            self.left = self.left.delete(maxn.key)
        elif key < self.key:
            if self.left is not None:
                self.left = self.left.delete(key)
        else:
            if self.right is not None:
                self.right = self.right.delete(key)
        return self

    def walk(self):
        if self.left is not None:
            yield from self.left.walk()
        yield (self.key, self.value)
        if self.right is not None:
            yield from self.right.walk()


root = TreeNode(50, "aaa50")
root.insert(25, "bbbb25")
root.insert(100, "cccc100")
root.insert(30, "dddd30")
root.insert(40, "eee40")
root.insert(15, "eee40")
root.insert(18, "eee40")

print(root)

print(root.find(50))
print(root.find(25))
print(root.find(100))
print(root.find(30))
print(root.find(40))

print("max")
print(root.maxnode())

print("generator test:")
for k,v in root.walk():
    print(k,v)
print("\n")


print("\n del 25")
root = root.delete(25)
print(root)

print("\n del 50")
root = root.delete(50)
print(root)

root = root.delete(100)
root = root.delete(30)
root = root.delete(40)
root = root.delete(15)
root = root.delete(18)

print("here:")
print(root)
