
获取heap dump文件的途径

1. 开启jmx，通过jconsole查看即可
jconsole - MBean - com.sun.management - HotSpotDiagnostic - 操作 - dumpHeap(String outputFile, boolean live)
outputFile的扩展名为.hprof

2. 
jmap -dump:live,format=b,file=heap-dump.bin <pid>
pid：JVM进程的id，可以使用jps 或者 ps 命令来查找

3. 
jcmd <pid> GC.heap_dump <file-path>

4. 发生oom时自动生成文件
java -Xms10m -Xmx10m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/ com.example.demo.oom.TestOOM 


shallow heap VS retained heap

shallow heap: 直译就是浅层堆，其实就是这个对象实际占用的堆大小。

retained heap:直译过来是保留堆，一般会大于或者等于shallow heap。如果这个对象被删除了（GC回收掉），能节省出多少内存，这个值就是所谓的retained heap

参考： https://blog.csdn.net/wwlwwy89/article/details/74330544

