class Command:
    def __init__(self, cmd):
        self.cmd = cmd  # 命令名

    def __str__(self):
        return self.cmd

    def __repr__(self):
        return self.__str__()

    def run(self):
        exec(self.cmd)


class Option:
    def __init__(
        self,
        opname,
        node=None,
    ):
        self.opname = opname  # 选项名
        self.node = node  # 选项节点

    def set_node(self, node: "Node"):
        self.node = node


class Node:
    def __init__(
        self,
        value: str = "",
        options: list[Option] | None = None,
        cmds: list[Command] | None = None,
    ):
        self.value = value  # 节点值
        self.options = options or list()
        self.cmds = cmds or list()

    def add_option(self, option: Option):
        self.options.insert(0, option)  # 首插入，保证先处理的选项在前面

    def add_cmd(self, cmd: Command):
        self.cmds.append(cmd)


class NodeTree:
    def __init__(self, root: Node, game_name: str = ""):
        self.__root = root
        self.game_name = game_name

    def __str__(self):
        return self._print_node(self.__root)

    def _print_node(self, root: Node, indent: int = 0):
        # 递归打印节点及其子节点
        s = f"{' '*indent}{root.value}\n"
        for option in root.options:
            s += f"{' '*indent}  {option.opname}\n"
            if option.node:
                s += self._print_node(option.node, indent + 2)
                for cmd in root.cmds:
                    s += f"{' '*indent}    {cmd.cmd}\n"

        return s

    def __repr__(self):
        return str(self)

    def set_root(self, root: Node):
        self.__root = root
