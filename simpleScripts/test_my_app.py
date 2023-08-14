import time

from playwright.sync_api import sync_playwright

# 远程 Chrome 的地址和端口
remote_address = 'http://localhost'
remote_port = 9222

# 初始化 Playwright
with sync_playwright() as p:
    # 连接到远程 Chrome 实例
    browser = p.chromium.connect_over_cdp(
        f'{remote_address}:{remote_port}',
        # 如果需要其他选项，请在这里添加
    )

    # 打开一个新的页面
    page = browser.new_page()

    # 在页面上执行操作
    page.goto('https://www.baidu.com')
    # 这里可以添加更多操作
    # 获取所有页面的句柄
    all_pages = browser.contexts
    print(all_pages)

    # 遍历句柄并执行操作
    for page in all_pages:
        print("Page title:", page.title())
        # 这里可以添加更多操作
    # 关闭页面和浏览器
    page.close()
    browser.close()
