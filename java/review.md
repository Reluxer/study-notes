1. ConcurrentHashMap JDK1.7 JDK1.8的实现方式？ 具体数据结构是什么样的？ 节点中的存储的数据是怎么设计的？为什么说1.8中的设计并发更好？ 好在哪里？ 好多少？数量级 ？

2. ThreadLocal的具体实现方式？ 为什么ThreadLocal用不好会内存溢出？ 是什么数据导致了内存溢出？

3. 候选人表示对容器比较熟悉，问了一个容器+泛型的问题，在函数设计过程中应该用downcast泛型还是用upcast泛型？为什么？

4. 缓存机制，应该如何设计缓存刷新策略？ 控制面和数据面直接如何数据传递？ 端上的缓存线程应该怎么设计？使用多少个线程如何判断和评估？

5. Spring IoC的实现原理是什么？ java里面的动态代理是怎么实现的？

6. 12亿个手机电话号码，如何快速毫秒级根据电话号码查找对应的省份和地市信息

跳表， 多叉树， 树结构以及每个节点中具体存什么数据;

7. 团队讨论问题别人对你的见解提出反对意见，你如何试图说服他? 与主管发送观点冲突了如何处理?

需要有激情

8. 假设一个事情做出效果需要2-3年，第一年因为效果不太好，主管打了非常不好的绩效，你认为主管做的对不对?

9. 人为什么要工作？ 你现在每天在做的工作，你为什么要做这些工作?

10. 你认为是什么样的工作表现好? 什么样的是工作表现不好？


11. java进程忽然消失了如何排查
https://www.cnblogs.com/myseries/p/11766804.html
https://www.cnblogs.com/rjzheng/p/11317889.html
可能有几种原因：
①、Java应用程序的问题：发生OOM导致进程Crash
最常见的是发生堆内存异常“java.lang.OutOfMemoryError: Java heap space”，排查步骤如下：

Step1: 查看JVM参数 -XX:+HeapDumpOnOutOfMemoryError 和 -XX:HeapDumpPath=*/java.hprof；
Step2: 根据HeapDumpPath指定的路径查看是否产生dump文件；
Step3: 若存在dump文件，使用Jhat、VisualVM等工具分析即可；
②、JVM出错：JVM或JDK自身的Bug导致进程Crash
当JVM出现致命错误时，会生成一个错误文件 hs_err_pid.log，其中包括了导致jvm crash的重要信息，可以通过分析该文件定位到导致crash的根源，从而改善以保证系统稳定。当出现crash时，该文件默认会生成到工作目录下，然而可以通过jvm参数-XX:ErrorFile指定生成路径。

③被操作系统OOM-Killer
Step1: 查看操作系统日志：sudo grep –color “java” /var/log/messages，确定Java进程是否被操作系统Kill；
Step2: 若被操作系统Kill，执行dmesg命令查看系统各进程资源占用情况，明确Java占用内存是否合理，以及是否有其它进程不合理的占用了大量内存空间；

@Autowired http://www.zzvips.com/article/178076.html determineautowirecandidate

