## 关于generator
* generator不但可以暂停，还可以接受回传值
        
        def jumping_range(up_to):
            """Generator for the sequence of integers from 0 to up_to, exclusive.
        
            Sending a value into the generator will shift the sequence by that amount.
            """
            index = 0
            while index < up_to:
                jump = yield index
                if jump is None:
                    jump = 1
                index += jump
    
    
        if __name__ == '__main__':
            iterator = jumping_range(5)
            print(next(iterator))  # 0
            print(iterator.send(2))  # 2
            print(next(iterator))  # 3
            print(iterator.send(-1))  # 2
            for x in iterator:
                print(x)  # 3, 4
* generator其实是一种**延迟计算**，不是一次性返回所有items，而是一次返回一个，让使用者按需索取；redis的`SCAN`指令和mysql的游标有类似效果
* 这和散列表动态分配空间的做法有异曲同工之妙：散列表为了不让某次导致重新分配空间的操作过于耗时，不是在分配好空间后一次性重新散列所有条目，而是一次搬迁
一部分，从而将成本分摊到每一次操作上，见[如何打造一个工业级水平的散列表](https://time.geekbang.org/column/article/64586)
* 老的文件搜索用的是常规方式(os.path.walk)，新的文件搜索用的是generator(os.work)，后者要省内存且友好的多
* 可参见[该贴](https://stackoverflow.com/a/102632/2272451)
                
## string和bytes的区别
* string是字符的序列，是人类可读的；bytes是字节的序列，计算机只能存储bytes
* bytes经解码后变成string才能被人类识别，string经编码变成bytes才能存储在计算机上
* 就像mp3经解码后才能被人类听懂，声音被编码成mp3后可以存储在计算机上
* `b'I am a string'`是bytes，被python打印后能被人类识别，仅仅是因为python默认用ascii解码它了

## time.time()其实计算的是现在到1970-1-1零时的时间差值(秒数)
* 即`datetime.datetime.utcnow() - t).total_seconds()`和`time.time()`几乎相等

## __init__ 和 __new__
* __new__用于**创建**实例，__init__用于**初始化**实例，详见[该贴](https://stackoverflow.com/a/674345/2272451)
* __new__是静态方法，第一个参数是cls；__init__是实例方法，第一个参数是self
* 三种单例模式：
 ```
 def Singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper
    
 class Singleton(object):
    def __new__(cls, *args, **kwargs): #static方法
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
 class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance
  ```


## object、class和metaclass
* class定义了object，metaclass定义了class：`MyClass = MetaClass(),my_object = MyClass()`
* 如果要统一改变对象的行为，可以改变类的定义；如果要改变统一类的行为，可以改变元类的定义
* 强烈建议看下[此贴](https://stackoverflow.com/a/6581949/2272451)

## 关于闭包
* 下面的代码，_impl函数中的fun变量是等到该函数执行的时候才evaluate的，详见[该贴](https://stackoverflow.com/a/30298338/2272451)
```
import math

mymath = dict()

for fun in ["sin", "cos"]:
    def _impl(val):
        print "calculating: %s" % fun
        return getattr(math, fun)(val)
    mymath[fun] = _impl


fun = 'tan'
# will print and calculate tan
print mymath["cos"](math.pi)
```
* 因此下面代码的执行结果是[9,9,9,9]，而不是[0,3,6,9]
```
def multi():
    return [lambda x : i*x for i in range(4)]
print([m(3) for m in multi()])
```

## 关于descriptor
* 强烈推荐看[该贴](http://ericplumb.com/blog/understanding-djangos-cached_property-decorator.html)，
重点：`cached_property`装饰的属性，首次调用是个`descriptor`，后面就被改成其他类性了，不是`descriptor`了，因此也不会再走`__get__'了
  ```class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res
  ```
  > 精彩描述：`instance.__dict__[self.func.__name__]` is where the magic happens. 
  >It asks `self.func` what its `__name__` is (in this case color), 
  >then uses the `instance's __dict__` attribute to replace itself with a property consisting
  >of the value calculated in step 1. In other words, before this statement is executed, 
  >`h.color` refers to a `cached_property` instance. After it is executed, `h.color` refers to 
  >the string "blue". What this instance is doing, at the very time it's being accessed, 
  >is replacing itself with the value calculated by the decorated method.

## json相比于binary，浪费空间
```
d = [3.5, 4.6] 
dd = [3.50000000, 4.688888888]
s = json.dumps(d)
ss = json.dumps(dd)
```
* d和dd的大小一样，但是ss就比s大多了

## base64编码之后还是bytes
* 详见[该贴](https://stackoverflow.com/questions/40000495/how-to-encode-bytes-in-json-json-dumps-throwing-a-typeerror)
* base64把`bytes`编码成`ASCII-only bytes`，而不是string
```
encoded = base64.encodebytes(b'data to be encoded') # encoded还是bytes
decoded_str = encoded.decode('ascii') # 解码成sring
```

## 关于subprocess的stdout和stderr
* 默认`subprocess.call()`输出到父进程的`stdout`和`stderr`，比如`ipython`里面输入`subprocess.call('ls')`，结果直接打印到console中   
* 传如`stdout=subprocess.PIPE`参数会把子进程的`stdout`导到`pipe`中而不是父进程的`stdout`中，如`ipython`里面输入
`subprocess.call('ls', stdout=subprocess.PIPE)`，结果不会打印到console中   
* 要想`subprocess.check_output`捕捉异常输出，需要传入参数`stderr=subprocess.PIPE`，否则抛出的异常CalledProcessError只
包含`stdout`，而`stderr`为空     

# numpy的array理解
```a = np.array([[1,2,3], [4,5,6]]) ```           
* ```a[:, 0] = array([1, 4]) ```  理解： 锁定第0列，取该列的所有行
* ```a[0,:]= array([1, 2, 3]) ``` 理解： 锁定第0行，取该行的所有列                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 