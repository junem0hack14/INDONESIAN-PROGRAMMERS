class Node:
	"""
	This class contains attributes of nodes.
	"""
	
	def __init__(self, value):
		# type: (object or None) -> None
		self.value: object or None = value
		self.next: Node or None = None  # initial value
		self.index: int = 0  # initial value
		
	def to_string(self):
		# type: () -> str
		ret_list: list = []  # initial value
		curr_node: Node = self
		while curr_node is not None:
			ret_list.append(curr_node.value)
			curr_node = curr_node.next
			
		res: str = "["  # initial value
		for i in range(len(ret_list)):
			to_add: str = str(ret_list[i]) if i == len(ret_list) - 1 else str(ret_list[i]) + ", "
			res += to_add
			
		res += "]\n"
		return res
		
	def append(self, value):
		# type: (object) -> None
		self.next: Node = Node(value)
		self.next.index = self.index + 1
		
	def delete(self, index):
		# type: (int) -> None
		curr_node: Node = self
		to_remove: Node or None = None  # initial value
		while curr_node.next is not None:
			if curr_node.index != index:
				curr_node = curr_node.next
			else:
				to_remove = curr_node
				break
				
		if to_remove is not None:
			curr_node = to_remove
			while curr_node.next is not None:
				curr_node = curr_node.next
				
	def remove(self, node):
		# type: (Node) -> None
		curr_node: Node = self
		to_remove: Node or None = None  # initial value
		while curr_node.next is not None:
			if curr_node != node:
				curr_node = curr_node.next
			else:
				to_remove = curr_node
				break
				
		if to_remove is not None:
			curr_node = to_remove
			while curr_node.next is not None:
				curr_node = curr_node.next
				
				
a = Node(23)
b = 25
a.append(b)
a.next.append(30)
a.next.next.append("s")
print(a.to_string())
