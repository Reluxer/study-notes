## 钩子函数，规则链

1. PREROUTING (路由前)
2. INPUT (数据包流入口)
3. FORWARD (转发管卡)
4. OUTPUT(数据包出口)
5. POSTROUTING（路由后）

[![Alt text](../assets/01.jpg)](http://blog.chinaunix.net/uid-23069658-id-3160506.html)

对于收到的每个数据包，都从“A”点进来，经过路由判决，如果是发送给本机的就经过“B”点，然后往协议栈的上层继续传递；否则，如果该数据包的目的地是不本机，那么就经过“C”点，然后顺着“E”点将该包转发出去。

对于发送的每个数据包，首先也有一个路由判决，以确定该包是从哪个接口出去，然后经过“D”点，最后也是顺着“E”点将该包发送出去。

## LVS

Linux Virtual Server，工作于内核中，Input链上，与iptables冲突，两者不能共用
- ipvsadm：管理集群服务的命令行工具，用户空间
- ipvs:内核

Client
- CIP:Client IP,互联网上的某台主机/客户端的IP

Director
- VIP: virtual IP,与外网通讯的IP
- DIP: 与后端主机通讯的IP

Real server
- RIP:后端主机的IP

Schedule Method
- LVS-NAT：Network address translation,地址转换
- LVS-DR: Direct routing,直接路由
- LVS-TUN: IP tunneling,隧道

## NAT

- 集群节点和Director必须在同一个IP网络中
- RIP通常是私有地址，仅用于各集群节点间的通信
- Director位于Client和Real Server之间，并负责处理进出的所有通信
- RealServer必须将网关指向DIP
- 支持端口映射
- RealServer可以使用任意OS
- 较大规模的应用场景中，单独的Director易成为系统瓶颈

## DR

- 集群节点和director必须在同一个物理网络中
- RIP可以使用公网地址，实现便捷的远程管理和监控
- Director仅负责处理入站请求，响应报文则由realserver直接发往客户端
- realserver不能将网关指向DIP
- 不支持端口映射
- 集群节点可以使用大多数的操作系统，因为要求操作系统能够隐藏VIP
- DR Director相比NAT能处理更多的realserver

## TUN

- 集群节点可以跨越Internet
- RIP必须是公网地址
- Director仅负责处理入站请求，响应报文则由realserver直接发往客户端
- realserver网关不能指向director
- 只有支持隧道功能的OS才能用于realserver
- 不支持端口映射

## 三种IP负载均衡技术的优缺点比较

|杂项|VS/NAT|VS/TUN|VS/DR|
|------|------------------------|-----------------|--------------|
|服务器操作系统|任意|支持隧道|多数(支持Non-arp)|
|服务器网络|私有网络|局域网/广域网|局域网|
|服务器数目(100M网络)|10-20|100|多(100)|
|服务器网关|负载均衡器|自己的路由|自己的路由|
|效率|一般|高|最高|


## 调度方法

### 固定调度(静态调度)

1. 轮叫调度(Round Robin, rr)

调度器通过“轮叫”调度算法将外部请求按顺序轮流分配到集群中的真实服务器上，它均等地对待每一台服务器，而不管服务器上实际的连接数和系统负载。

2. 加权轮叫(Weighted Round Robin, wrr)

调度器通过“加权轮叫”调度算法根据真实服务器的不同处理能力来调度访问请求。这样可以保证处理能力强的服务器能处理更多的访问流量。调度器可以自动问询真实服务器的负载情况，并动态地调整其权值。

3. 源地址散列(Source Hashing, SH)

“源地址散列”调度算法根据请求的源IP地址，作为散列键（Hash Key）从静态分配的散列表找出对应的服务器，若该服务器是可用的且未超载，将请求发送到该服务器，否则返回空。

4. 目标地址散列(Destination Hashing, DH)

“目标地址散列”调度算法根据请求的目标IP地址，作为散列键（Hash Key）从静态分配的散列表找出对应的服务器，若该服务器是可用的且未超载，将请求发送到该服务器，否则返回空。

### 动态调度

5. 最少链接(Least Connections, LC)

调度器通过“最少连接”调度算法动态地将网络请求调度到已建立的链接数最少的服务器上。如果集群系统的真实服务器具有相近的系统性能，采用“最小连接”调度算法可以较好地均衡负载。min{active*256+inactive}.

6. 加权最少链接(Weighted Least Connections, WLC)

在集群系统中的服务器性能差异较大的情况下，调度器采用“加权最少链接”调度算法优化负载均衡性能，具有较高权值的服务器将承受较大比例的活动连接负载。调度器可以自动问询真实服务器的负载情况，并动态地调整其权值。min{active*256+inactive/weight}.

7. 最短的期望的延迟(Shortest Expected Delay Scheduling SED, SED)

基于wlc算法。这个必须举例来说了
ABC三台机器分别权重123 ，连接数也分别是123。那么如果使用WLC算法的话一个新请求进入时它可能会分给ABC中的任意一个。使用sed算法后会进行这样一个运算
A(1+1)/1
B(1+2)/2
C(1+3)/3
根据运算结果，把连接交给C 。

8. 最少队列调度(Never Queue Scheduling NQ, NQ)

无需队列。如果有台 realserver的连接数＝0就直接分配过去，不需要在进行sed运算

9. 基于局部性的最少链接(Locality-Based Least Connections, LBLC)

“基于局部性的最少链接”调度算法是针对目标IP地址的负载均衡，目前主要用于Cache集群系统。该算法根据请求的目标IP地址找出该目标IP地址最近使用的服务器，若该服务器是可用的且没有超载，将请求发送到该服务器；若服务器不存在，或者该服务器超载且有服务器处于一半的工作负载，则用“最少链接” 的原则选出一个可用的服务器，将请求发送到该服务器。

10. 带复制的基于局部性最少链接(Locality-Based Least Connections with Replication, LBLCR)

“带复制的基于局部性最少链接”调度算法也是针对目标IP地址的负载均衡，目前主要用于Cache集群系统。它与LBLC算法的不同之处是它要维护从一个目标 IP地址到一组服务器的映射，而LBLC算法维护从一个目标IP地址到一台服务器的映射。该算法根据请求的目标IP地址找出该目标IP地址对应的服务器组，按“最小连接”原则从服务器组中选出一台服务器，若服务器没有超载，将请求发送到该服务器；若服务器超载，则按“最小连接”原则从这个集群中选出一台服务器，将该服务器加入到服务器组中，将请求发送到该服务器。同时，当该服务器组有一段时间没有被修改，将最忙的服务器从服务器组中删除，以降低复制的程度。

一般采用wlc算法.

## More...

- [LVS的三种模式区别详解](http://blog.chinaunix.net/uid-29431701-id-4082013.html)
- [(一)洞悉linux下的Netfilter&iptables：什么是Netfilter?](http://blog.chinaunix.net/uid-23069658-id-3160506.html)
- [iptables详解](http://blog.chinaunix.net/uid-26495963-id-3279216.html)
- [LVS三种工作模式、十种调度算法介绍](http://www.xmydlinux.org/201102/331.html)