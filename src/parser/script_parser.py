"""
## 使用方式

Alice Engine 引擎运行的基本单位是节点(Point)，节点分属着各自的选项(Choice)，选项再链接到各自的节点。<br>
当游戏开始时，游戏画面会显示此时的节点文本，下面会列出一系列选项。当玩家点击一个选项后，游戏会跳转到选项所对应的节点。

### 1. 节点

引擎使用如下的语法定义一个节点：

```as
{
    节点文本
    #选项一...
    #选项二...
    #...
}
```

其中，换行和缩进是可选的，合适的换行和缩进可以让脚本文件更具可读性。

#### 在节点中添加Python代码
你可以在脚本的节点添加 python 代码，当游戏来到一节点时，其相应的代码会被执行。<br>
python 代码用一对`@`括起来

下面为调用示例：
```as
@a = 3@
```
在 python 代码调用中，你可以定义和调用变量，还可以调用部分 python 内置函数(注意：为了游戏运行的安全性和稳定性，部分 python 内置函数将被屏蔽从而避免被调用)<br>
此外，你还可以通过使用`@api.func()@`格式调用引擎提供的接口库 api，来调用引擎的接口函数。

### 2. 选项

选项的语法为：

```
#选项名
{
    对应的节点...
}
```

### 3. 转义字符

转义字符是如同`$a`、`$n`等的字符串，用以替代一些字符，从而能被解释器正常解释。解释前，它们将被转换为其原本的字符。<br>
如果你的游戏文本中含有`{`、`}`和`#`等脚本语言的保留字符，请用转义字符替代它们，以免被脚本文件解释器错误解释。<br>
此外，如果你的游戏文本中含有空格键、换行符等，我们同样推荐你使用转义字符替代它们，从而降低脚本文件解释器出现错误的概率。

现有的转义字符如下：

> `$n` : 换行符 <br> > `$s` : 空格 <br> > `$t` : 制表符(`\t`) <br> > `$p` : 井号 <br> > `$l` : 左大括号 <br> > `$r` : 右大括号 <br> > `$b` : 回车(`\r`) <br> > `$k` : 斜杠(`/`) <br>

<br>
目前共有两个接口函数：echo 和 create_gui。echo(text)的功能和 python 内置函数 print 类似，其将接受一个字符串参数，并在控制台打印出来；而 create_gui()函数则会创建并返回一个新的 GUI 对象。

### 4. 注释

你还可以在脚本中添加注释，以提高代码的可读性和可维护性。<br>
注释以`/*`开始，以`*/`结束。

以下是一个示例注释：

```
/*这是一段注释*/
```

### 5. 游戏名

最后，不要忘记在脚本文件的开头加上游戏名。

设置游戏名的格式为：
```as
游戏名&
```
"""

"""
游戏脚本解释器
"""
from parser.alice_types.tree_types import *
import pretreatment
import re


def tokenize(code: str) -> list:
    """
    词法分析

    注意: 解析的时候不用考虑注释

    token解析规则:
    #后的内容为选项名,#连同选项名为一个token
    {与} 为单独的token
    @与@ 之间的内容为单独的token
    &前面的内容为游戏名,为单独的token
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

    return tokens


def parse(tokens: list[str]) -> NodeTree:
    """
    解析函数
    """
    # TODO


if __name__ == "__main__":
    code = '游戏脚本示例&{你$n好#选项一{这是文本B#退出}#选项二{这是文本C#退出}#选项三{这是文本D@echo("Hello,world!")@#退出}}'
    tree = parse(code)
    print(tree)
