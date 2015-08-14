## 钩子函数，规则链

    1. PREROUTING (路由前)
    2. INPUT (数据包流入口)
    3. FORWARD (转发管卡)
    4. OUTPUT(数据包出口)
    5. POSTROUTING（路由后）

[![Alt text](/imgs/01.jpg)](http://blog.chinaunix.net/uid-23069658-id-3160506.html)

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

|杂项　|　　　　　　　　VS/NAT　|　　　 VS/TUN　　|　　　　VS/DR |
|------|------------------------|-----------------|--------------|
|服务器操作系统　　　|　任意　　　|　　　支持隧道　　　|　多数(支持Non-arp )|
|服务器网络　　　　　|　私有网络　|　　　局域网/广域网　|　局域网|
|服务器数目(100M网络)| 10-20　　　|　　　100　　　　　|　　多(100)|
|服务器网关　　|　　　　负载均衡器|　　　自己的路由　|　　　自己的路由|
|效率　　|　　　　　　　一般　　　|　　　高　　　　　|　　　最高|

## More...

- [LVS的三种模式区别详解](http://blog.chinaunix.net/uid-29431701-id-4082013.html)
- [(一)洞悉linux下的Netfilter&iptables：什么是Netfilter?](http://blog.chinaunix.net/uid-23069658-id-3160506.html)
- [iptables详解](http://blog.chinaunix.net/uid-26495963-id-3279216.html)