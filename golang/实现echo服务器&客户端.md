# 简介

> 参考这里：http://studygolang.com/articles/3183

原文里面服务端程序有个地方，写的并不好，不具备普适性

# server.go

```golang
package main

import (
    "bufio"
    "fmt"
    "net"
    "time"
)

func main() {
    var tcpAddr *net.TCPAddr

    tcpAddr, _ = net.ResolveTCPAddr("tcp", ":9999") // 这里ip地址最好不要写

    tcpListener, _ := net.ListenTCP("tcp", tcpAddr)

    defer tcpListener.Close()

    for {
        tcpConn, err := tcpListener.AcceptTCP()
        if err != nil {
            continue
        }

        fmt.Println("A client connected : " + tcpConn.RemoteAddr().String())
        go tcpPipe(tcpConn)
    }

}

func tcpPipe(conn *net.TCPConn) {
    ipStr := conn.RemoteAddr().String()
    defer func() {
        fmt.Println("disconnected :" + ipStr)
        conn.Close()
    }()
    reader := bufio.NewReader(conn)

    for {
        message, err := reader.ReadString('\n')
        if err != nil {
            return
        }

        fmt.Println(string(message))
        msg := time.Now().String() + "\n"
        b := []byte(msg)
        conn.Write(b)
    }
}
```


# client.go

```golang
package main

import (
    "bufio"
    "fmt"
    "net"
    "time"
)

var quitSemaphore chan bool

func main() {
    var tcpAddr *net.TCPAddr
    tcpAddr, _ = net.ResolveTCPAddr("tcp", "192.168.0.106:9999")
    conn, _ := net.DialTCP("tcp", nil, tcpAddr)
    defer conn.Close()
    fmt.Println("connected!")
    go onMessageRecived(conn)
    b := []byte("time\n")
    conn.Write(b)
    <-quitSemaphore
}

func onMessageRecived(conn *net.TCPConn) {
    reader := bufio.NewReader(conn)
    for {
        msg, err := reader.ReadString('\n')
        fmt.Println(msg)
        if err != nil {
            quitSemaphore <- true
            break
        }
        time.Sleep(time.Second)
        b := []byte(msg)
        conn.Write(b)
    }
}
```