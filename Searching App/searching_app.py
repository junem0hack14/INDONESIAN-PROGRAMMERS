class Node:
    """
    This class contains attributes of a node.
    """

    def __init__(self, value):
        # type: (str) -> None
        self.value: str = value
        self.left: Node or None = None  # initial value
        self.right: Node or None = None  # initial value

    def search(self, a_str):
        # type: (str) -> str
        curr_node: Node = self  # initial value
        if curr_node.value == a_str:
            return str(a_str) + " is found.\n"
        while curr_node.value != a_str:
            if a_str < curr_node.value:
                if curr_node.left is not None:
                    curr_node = curr_node.left
                    return curr_node.search(a_str)
                else:
                    return str(a_str) + " is not found.\n"
            else:
                if curr_node.right is not None:
                    curr_node = curr_node.right
                    return curr_node.search(a_str)
                else:
                    return str(a_str) + " is not found.\n"

    def insert(self, a_str):
        # type: (str) -> bool
        curr_node: Node = self  # initial value
        if a_str < curr_node.value:
            if curr_node.left is None:
                curr_node.left = Node(a_str)
                curr_node.left.right = curr_node
                return True

            while curr_node.left is not None:
                curr_node = curr_node.left
                curr_node.insert(a_str)

        elif a_str > curr_node.value:
            if curr_node.right is None:
                curr_node.right = Node(a_str)
                curr_node.right.left = curr_node
                return True

            while curr_node.right is not None:
                curr_node = curr_node.right
                curr_node.insert(a_str)

        else:
            return False

    def delete(self, a_str):
        # type: (str) -> bool
        curr_node: Node or None = self
        if curr_node.value == a_str:
            temp1: Node = curr_node.right
            temp2: Node = curr_node.left
            if not (curr_node.left is None and curr_node.right is None):
                if curr_node.left is not None:
                    curr_node.left.right = temp1

                if curr_node.right is not None:
                    curr_node.right.left = temp2

            else:
                curr_node = None

            return True
        while curr_node.value != a_str:
            if a_str < curr_node.value:
                if curr_node.left is not None:
                    curr_node = curr_node.left
                    curr_node.delete(a_str)
                else:
                    break
            else:
                if curr_node.right is not None:
                    curr_node = curr_node.right
                    curr_node.delete(a_str)
                else:
                    break

        return False

    def to_string(self):
        # type: () -> str
        res: str = "["  # initial value
        ret_list: list = []  # initial value
        curr_node: Node = self  # initial value
        while curr_node.left is not None:
            curr_node = curr_node.left

        while curr_node is not None:
            ret_list.append(curr_node.value)
            curr_node = curr_node.right

        for i in range(len(ret_list)):
            to_add: str = str(ret_list[i]) if i == len(ret_list) - 1 else str(ret_list[i]) + ", "
            res += to_add

        res += "]\n"
        return res


a: Node = Node("Jogja")
a.insert("Jakarta")
a.insert("Malang")
a.insert("Medan")
print(a.to_string())
a.delete("Medan")
print(a.to_string())
a.insert("Medan")
print(a.to_string())
a.delete("Malang")
print(a.to_string())
a.delete("Jakarta")
print(a.to_string())
a.insert("Surabaya")
print(a.to_string())
print(a.search("Jakarta"))
print(a.search("Jogja"))
print(a.search("Medan"))
print(a.search("Surabaya"))
