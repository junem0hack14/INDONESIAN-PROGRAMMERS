import copy
import sys

sys.modules['_decimal'] = None
import decimal
from decimal import *
from decimal import Decimal

getcontext().Emin = -10 ** 10000
getcontext().Emax = 10 ** 10000
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100

POSSIBLE_OPERATIONS: list = ["INTERSECT", "UNION"]


def is_operation(a_str: str) -> bool:
    return a_str in POSSIBLE_OPERATIONS


def graph_exists(a_str, graph_list):
    # type: (str, list) -> bool
    for graph in graph_list:
        if graph.name == a_str:
            return True

    return False


def evaluate_expression(expr, graph_list):
    # type: (str, list) -> Graph
    nodes: list = []  # initial value
    whitespace: str = " "
    values: list = expr.split(whitespace)
    for value in values:
        if is_operation(value):
            nodes.append(OperationNode(value))
        elif graph_exists(value, graph_list):
            # Getting the corresponding graph
            corresponding_graph: Graph or None = None  # initial value
            for graph in graph_list:
                if graph.name == value:
                    corresponding_graph = graph
                    break

            nodes.append(GraphNode(corresponding_graph))

    while len(nodes) > 1:
        first_graph: Graph = nodes[0].evaluate(nodes[1], nodes[2])
        temp_list: list = [GraphNode(first_graph)]  # initial value
        for i in range(3, len(nodes)):
            temp_list.append(nodes[i])

        nodes = temp_list

    return nodes[0].value


class Node:
    """
    This class contains attributes of nodes to store data
    """

    def __init__(self):
        self.value = None


class GraphNode(Node):
    """
    This class contains attributes of nodes to store graphs.
    """

    def __init__(self, value):
        # type: (Graph) -> None
        super(GraphNode, self).__init__()
        self.value: Graph = value

    def evaluate(self, operation_node, graph_node):
        # type: (OperationNode, GraphNode) -> Graph
        new_graph: Graph = Graph()
        if operation_node.value == "INTERSECT":
            for link in self.value.links:
                # Getting the corresponding link
                corresponding_link: Link or None = None  # initial value
                for curr_link in graph_node.value.links:
                    if (curr_link.from_vertex == link.from_vertex and curr_link.to_vertex == link.to_vertex) or \
                            (curr_link.from_vertex == link.to_vertex and curr_link.to_vertex == link.from_vertex):
                        corresponding_link = curr_link

                if corresponding_link is not None:
                    to_add: Link = corresponding_link if corresponding_link.weight > link.weight else link
                    new_graph.add_link(to_add)

        elif operation_node.value == "UNION":
            for link in self.value.links:
                # Getting the corresponding link
                corresponding_link: Link or None = None  # initial value
                for curr_link in graph_node.value.links:
                    if (curr_link.from_vertex == link.from_vertex and curr_link.to_vertex == link.to_vertex) or \
                            (curr_link.from_vertex == link.to_vertex and curr_link.to_vertex == link.from_vertex):
                        corresponding_link = curr_link
                        break

                if corresponding_link is not None:
                    to_add: Link = corresponding_link if corresponding_link.weight > link.weight else link
                    new_graph.add_link(to_add)
                else:
                    new_graph.add_link(link)

            for link in graph_node.value.links:
                # Getting the corresponding link
                corresponding_link: Link or None = None  # initial value
                for curr_link in self.value.links:
                    if (curr_link.from_vertex == link.from_vertex and curr_link.to_vertex == link.to_vertex) or \
                            (curr_link.from_vertex == link.to_vertex and curr_link.to_vertex == link.from_vertex):
                        corresponding_link = curr_link
                        break

                if corresponding_link is None:
                    new_graph.add_link(link)

        return new_graph


class OperationNode(Node):
    """
    This class contains attributes of nodes used for storing operations.
    """

    def __init__(self, value: str):
        super().__init__()
        assert value in POSSIBLE_OPERATIONS, "Invalid argument 'value'!"
        self.value: str or None = value


class Operation:
    """
    This class contains attributes of graph operations which the user can use.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.name: str or None = name if name in POSSIBLE_OPERATIONS else None

    def clone(self):
        # type: () -> Operation
        return copy.deepcopy(self)


class Graph:
    """
    This class contains attributes of a graph.
    """

    def __init__(self):
        # type: () -> None
        self.name: str = ""  # initial value
        self.vertices: list = []  # initial value
        self.links: list = []  # initial value

    def set_name(self, name: str):
        self.name = name

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Graph " + str(self.name) + "\n"
        res += "List of vertices: \n"
        for i in range(len(self.vertices)):
            res += str(i + 1) + ". " + str(self.vertices[i].to_string()) + "\n"

        res += "List of links: \n"
        for link in self.links:
            res += str(link.to_string()) + "\n"

        return res

    def add_vertex(self, vertex):
        # type: (Vertex) -> bool
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            return True
        return False

    def remove_vertex(self, vertex):
        # type:(Vertex) -> bool
        if vertex in self.vertices:
            self.vertices.remove(vertex)
            for link in self.links:
                if link.from_vertex == vertex or link.to_vertex == vertex:
                    self.remove_link(link)

            return True
        return False

    def add_link(self, link):
        # type: (Link) -> bool
        link_exists: bool = False  # initial value
        for curr_link in self.links:
            if (curr_link.from_vertex == link.from_vertex and curr_link.to_vertex == link.to_vertex) or \
                    (curr_link.from_vertex == link.to_vertex and curr_link.to_vertex == link.from_vertex):
                link_exists = True
                break

        if not link_exists:
            self.links.append(link)
            self.add_vertex(link.from_vertex)
            self.add_vertex(link.to_vertex)
            return True
        return False

    def remove_link(self, link):
        # type: (Link) -> bool
        corresponding_link: Link or None = None  # initial value
        link_exists: bool = False  # initial value
        for curr_link in self.links:
            if (curr_link.from_vertex == link.from_vertex and curr_link.to_vertex == link.to_vertex) or \
                    (curr_link.from_vertex == link.to_vertex and curr_link.to_vertex == link.from_vertex):
                link_exists = True
                corresponding_link = curr_link
                break

        if not link_exists:
            return False
        else:
            start_vertex: Vertex = corresponding_link.from_vertex
            end_vertex: Vertex = corresponding_link.to_vertex
            self.links.remove(corresponding_link)
            start_vertex_linked: bool = False  # initial value
            end_vertex_linked: bool = False  # initial value
            for curr_link in self.links:
                if curr_link.from_vertex == start_vertex or curr_link.to_vertex == start_vertex:
                    start_vertex_linked = True
                    break

            for curr_link in self.links:
                if curr_link.from_vertex == end_vertex or curr_link.to_vertex == end_vertex:
                    end_vertex_linked = True
                    break

            if not start_vertex_linked:
                self.remove_vertex(start_vertex)

            if not end_vertex_linked:
                self.remove_vertex(end_vertex)

            return True

    def clone(self):
        # type: () -> Graph
        return copy.deepcopy(self)


class Vertex:
    """
    This class contains attributes of vertices in a graph.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name

    def to_string(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Vertex
        return copy.deepcopy(self)


class Link:
    """
    This class contains attributes of links between two nodes in a graph.
    """

    def __init__(self, from_vertex, to_vertex, weight):
        # type: (Vertex, Vertex, Decimal or int or float) -> None
        self.from_vertex: Vertex = from_vertex
        self.to_vertex: Vertex = to_vertex
        self.weight: Decimal or int or float = weight

    def to_string(self):
        # type: () -> str
        return str(self.from_vertex.to_string()) + " - " + str(self.to_vertex.to_string()) + ", weight = " + \
               str(self.weight) + "\n"

    def clone(self):
        # type: () -> Link
        return copy.deepcopy(self)


def main():
    """
    This function is used to run the program.
    :return:
    """
    print("Enter 1 to type an expression.")
    print("Enter 2 to add a new graph.")
    print("Enter 3 to edit an existing graph.")
    print("Enter 4 to remove an existing graph.")
    print("Enter 5 to quit.")
    existing_graphs: list = []  # initial value
    option: int = int(input("Please enter a number: "))
    while option < 1 or option > 5:
        option: int = int(input("Sorry, invalid input! Please enter a number: "))

    while option != 5:
        if option == 1:
            alphabets: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
            allowed_chars: list = [" "]  # initial value
            for char in alphabets:
                allowed_chars.append(char)

            for char in POSSIBLE_OPERATIONS:
                allowed_chars.append(char)

            if len(existing_graphs) > 1:
                expression: str = input("Please enter an expression: ")
                can_proceed: bool = True  # initial value
                for char in expression:
                    if char not in allowed_chars:
                        can_proceed = False

                while not can_proceed:
                    expression: str = input("Sorry, invalid expression! Please enter another expression: ")
                    can_proceed = True  # initial value
                    for char in expression:
                        if char not in allowed_chars:
                            can_proceed = False

                result: Graph = evaluate_expression(expression, existing_graphs)
                print(str(expression) + " = " + str(result.to_string()))

        elif option == 2:
            print("Please enter information regarding the new graph you want to add.")
            new_graph: Graph = Graph()
            name: str = input("Please enter name of the graph: ")
            new_graph.set_name(name)
            num_vertices: int = int(input("How many vertices do you want? "))
            for i in range(num_vertices):
                name: str = input("Please enter name of vertex: ")
                new_vertex: Vertex = Vertex(name)
                new_graph.add_vertex(new_vertex)

            print("Enter Y for yes.")
            print("Enter anything else for no.")
            add_link_ask: str = input("Do you want to add a link? ")
            while add_link_ask == "Y":
                start_vertex_name: str = input("Please enter the vertex where the link starts: ")
                end_vertex_name: str = input("Please enter the vertex where the link ends: ")
                matching_start_vertex: Vertex or None = None  # initial value
                matching_end_vertex: Vertex or None = None  # initial value
                for vertex in new_graph.vertices:
                    if vertex.name == start_vertex_name:
                        matching_start_vertex = vertex

                    if vertex.name == end_vertex_name:
                        matching_end_vertex = vertex

                while matching_start_vertex is None or matching_end_vertex is None or \
                        matching_start_vertex == matching_end_vertex:
                    start_vertex_name: str = input("Invalid input! Please enter the vertex where the link starts: ")
                    end_vertex_name: str = input("Invalid input! Please enter the vertex where the link ends: ")
                    matching_start_vertex: Vertex or None = None  # initial value
                    matching_end_vertex: Vertex or None = None  # initial value
                    for vertex in new_graph.vertices:
                        if vertex.name == start_vertex_name:
                            matching_start_vertex = vertex

                        if vertex.name == end_vertex_name:
                            matching_end_vertex = vertex

                weight: Decimal or int or float = Decimal(input("Please enter weight of the link: "))
                new_graph.add_link(Link(matching_start_vertex, matching_end_vertex, weight))
                add_link_ask: str = input("Do you want to add a link? ")

            existing_graphs.append(new_graph)

        elif option == 3:
            print("Below is a list of graphs that you have: \n")
            for graph in existing_graphs:
                print(graph.to_string())

            graph_index: int = int(input("Please enter the index of the graph that you want to edit: "))
            while graph_index < 0 or graph_index >= len(existing_graphs):
                graph_index: int = int(input("Invalid input! "
                                             "Please enter the index of the graph that you want to edit: "))

            graph_to_edit: Graph = existing_graphs[graph_index]
            print("Enter 1 to add a new vertex.")
            print("Enter 2 to remove an existing vertex.")
            print("Enter 3 to add a new link.")
            print("Enter 4 to remove an existing link.")
            print("Enter 5 to return to main menu.")
            decision: int = int(input("Please enter your decision code: "))
            while decision < 1 or decision > 5:
                decision: int = int(input("Sorry, invalid input! Please enter your decision code: "))

            while decision != 5:
                if decision == 1:
                    vertex_name: str = input("Please enter name of vertex: ")
                    to_add: Vertex = Vertex(vertex_name)
                    graph_to_edit.add_vertex(to_add)
                elif decision == 2:
                    print("Below is a list of vertices you already have.\n")
                    for vertex in graph_to_edit.vertices:
                        print(vertex.to_string())

                    vertex_index: int = int(input("Please enter index of vertex you want to delete: "))
                    while vertex_index < 0 or vertex_index >= len(graph_to_edit.vertices):
                        vertex_index: int = int(input("Invalid input! "
                                                      "Please enter index of vertex you want to delete: "))

                    to_remove: Vertex = graph_to_edit.vertices[vertex_index]
                    graph_to_edit.remove_vertex(to_remove)
                elif decision == 3:
                    start_vertex_name: str = input("Please enter the vertex where the link starts: ")
                    end_vertex_name: str = input("Please enter the vertex where the link ends: ")
                    matching_start_vertex: Vertex or None = None  # initial value
                    matching_end_vertex: Vertex or None = None  # initial value
                    for vertex in graph_to_edit.vertices:
                        if vertex.name == start_vertex_name:
                            matching_start_vertex = vertex

                        if vertex.name == end_vertex_name:
                            matching_end_vertex = vertex

                    while matching_start_vertex is None or matching_end_vertex is None or \
                            matching_start_vertex == matching_end_vertex:
                        start_vertex_name: str = input("Invalid input! Please enter the vertex where the link starts: ")
                        end_vertex_name: str = input("Invalid input! Please enter the vertex where the link ends: ")
                        matching_start_vertex: Vertex or None = None  # initial value
                        matching_end_vertex: Vertex or None = None  # initial value
                        for vertex in graph_to_edit.vertices:
                            if vertex.name == start_vertex_name:
                                matching_start_vertex = vertex

                            if vertex.name == end_vertex_name:
                                matching_end_vertex = vertex

                    weight: Decimal or int or float = Decimal(input("Please enter weight of the link: "))
                    graph_to_edit.add_link(Link(matching_start_vertex, matching_end_vertex, weight))

                elif decision == 4:
                    print("Below is a list of existing links in the graph.\n")
                    for link in graph_to_edit.links:
                        print(link.to_string())

                    link_index: int = int(input("Please enter index of link you want to remove: "))
                    to_remove: Link = graph_to_edit.links[link_index]
                    graph_to_edit.remove_link(to_remove)

                decision: int = int(input("Please enter your decision code: "))
                while decision < 1 or decision > 5:
                    decision: int = int(input("Sorry, invalid input! Please enter your decision code: "))

        elif option == 4:
            print("Below is a list of graphs that you have: \n")
            for graph in existing_graphs:
                print(graph.to_string())

            graph_index: int = int(input("Please enter the index of the graph that you want to remove: "))
            while graph_index < 0 or graph_index >= len(existing_graphs):
                graph_index: int = int(input("Invalid input! "
                                             "Please enter the index of the graph that you want to remove: "))

            graph_to_remove: Graph = existing_graphs[graph_index]
            existing_graphs.remove(graph_to_remove)

        option: int = int(input("Please enter a number: "))
        while option < 1 or option > 5:
            option: int = int(input("Sorry, invalid input! Please enter a number: "))

    sys.exit()


main()
