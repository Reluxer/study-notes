钩子函数，规则链

    1. PREROUTING (路由前)
    2. INPUT (数据包流入口)
    3. FORWARD (转发管卡)
    4. OUTPUT(数据包出口)
    5. POSTROUTING（路由后）

[![Alt text](/imgs/01.jpg)](http://blog.chinaunix.net/uid-23069658-id-3160506.html)

对于收到的每个数据包，都从“A”点进来，经过路由判决，如果是发送给本机的就经过“B”点，然后往协议栈的上层继续传递；否则，如果该数据包的目的地是不本机，那么就经过“C”点，然后顺着“E”点将该包转发出去。

对于发送的每个数据包，首先也有一个路由判决，以确定该包是从哪个接口出去，然后经过“D”点，最后也是顺着“E”点将该包发送出去。

LVS
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