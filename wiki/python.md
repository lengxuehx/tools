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
* generator其实是一种**延迟计算**，不是一次性返回所有items，而是一次返回一个，让使用者按需索取
* 老的文件搜索用的是常规方式(os.path.walk)，新的文件搜索用的是generator(os.work)，后者要省内存且友好的多
* 可参见[该贴](https://stackoverflow.com/a/102632/2272451)
                
## string和bytes的区别
* string是字符的序列，是人类可读的；bytes是字节的序列，计算机只能存储bytes
* bytes经解码后变成string才能被人类识别，string经编码变成bytes才能存储在计算机上
* 就像mp3经解码后才能被人类听懂，声音被编码成mp3后可以存储在计算机上
* `b'I am a string'`是bytes，被python打印后能被人类识别，仅仅是因为python默认用ascii解码它了

## time.time()其实计算的是现在到1970-1-1零时的时间差值(秒数)
* 即`datetime.datetime.utcnow() - t).total_seconds()`和`time.time()`几乎相等