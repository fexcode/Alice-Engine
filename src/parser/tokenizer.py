import pretreatment
from alice_types.token_types import Token,Tokens

def tokenize(code: str) -> Tokens:
    """
    词法分析

    注意: 解析的时候不用考虑注释

    token解析规则:
    #后的内容为选项名,#连同选项名为一个token
    {与} 为单独的token
    @与@ 之间的内容为单独的token
    &后面的内容为游戏名,为单独的token
    其他内容为文本内容,连在一起的文本内容会被合并为一个token

    游戏脚本: "游戏脚本示例&{你好#选项一{@a=3@}}"
    解析结果(空格分割): 游戏脚本示例& { 你好 #选项一 { @a=3@ } }

    """
    # 预处理
    code = pretreatment.do_pretreatment(code)

    # 解析
    tokens = []
    token = ""
    in_string = False
    for char in code:
        if in_string:
            if char == '"':
                in_string = False
                tokens.append(token)
                token = ""
            else:
                token += char
            continue
        if char == '"':
            in_string = True
            token += char
            continue
        if char == "#":
            if token:
                tokens.append(token)
                token = ""
            tokens.append(char)
            continue
        if char == "{":
            if token:
                tokens.append(token)
                token = ""
            tokens.append(char)
            continue
        if char == "}":
            if token:
                tokens.append(token)
                token = ""
            tokens.append(char)
            continue
        if char == "@":
            if token:
                tokens.append(token)
                token = ""
            tokens.append(char)
            continue
        if char == "&":
            if token:
                tokens.append(token)
                token = ""
            tokens.append(char)
            continue
        if char == " ":
            if token:
                tokens.append(token)
                token = ""
            continue
        token += char

    if token:
        tokens.append(token)

    # 合并 token
    for i in tokens:
        if i == "#":
            tokens[tokens.index(i)] = "#" + (opname := tokens[tokens.index(i) + 1])
            tokens.remove(opname)
        if i == "&":
            tokens[tokens.index(i)] = "&" + (gamename := tokens[tokens.index(i) - 1])
            tokens.remove(gamename)

        if i == "@":
            # 合并 @ 与 @ 之间的内容
            j = tokens.index(i)
            while j < len(tokens) - 1 and tokens[j + 1] != "@":
                j += 1
            tokens[tokens.index(i) : j + 2] = ["".join(tokens[tokens.index(i) : j + 2])]

    # 处理转义字符
    # 看看每个token中是否包含转义字符,仅替换转义字符
    for i in range(len(tokens)):
        if "$n" in tokens[i]:
            tokens[i] = tokens[i].replace("$n", "\n")
        if "$s" in tokens[i]:
            tokens[i] = tokens[i].replace("$s", " ")
        if "$t" in tokens[i]:
            tokens[i] = tokens[i].replace("$t", "\t")
        if "$p" in tokens[i]:
            tokens[i] = tokens[i].replace("$p", "#")
        if "$l" in tokens[i]:
            tokens[i] = tokens[i].replace("$l", "{")
        if "$r" in tokens[i]:
            tokens[i] = tokens[i].replace("$r", "}")
        if "$b" in tokens[i]:
            tokens[i] = tokens[i].replace("$b", "\r")
        if "$k" in tokens[i]:
            tokens[i] = tokens[i].replace("$k", "/")

    # 构造 token
    tokens = [Token(token) for token in tokens]

    return Tokens(tokens)
