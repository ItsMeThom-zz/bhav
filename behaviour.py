from enum import Enum
from abc import abstractmethod


class NodeState(Enum):
    FAILURE = -1
    READY = 0
    RUNNING = 1
    SUCCESS = 2


class Node:
    state = NodeState.READY
    children = []

    def __init__(self, *children):
        self.state = NodeState.READY
        self.children = [c for c in children]
        self.parent_tree = None

    def reset(self):
        if self.state is not NodeState.RUNNING:
            self.state = NodeState.READY
        for child in self.children:
            if isinstance(child, Node):
                child.reset()

    def set_tree(self, tree):
        print("setting tree to {}".format(tree))
        self.parent_tree = tree
        for child in self.children:
            if isinstance(child, Node):
                print("set child")
                child.set_tree(tree)

    @abstractmethod
    def check(self):
        pass


class Action(Node):
    """ Perform some external function like a move() or shoot()
    or whatever. """

    def __init__(self, action, *children):
        if not callable(action):
            raise TypeError("{} is not a callable func or object"
                            .format(action.__name__))
        self.action = action
        super().__init__(*children)

    def check(self):
        response = self.action()  # TODO: Probably some scope args go here.
        if response or response is None:
            return NodeState.SUCCESS
        return NodeState.FAILURE


class If(Node):
    """ Test an external condition to see if we progress
    down this portion of the tree.
    If the conditional fails return failure state.
    Otherwise recursively return the condition of the
    single child. """

    def __init__(self, condition, *children):
        if not callable(condition):
            raise TypeError("{} is not a callable func or object"
                            .format(condition.__name__))
        self.condition_test = condition
        super().__init__(*children)

    def check(self):
        if not self.condition_test():
            self.state = NodeState.FAILURE
            return self.state
        self.state = self.children[0].check()
        return self.state


class Sequence(Node):
    """ Check all children in order. Return success when all checked,
    otherwise return state of last checked child for example (Running,
    or Failure)"""

    def __init__(self, *children):
        self.current_child = -1
        super().__init__(*children)

    def check(self):
        self.current_child += 1
        if self.current_child > len(self.children):
            # all nodes completed, reset.
            self.state = NodeState.SUCCESS
            self.current_child = -1
            return self.state
        # Current child might return RUNNING or FAILURE.
        self.state = self.children[self.current_child].check()
        return self.state


class Selector(Node):
    """ Tries each child node in order until one returns Success or Running."""

    def __init__(self, *children):
        super().__init__(*children)

    def check(self):
        # TODO: Will we need to retain the last child between ticks?
        for child in self.children:
            child_status = child.check()
            if child_status is not NodeState.FAILURE:
                self.state = child_status
                return self.state
        self.state = NodeState.FAILURE
        return self.state


class Inverter(Node):
    """ Inverts the result of its child node in Success/Failure states. Can
    only have a single child. In the case of a child in Running state this
    node returns Running.
    """

    def check(self):
        child_state = self.children[0].check()
        if child_state is NodeState.SUCCESS:
            self.state = NodeState.FAILURE
        elif child_state is NodeState.FAILURE:
            self.state = NodeState.SUCCESS
        else:
            self.state = child_state
        return self.state


class Tree:
    """ Tree stores the root node and is responsible for
    dispatching the check() call that selects an action and for
    resetting the node values to NodeState.READY. """
    root_node = None

    def __init__(self, root):
        self.set_root(root)
        self.context = {}

    def set_root(self, node):
        node.set_tree(self)
        self.root_node = node

    def tick(self):
        self.root_node.reset()
        state = self.root_node.check()
        print("state is: {}".format(state))









