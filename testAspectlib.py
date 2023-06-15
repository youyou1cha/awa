# 目的是测试AOP面向方面编程的库aspectlib
# 用装饰器拦截函数，处理后返回

import aspectlib

@aspectlib.Aspect
def mock_open(*param):
    print('open file'+param[0])
    result = yield aspectlib.Proceed
    yield aspectlib.Return(result)

if __name__ == "__main__":
    with aspectlib.weave(open,mock_open):
        open('test.data')