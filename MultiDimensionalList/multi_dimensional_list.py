def nest(a_list: list, length: int, elem: object) -> list:
	if a_list == []:
		a_list = [elem for i in range(length)]
	else:
		for i in range(len(a_list)):
			if isinstance(a_list[i], list):
				a_list[i] = nest(a_list[i], length, elem)
			else:
				a_list[i] = [elem for j in range(length)]
				
	return a_list

def all_int(a_list):
	# type: (list) -> bool
	for elem in a_list:
		if not isinstance(elem, int):
			return False
			
	return True


class MultiDimensionalList:
	"""
	This class contains attributes of a multi-dimensional list.
	"""
	
	def __init__(self, num_dimensions, dimensions):
		# type: (int, list) -> None
		self.num_dimensions = num_dimensions
		self.dimensions: list = dimensions if len(dimensions) == num_dimensions and all_int(dimensions) else [1]*num_dimensions
		self.elems = []  # initial value
		for i in range(len(dimensions)):
			self.elems = nest(self.elems, dimensions[i], "#")
			
	def to_string(self):
		# type: () -> str
		return str(self.elems)
		
		
a: MultiDimensionalList = MultiDimensionalList(3, [3, 3, 3])
print(a.to_string())
b: MultiDimensionalList = MultiDimensionalList(4, [2, 3, 4, 3])
print(b.to_string())
c: MultiDimensionalList = MultiDimensionalList(2, [4, 2])
print(c.to_string())
d: list = [[1, 2], [3, 4]]
print(nest(d, 3, 3))
k: int = int(input("Please enter a number: "))
l: int = int(input("Please enter a number: "))
e: MultiDimensionalList = MultiDimensionalList(k, [l for i in range(k)])
print(e.to_string())
