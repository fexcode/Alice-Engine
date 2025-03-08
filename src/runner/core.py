__import__("sys").path.append("./src")

from parser.alice_types import *
from parser.script_parser import tokenize, parse


def run_ast(ast: NodeTree):
    root: Node = ast.get_root()
    run_node(root)


def run_node(node: Node):
    context = {}  # 初始化上下文

    # 输出节点文本
    print(node.value)

    # 执行命令并更新上下文
    for cmd in node.cmds:
        if cmd.cmd == "@exit()@":
            exit()
        else:
            # 执行命令，并将更新后的上下文传回
            new_context = cmd.run(context)
            context.update(new_context if new_context else {})

    # 打印选项
    for i, opt in enumerate(node.options):
        print(f"{i+1}> {opt.opname}")

    # 若没有选项，直接退出
    if not node.options:
        return

    while True:
        result = input(">>> ")
        if result.isdigit():
            index = int(result)
            if 1 <= index < len(node.options)+1:
                run_node(node.options[index-1].node)
                break
            else:
                print("错误的选项")
                continue
        else:
            print("请输入选项前的数字")
            continue


if __name__ == "__main__":
    code = """
游戏名&
{
   "你好啊
   我是Fexcode
   欢迎通过邮箱联系我 2734664632@qq.com"
    #hi
    {
        你好啊
        #Exit{退出中@exit()@}
    }
    #exit{退出中@exit()@}
}
"""
    tks = tokenize(code)
    # for i, token in enumerate(tks):
    #     print(f"{i}> {token}")
    ast = parse(tks)
    run_ast(ast)
