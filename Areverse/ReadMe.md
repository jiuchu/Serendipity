# IOS逆向

### 适用于使用常规方法hook不到数据，可以参考下面的文章
* 相关参考文章：https://bbs.kanxue.com/thread-278175-1.htm
* 大佬库：https://github.com/jitcor/frida-ios-cipher


## 操作指令
### MD5
```
frida-trace -UF -i CC_MD5 -o md5.txt
```

### SHA256
```
frida-trace -UF -i CC_SHA256 -o sha256.txt
```


### 同时HOOK并分析多个，日志合并收集【多合一版本】
```
frida-trace -UF -i CC_MD5 -i CC_SHA1 -i CCCrypt -i SecKeyEncrypt -i CC_SHA256 >> multi_trace_log.txt
```

### 使用github大佬库进行hook【已对常见的加密算法做了整合】
```
frida -U -p 35295 -l iosciper.js -o fan.txt
```