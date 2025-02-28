__import__("sys").path.append("./src")

from parser.alice_types import *
from parser.script_parser import tokenize, parse


def run_ast(ast: NodeTree):
    root: Node = ast.get_root()
    run_node(root)


def run_node(node: Node):
    # 输出节点文本
    print(node.value)

    # 运行命令
    for cmd in node.cmds:
        if cmd.cmd == "@exit()@":
            exit()
        else:
            cmd.run()

    # 打印选项
    for i, opt in enumerate(node.options):
        print(f"{i+1}> {opt.opname}")

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
