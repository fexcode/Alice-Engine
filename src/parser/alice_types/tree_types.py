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
        nodes: list["Node"] | None = None,
    ):
        self.opname = opname  # 选项名
        self.nodes = nodes or []  # 选项节点

    def add_node(self, node: "Node"):
        self.nodes.append(node)


class Node:
    def __init__(
        self,
        value: str = "",
        options: list[Option] | None = None,
        cmds: list[Command] | None = None,
    ):
        self.value = value  # 节点值
        self.options = options or []
        self.cmds = cmds or []

    def add_option(self, option: Option):
        self.options.append(option)

    def add_cmd(self, cmd: Command):
        self.cmds.append(cmd)


class NodeTree:
    def __init__(self, root: Node, game_name: str = ""):
        self.__root = root
        self.game_name = game_name

    def __str__(self):
        return self._print_node(self.root, 0)

    def _print_node(self, node: Node, indent: int):
        # 生成缩进
        indent_str = " " * indent
        # 打印节点值
        output = f"{indent_str}节点：{node.value}\n"
        # 打印命令
        for cmd in node.cmds:
            output += f"{indent_str}  命令：{cmd.cmd}\n"
        # 递归打印子节点
        for option in node.options:
            output += f"{indent_str}选项：{option.opname}\n"
            for child_node in option.nodes:
                output += self._print_node(child_node, indent + 2)
        return output

    def __repr__(self):
        return str(self)
    
    def set_root(self, root: Node):
        self.__root = root
