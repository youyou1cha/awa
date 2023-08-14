'''
定一个只包含括号字符（小括号：’(‘和’)’，中括号：’[‘和’]’，以及大括号：’{‘和’}’）的字符串，要求程序给出字符串中的括号是否正确嵌套以及是否正确关闭。空串认为是符合要求的。
'''
def is_valid_parentheses(s:str):
    stack = []
    mapping = {')':'(',']':'[','}':'{'}

    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            return False

    return len(stack) == 0


if __name__ == '__main__':
    # 测试
    test_strings = [
        "",
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[]}",
        "{{[()]}}"
    ]

    for s in test_strings:
        print(f"string : '{s}' --> Valid : {is_valid_parentheses(s)}")