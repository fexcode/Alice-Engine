import unittest
from tree_types import *
from token_types import *


class TestAliceTypes(unittest.TestCase):
    def test_Command_type(self):
        cmd = Command("author=fexcode")
        self.assertEqual(str(cmd), "author=fexcode")

    def test_Option_type(self):
        opt = Option("this is an option")
        node1 = Node("node1")
        node2 = Node("node2")
        node3 = Node("node3")

        opt.add_node(node1)
        opt.add_node(node2)
        opt.add_node(node3)

        self.assertEqual(len(opt.nodes), 3)
        self.assertEqual(opt.nodes[0], node1)
        self.assertEqual(opt.nodes[1], node2)
        self.assertEqual(opt.nodes[2], node3)

    def test_Node_type(self):
        node = Node("this is a node")
        opt1 = Option("option1")
        opt2 = Option("option2")
        cmd1 = Command("cmd1")
        cmd2 = Command("cmd2")

        node.add_option(opt1)
        node.add_option(opt2)
        node.add_cmd(cmd1)
        node.add_cmd(cmd2)

        self.assertEqual(len(node.options), 2)
        self.assertEqual(node.options[0], opt1)
        self.assertEqual(node.options[1], opt2)
        self.assertEqual(len(node.cmds), 2)
        self.assertEqual(node.cmds[0], cmd1)
        self.assertEqual(node.cmds[1], cmd2)

    def test_NodeTree_type(self):
        tree = NodeTree("this is a tree")
        node1 = Node("node1")
        op1 = Option("op1")
        cmd1 = Command("cmd1")
        node1.add_option(op1)
        node1.add_cmd(cmd1)
        tree.set_root(node1)

    def test_Tokens_type(self):
        t1 = Token("hello")
        t2 = Token("#option")
        t3 = Token("@command@")
        t4 = Token("{")
        t5 = Token("}")
        self.assertTrue(t1.is_text())
        self.assertTrue(t2.is_option())
        self.assertTrue(t3.is_command())
        self.assertTrue(not t4._is_not_block())
        self.assertTrue(not t5._is_not_block())
        self.assertTrue(t1._is_not_block())
        self.assertTrue(t2._is_not_block())
        self.assertTrue(t3._is_not_block())

    def test_Tokens_type(self):
        t1 = Token("hello")
        t2 = Token("#option")
        t3 = Token("@command@")
        t4 = Token("{")
        t5 = Token("}")
        target = [t1, t2, t3, t4, t5]
        tokens = Tokens([t1, t2, t3, t4])
        tokens.append(t5)
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0], t1)
        self.assertEqual(tokens[1], t2)
        self.assertEqual(tokens[2], t3)
        self.assertEqual(tokens[3], t4)
        self.assertEqual(tokens[4], t5)
        for token in tokens:
            self.assertTrue(token in target)
        self.assertEqual(tokens.get_current(), t1)
        self.assertEqual(tokens.next(), t2)
        self.assertEqual(tokens.next(), t3)
        self.assertEqual(tokens.next(), t4)
        self.assertEqual(tokens.next(), t5)
        self.assertEqual(tokens.get_current(), t5)
        self.assertEqual(tokens.get_next(), None)
        self.assertEqual(tokens.get_current(), t5)


if __name__ == "__main__":
    unittest.main()
