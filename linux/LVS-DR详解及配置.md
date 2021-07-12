DR

## 要求

1. Realserver 不能对arp协议做出响应，只有director才可以响应

## 实现要求
1. 在路由器上静态绑定vip对应到director的mac地址，此举需要路由器的支持
2. arptables：定制规则
3. linux内核中支持两个参数，arp_ignore,arp_announce

arp_ignore: 定义接受arp请求时的响应级别
- 0 默认的，只要本机的某个接口上配置了ip地址，你请求我就响应；
- 1 仅在请求的目标地址配置请求到达的接口上的时候，才给予响应；
- 2 3 4 5 6 7 8 未完待续

arp_announce: 定义将自己的地址向外通告时的通告级别
- 0 默认的，表示使用本地任何接口上的任何地址向外通告
- 1 试图仅向目标网络通告与其网络匹配的地址
- 2 仅向本地接口上的地址匹配的网络进行通告

## 配置

Director

eth0 DIP: 172.16.100.2

eth0:0 VIP: 172.16.100.1

RS1

eth0 rip1: 172.16.100.8

lo:0 vip: 172.16.100.1

RS2

eth0 rip2: 172.16.100.7

lo:0 vip: 172.16.100.1

## 操作

Director 桥接

ifconfig eth0:0 172.16.100.1/16 up

# ifconfig eth0:0 172.16.100.1 broadcaet 172.16.100.1 netmask 255.255.255.255 up

route add -host 172.16.100.1 dev eth0:0

RS 桥接，先配RIP，设置arp_ignore之后再配VIP；

rip配置后，ping测试一下

RS1

sysctl -w proc.sys.net.ipv4.conf.eth0.arp_announce=2

sysctl -w proc.sys.net.ipv4.conf.all.arp_announce=2

echo 1 > /proc/sys/net/ipv4/conf/eth0/arp_ignore

echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore

ifconfig lo:0 172.16.100.1 broadcast 172.16.100.1 netmask 255.255.255.255 up

route add -host 172.16.100.1 dev lo:0

重复设置一下RS2

配置ipvs

ipvsadm -C

ipvsadm -A -t 172.16.100.1:80 -s wlc

ipvsadm -a -t 172.16.100.1:80 -r 172.16.100.7 -g  -w 2

ipvsadm -a -t 172.16.100.1:80 -r 172.16.100.8 -g  -w 1
