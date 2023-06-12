#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#输入模块的名称
mod_name = input("请输入模块名称>>>")

# 输入函数or方法的名称
func_name = input("请输入模块名称>>>")

# 查看输入的内容以及数据类型
print(mod_name,type(mod_name))

# 通过__import__的方式导入模块，并赋值给dd
dd = __import__(mod_name)

# 导入模块中的方法
target_func = getattr(dd,func_name)

# 查看target_func和dd.f1的内存地址
print(id(target_func),id(dd.f1))

# 执行target_func 函数
result = target_func()
# 执行f1()函数
ret = dd.f1()

# 输出函数的返回值
print(ret)

# 执行reflection.py

