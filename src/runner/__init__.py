__import__("sys").path.append("./src")

from parser.alice_types import *
from parser.script_parser import tokenize, parse
from runner import run_ast


def run(code):
    tks = tokenize(code)
    # for i, token in enumerate(tks):
    #     print(f"{i}> {token}")
    ast = parse(tks)
    run_ast(ast)

if __name__ == "__main__":
    run("""
游戏名&
{
   "你好啊
   我是Fexcode
   欢迎通过邮箱联系我 2734664632@qq.com"
    #hi
    {
        你好啊
        #Exit
    }
    #exit
}
""")