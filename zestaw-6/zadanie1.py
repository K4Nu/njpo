from functools import cache
import math
import random
class Tree():
    def __init__(self,data):
        self.data=data
        self.parent=None
        self.children=[]

    def add_child(self,child):
        self.parent=self
        self.children.append(child)

    def print_tree(self,level=0):
        print(" "*level*2+self.data)
        for child in self.children:
            child.print_tree(level+1)

    def __len__(self):
        if not self.children:
            return 1

        level = 0
        children_check = self.children

        while children_check:
            new_children = []
            for child in children_check:
                if child.children:
                    new_children.extend(child.children)
            level += 1
            children_check = new_children

        return level + 1
    def count(self):
        if not self:
            return 0
        c=0
        q=[self]
        while q:
            current=q.pop(0)
            c+=1
            for child in current.children:
                q.append(child)
        return c

    def __pow__(self, power=2, modulo=None):
        initial_count = self.count()
        target_count = initial_count ** power

        while self.count() < target_count:
            new_name = "".join([chr(random.randint(ord("a"), ord("z"))) for _ in range(10)]).capitalize()
            new_child = Tree(data=new_name)
            self.add_child(new_child)

    def __call__(self, *args, **kwargs):
        return self.count()>0

    def __iter__(self,level=0):
        yield self,level

        for child in self.children:
            yield from child.__iter__(level+1)

t=Tree("Esiok")
t1=Tree("Zlom")
t2=Tree("Janek")
t.add_child(t1)
t1.add_child(t2)
t.print_tree()
print(t.__pow__())
#t.print_tree()
for node, level in t:
    print("\t" * level + node.data)