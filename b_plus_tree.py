#!/usr/bin/env python3
"""B+ tree — ordered index with leaf-level linked list."""
class BPlusNode:
    def __init__(self,leaf=False):self.keys=[];self.children=[];self.leaf=leaf;self.next=None
class BPlusTree:
    def __init__(self,order=4):self.root=BPlusNode(True);self.order=order
    def search(self,key):
        node=self.root
        while not node.leaf:
            i=0
            while i<len(node.keys) and key>=node.keys[i]: i+=1
            node=node.children[i]
        return key in node.keys
    def insert(self,key):
        root=self.root
        if len(root.keys)<self.order-1: self._insert_non_full(root,key)
        else:
            new_root=BPlusNode();new_root.children=[root]
            self._split_child(new_root,0);self._insert_non_full(new_root,key)
            self.root=new_root
    def _insert_non_full(self,node,key):
        if node.leaf:
            i=0
            while i<len(node.keys) and node.keys[i]<key: i+=1
            node.keys.insert(i,key)
        else:
            i=len(node.keys)-1
            while i>=0 and key<node.keys[i]: i-=1
            i+=1
            if len(node.children[i].keys)>=self.order-1:
                self._split_child(node,i)
                if key>node.keys[i]: i+=1
            self._insert_non_full(node.children[i],key)
    def _split_child(self,parent,i):
        child=parent.children[i];mid=len(child.keys)//2
        new=BPlusNode(child.leaf)
        if child.leaf:
            new.keys=child.keys[mid:];child.keys=child.keys[:mid]
            new.next=child.next;child.next=new
            parent.keys.insert(i,new.keys[0])
        else:
            new.keys=child.keys[mid+1:];up=child.keys[mid];child.keys=child.keys[:mid]
            new.children=child.children[mid+1:];child.children=child.children[:mid+1]
            parent.keys.insert(i,up)
        parent.children.insert(i+1,new)
    def range_query(self,lo,hi):
        node=self.root
        while not node.leaf:
            i=0
            while i<len(node.keys) and lo>=node.keys[i]: i+=1
            node=node.children[i]
        result=[]
        while node:
            for k in node.keys:
                if lo<=k<=hi: result.append(k)
                elif k>hi: return result
            node=node.next
        return result
def main():
    bt=BPlusTree(4)
    for x in [10,20,5,6,12,30,7,17]: bt.insert(x)
    print(f"Range [5,15]: {bt.range_query(5,15)}")
if __name__=="__main__":main()
