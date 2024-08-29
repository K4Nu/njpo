from functools import cache
import math
import random
class Tree():
    def __init__(self,data):
        self.data=data
        self.parent=None
        self.children=[]

    def add_child(self,child):
        child.parent=self
        self.children.append(child)

    def __str__(self,level=0):
        ret=" "*level*2+self.data+"\n"
        for child in self.children:
            ret+=child.__str__(level+1)
        return ret

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
            parent=random.choice(list(self))
            parent.add_child(new_child)

    def __call__(self, *args, **kwargs):
        return self.count()>0

    def __iter__(self):
        yield self

        for child in self.children:
            yield from child

    def __contains__(self, item):
        q=[self]
        while q:
            current=q.pop(0)
            if current.data==item:
                return True
            q.extend(current.children)
        return False

    def __getitem__(self, item):
        q=[self]
        index=0

        while q:
            current=q.pop(0)
            if index==item:
                return current.data
            index+=1
            q.extend(current.children)

        raise IndexError("The index is invalid")

    def __setitem__(self, data,parent_data):
        new_item=Tree(data=data)
        q=[self]
        while q:
            current=q.pop(0)
            if current.data==parent_data:
                new_item.parent=current
                current.add_child(new_item)
                return
            q.extend(current.children)
        raise ValueError(f"Parent {parent_data} not found")

    def __lshift__(self, new_child):
        if isinstance(new_child,Tree):
            self.add_child(new_child)
        else:
            raise ValueError("The operand must be an instance of Tree.")
        return self


t=Tree("Esiok")
t1=Tree("Zlom")
t2=Tree("Janek")
t.add_child(t1)
t1.add_child(t2)
#print(t.__pow__())
#t.print_tree()
print(t)
