from exceptions_classes import*

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
        if self.top is None:
            return l
        node = self.top
        while node:
            l.append(node.data)
            node = node.next_node
        l.reverse()
        return l

class LinkedListVacancies():
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_begining(self, data):
        if self.head is None:
            self.head = self.tail = Node(data, None)
            return
        new_node = Node(data, self.head)
        self.head = new_node

    def insert_end(self, data):
        if self.head is None:
            self.head = self.tail = Node(data, None)
            return
        self.tail.next_node = Node(data, None)
        self.tail = self.tail.next_node

    def search_by_id(self, id_vac):
        node = self.head
        while node:
            if node.data.get_id() == id_vac:
                return node.data
            node = node.next_node
        raise NotFoundIdVacancy(f"Вакансия с номером {id_vac} не найдена в последней выгрузке. Скорректируйте запрос")

    def to_list(self):
        l = []
        if self.head is None:
            return l
        node = self.head
        while node:
            l.append(node.data)
            node = node.next_node
        return l



if __name__ == "__main__":
    s = StackVacancies()

    for i in range(1, 10):
        s.push(i)

    for i in s.to_list():
        print(i)

    ll = LinkedListVacancies()

    for i in range(1, 10):
        ll.insert_end(i)

    for i in ll.to_list():
        print(i)