__import__("sys").path.append("./src")
from logger import logger

from .alice_types.tree_types import *
from .alice_types.token_types import *
from .tokenizer import tokenize


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
    if not tokens.get_current().is_text():
        raise SyntaxError("节点文本缺失")

    # 获取原始文本并按行处理
    node_text = tokens.get_current().value
    lines = node_text.strip().split('\n')  # 按换行分割并去除首尾空行
    cleaned_lines = [line.strip() for line in lines]  # 去除每行首尾空格
    cleaned_text = '\n'.join(cleaned_lines)  # 重新组合为干净的文本

    block_node = Node(value=cleaned_text)  # 使用处理后的文本
    current_option: Option | None = None

    for i in range(len(tokens)):
        token = tokens.next()
        if token.value == "}":
            return block_node
            
        elif token.is_option():
            current_option = Option(opname=token.value[1:])
            if tokens.get_next().value != "{":
                block_node.add_option(current_option)
                
        elif token.is_command():
            block_node.add_cmd(Command(cmd=token.value[1:-1]))
            
        elif token.value == "{":
            tokens.next()
            node = parse_block(tokens)
            current_option.set_node(node)
            block_node.add_option(current_option)


if __name__ == "__main__":
    code = """
游戏名&
{
   "你好啊
   $s
   我是Fexcode(https:$k$kgithub.com$kFexcode)"
    #hi
    {
        你好啊
        @exit()@
        #Exit
    }
    #exit
}
"""
    tks = tokenize(code)
    for i, token in enumerate(tks):
        print(f"{i}> {token}")

    tree = parse(tks)

    print()
    print(tree)
