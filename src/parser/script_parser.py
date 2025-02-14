__import__("sys").path.append("./src")
from logger import logger

from alice_types.tree_types import *
from alice_types.token_types import *
from tokenizer import tokenize


def parse(tokens: Tokens) -> NodeTree:
    # 解析游戏名
    for token in tokens:
        if token.is_game_name():
            game_name = token.value[1:]
            tokens.next()  # 指针向后移动
            break
    else:
        game_name = "未命名游戏"

    if tokens.get_current().value == "{":
        tokens.next()  # 指针向后移动
    else:
        raise SyntaxError("游戏名后未找到根节点")

    # 解析根节点
    root_node = parse_block(Tokens(tokens.tokens, pointer=tokens.pointer))
    tree = NodeTree(root=root_node, game_name=game_name)
    return tree


def parse_block(tokens: Tokens) -> Node:
    # 在parse中,根节点的{已经被过滤了,所以当前token就是节点文本
    if not tokens.get_current().is_text():
        raise SyntaxError("节点文本缺失")
        pass

    node_text = ""

    node_text = tokens.get_current().value

    block_node = Node(value=node_text)
    current_option: Option | None = None

    # 其实并不需要i变量,这里只是防止程序莫名其妙地死循环,也可以改成while True:
    for i in range(len(tokens)):
        logger.log(NodeTree(root=block_node, game_name=""))
        # logger.log("=> " + current_option.opname if current_option else "None")
        token = tokens.next()
        # logger.log(f"token: {token}, pointer: {tokens.pointer}")

        if token.value == "}":
            return block_node
        elif token.is_option():
            current_option = Option(opname=token.value[1:])
            if tokens.get_next().value != "{":
                # 当选项后面没有{时,说明选项后面没有节点,选项选择后无需跳转,程序停止
                block_node.add_option(current_option)
            
        elif token.is_command():
            block_node.add_cmd(Command(cmd=token.value[1:-1]))
        elif token.value == "{":
            # 遇到{时,说明选项后面有节点,需要递归解析节点
            tokens.next()  # 指针向后移动,过滤{
            node = parse_block(tokens)
            current_option.set_node(node)
            block_node.add_option(current_option)


if __name__ == "__main__":
    code = """
游戏名&
{
    你好啊$s我是Fexcode(https:$k$kgithub.com$kFexcode)
    #hi
    {
        你好啊
        @exit()@
        #Exit
    }
    #exit
}
"""
    print(str(tks := tokenize(code)))
    tree = parse(tks)

    print()
    print(tree)
