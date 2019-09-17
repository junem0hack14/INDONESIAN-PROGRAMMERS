class Node:
  """
  This class contains attributes of a node.
  """
  
  def __init__(self, value):
    # type: (object) -> None
    self.value: object = value
    self.next: Node or None = None
    self.previous: Node or None = None
      
  def add(self, value):
    # type: (object) -> None
    curr_node: Node = self
    if curr_node.next is None:
      curr_node.next = Node(value)
      curr_node.next.previous = self
    else:
      curr_node = curr_node.next
      curr_node.add(value)
      
  def remove(self):
    # type: (object) -> None
    curr_node: Node = self
      if curr_node.next is None:
        curr_node.previous.next = None
        curr_node = None
      else:
        curr_node = curr_node.previous
        curr_node.remove()
        
  def to_string(self):
    # type: () -> str
    res: str = "["  # initial value
    ret_list: list = []  # initial value
    curr_node: Node = self
    while curr_node.previous is not None:
      curr_node = curr_node.previous
      
    while curr_node.next is not None:
      ret_list.append(curr_node.value)
      curr_node = curr_node.next
      
    for i in range(len(ret_list)):
      to_add: str = str(ret_list[i]) if i == len(ret_list) - 1 else str(ret_list[i]) + ", "
      res += to_add
      
    res += "]\n"
    return res
  
  
a: Node = Node(5)
a.add(7)
a.add(9)
a.add("s")
print(a.to_string())
a.remove()
print(a.to_string())
