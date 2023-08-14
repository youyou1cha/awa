'''

为了表示给定链表中的循环，我们使用一个整数 pos 来表示链表中尾巴连接到的位置（0 索引）。如果 pos 为 -1，则链表中没有循环。
ChatGPT
理解了，你是在描述一个链表中可能存在循环的情况，并且使用整数 pos 来表示循环的连接位置。如果 pos 为 -1，则表示链表没有循环。

如果你想要判断链表是否有循环并找到循环的起始节点，可以使用弗洛伊德的循环检测算法（Floyd's Cycle Detection Algorithm），也叫做龟兔赛跑算法（Tortoise and Hare Algorithm）。
'''


class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


def detectCycle(head: ListNode):
    if not head or not head.next:
        return None

    slow = head
    fast = head
    # fast 开始跑 slow在后面跑。当跑到结尾的时候就范围None
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            break

    if not fast or not fast.next:
        return None

    # slow 要么撵上了 开始重新跑。当slow = fast的时候推出 说明成环
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return  slow


# 创建

