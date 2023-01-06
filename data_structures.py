class Node():
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node

class StackVacancies():
    def __init__(self):
        self.top = None

    def push(self, data):
        new_top = Node(data, self.top)
        self.top = new_top

    def pop(self):
        if self.top is None:
            return None
        removed_data = self.top.data
        self.top = self.top.next_node
        return removed_data

    def to_list(self):
        l = []
        node = self.top
        while node:
            l.append(node.data)
            node = node.next_node
        return l

if __name__ == "__main__":
    s = StackVacancies()

    for i in range(1, 10):
        s.push(i)
        print(s)

    for i in s.to_list():
        print(i)