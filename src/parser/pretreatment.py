"""
预处理模块
"""

import re


def remove_comment(al_script: str) -> str:
    """
    去除注释

    al_script中的注释包裹在 /* 和 */ 之间，因此可以用正则表达式进行匹配。
    """
    pattern: str = r"/\*.*?\*/"
    return re.sub(pattern, "", al_script)


def remove_empty_line(al_script: str) -> str:
    """
    去除空行
    """
    return "\n".join([line for line in al_script.split("\n") if line.strip()])


def do_pretreatment(al_script: str) -> str:
    """
    预处理
    """
    al_script = remove_comment(al_script)
    al_script = remove_empty_line(al_script)
    return al_script
