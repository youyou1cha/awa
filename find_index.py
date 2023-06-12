# 基于反射模拟web框架路由系统
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

url = input("请输入url:")
target_module,target_func = url.split('/')

m = __import__('lib.' + target_module,fromlist=True)

if hasattr(m,target_func):
    target_func = getattr(m,target_func)
    r = target_func()
    print(r)
else:
    print("404")