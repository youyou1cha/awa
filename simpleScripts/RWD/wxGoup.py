from wxauto import *

# 获取当前微信客户端
wx = WeChat()

# 获取会话列表
wx.GetSessionList()


###############################
# 1、获取默认窗口聊天信息
###############################
def get_default_window_messages():
    # 默认是微信窗口当前选中的窗口
    # 输出当前聊天窗口聊天消息
    msgs = wx.GetAllMessage
    for msg in msgs:
        print('%s : %s' % (msg[0], msg[1]))

    # 获取更多聊天记录
    wx.LoadMoreMessage()
    msgs = wx.GetAllMessage
    for msg in msgs:
        print('%s : %s' % (msg[0], msg[1]))


if __name__ == '__main__':
    get_default_window_messages()

