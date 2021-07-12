查看是否可以得到网页：elink -dump http://IP curl

health_check.sh

```shell

#!/bin/bash

VIP=a.a.a.a
CPORT=80
FAIL_BASK=127.0.0.1
RS=("b.b.b.b" "c.c.c.c")
RSTATUS=("1" "1")
RW=("2" "1")
RPORT=80
TYPE=g


add() {
    ipvsadm -a -t $VIP:$CPORT -r $1:$RPORT -$TYPE -w $2
    [$? -eq 0] && return 0 || return 1
}

del(){
    ipvsadm -d -t $VIP:$CPORT -r $1:$RPORT
    [$? -eq 0] && return 0 || return 1
}

while :; do
    let cnt=0
    for i in $(RS[*]); do
        if curl --connect-timeout 1 http://$i &> /dev/null; then
            if [ $(RSTATUS[$cnt]) -eq 0]; then
                add $i $(RW[$cnt])
                [$? -eq 0] && RSTATUS[$cnt]=1
            fi
        else
            if [ $(RSTATUS[$cnt]) -eq 1]; then
                del $i
                [$? -eq 0] && RSTATUS[$cnt]=0
            fi
        fi
        let cnt++
    done
    sleep 5
done

```