## 基本配置

Client
- CIP:Client IP,互联网上的某台主机/客户端的IP


Director(vmware centos 6.4)
- VIP: 192.168.1.133 桥接/NAT
- DIP: 192.168.10.7 host only

Real server-Web server(vmware)
- RIP1:192.168.10.8
- RIP2:192.168.10.9

各节点之间的时间偏差不应该超出一秒钟:NTP:Network Time Protocol
各RS配置同步director的时间 配置ntpd服务 定义成clock计划
## ipvsadm 用法

### 管理集群服务

- 添加 -A -t|u|f service-address [-s scheduler]

    - -t TCP协议的集群 service-address为IP:PORT
    - -u UDP协议的集群 service-address为IP:PORT
    - -f Firewallmark,FWM,防火墙标记，LVS的持久连接service-address为防火墙标记号

- 修改 -E -t|u|f service-address [-s scheduler]

- 删除 -D -t|u|f service-address

- -C:清空ipvs规则
- -S:保存规则，使用输出重定向 ipvsadm -S > /path/to/somefile 或者service ipvsadm save
- -R:导入规则，使用输出重定向 ipvsadm -R < /path/from/somefile

### 管理集群服务中的RS

- 添加 -a  -t|u|f service-address -r server-address [-g|i|m] [-w weight]

    - service-address:事先定义好的某集群服务
    - server-address:某个RS的地址，在NAT模型中，可使用IP:PORT实现端口映射
    - g|i|m LVS模型 g,DR;i,TUN;m,NAT;默认-g
    - w:定义服务器权重

- 修改 -e

- 删除 -d -t|u|f service-address -r server-address

### 查看

- -L|l
    -n: 数字格式显示主机地址和端口
    -c: 显示当前IPVS的连接状况
    --stats: 统计数据
    --rate: 速率
    --timeout显示会话超时时间长度

## 实验

1. 查看网卡 `vi /etc/udev/rules.d/70-persistent-net.rules`,记录下mac地址
2. `cd /etc/sysconfig/network-scripts/`,然后`cp ifcfg-eth0  ifcfg-eth1`,修改`ifcfg-eth1中的名称和mac地址`
3. Director 查看内核是否已经拥有ipvs `grep -i "vs" /boot/config-2.6.32-358.el6.x86_64`
4. Director 安装ipvsadm: `yum install -y ipvsadm`
5. RS `yum install httpd`, `service httpd start`
6. RS1 `echo "You are in RS1" > /var/www/html/index.html` RS2 `echo "You are in RS2" > /var/www/html/index.html`
7. 关闭防火墙`service iptables stop`
8. `echo 1 >  /proc/sys/net/ipv4/ip_forward`(出于安全考虑，Linux系统默认是禁止数据包转发的。所谓转发即当主机拥有多于一块的网卡时，其中一块收到数据包，根据数据包的目的ip地址将包发往本机另一网卡，该网卡根据路由表继续发送数据包。这通常就是路由器所要实现的功能。配置Linux系统的ip转发功能，首先保证硬件连通，然后打开系统的转发功能`less /proc/sys/net/ipv4/ip_forward`，该文件内容为0，表示禁止数据包转发，1表示允许，将其修改为1。可使用命令`echo "1" > /proc/sys/net/ipv4/ip_forward `修改文件内容，重启网络服务或主机后效果不再。若要其自动执行，可将命令`echo "1" > /proc/sys/net/ipv4/ip_forward `写入脚本`/etc/rc.d/rc.local `或者 在`/etc/sysconfig/network`脚本中添加 `FORWARD_IPV4="YES"`)


```

[root@R Zero]# ipvsadm -A -t 192.168.1.133:80 -s rr
[root@R Zero]# ipvsadm -a -t 192.168.1.133:80 -r 192.168.10.8 -m
[root@R Zero]# ipvsadm -a -t 192.168.1.133:80 -r 192.168.10.9 -m

```

改为wrr

```

[root@R Zero]# ipvsadm -E -t 192.168.1.133:80 -s wrr
[root@R Zero]# ipvsadm -e -t 192.168.1.133:80 -r 192.168.10.8 -m -w 3
[root@R Zero]# ipvsadm -e -t 192.168.1.133:80 -r 192.168.10.9 -m -w 1

```

测试：

```
ab -n 1000 -c 100 http://192.168.1.133/index.html
[root@R Zero]# ipvsadm -L -n --stats
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port               Conns   InPkts  OutPkts  InBytes OutBytes
  -> RemoteAddress:Port
TCP  192.168.1.133:80                1020     5105     5083   367990   560811
  -> 192.168.10.8:80                   762     3815     3798   274779   418947
  -> 192.168.10.9:80                   258     1290     1285    93211   141864

```