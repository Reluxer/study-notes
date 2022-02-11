[TOC]

# 基础语法

## 变量定义

### 1. 关键字**var** 

#### 定义

```golang
var a int
var b string
```

定义之后，自动赋予初始值 ZeroValue

`0` for numeric types,  
`false` for the boolean type, and  
`""` (the empty string) for strings.

#### 定义并初始化

```go
var a, c int = 1, 2
var b string = "b"
```

类型可省略，编译器自动推断

```go
var a, b, c, d = 1, 2, true, "hello world"
```

### 2. := 定义并初始化

在函数内部，可以使用`:=`替代`var`

```go
func xxx(){
    k := 3
    c, python, java := true, false, "no!"
}
```

但是在函数外面，所有的语句必须以关键字开始（ `var`, `func`... ），不可使用`:=`

### 变量作用域

go没有全局变量，有包内变量，和函数内变量

## 内建变量类型

- `bool` `string`
- `(u)int` `(u)int8` `(u)int16` `(u)int32` `(u)int64` `uintptr`
- `byte` : 8bit,  `rune` : 32bit
- `float32` `float64` `complex64` `complex128`

类型转换是强制的 显式的

## 常量

使用`const`定义常量

```go
const filename = "abc.txt"
// 不指定类型，就是简单的文本替换
const a, b = 3, 4
var c int = int(math.Sqrt(a * a + b * b))

// 指定类型，要考虑类型转换
const a, b int = 3, 4
var c int = int(math.Sqrt(float64(a * a + b * b)))
```

### 枚举

```go
const (
    cpp = 1
    java    // = 1复制前面的值
    python  // = 1
    golang  // = 1
)
    
const (
    cpp = iota // 0 
    java       // 1 自增
    _          // 2 可用_忽略该值，但仍然自增
    golang     // 3
)
    
const (
    b = 1 << (10 * iota) // 1
    kb                   // 1024
    mb                   // 1048576
    gb                   // 1073741824
    tb                   // 1099511627776
    pb                   // 1125899906842624
)
```

## 控制语句

### if

`if`表达式不需要`( )`，但是 `{}`还是需要的

```go
func sqrt(x float64) string {
    if x < 0 {
        return sqrt(-x) + "i"
    }
    return fmt.Sprint(math.Sqrt(x))
}
```

`if`语句能在条件判断之前执行一个表达式，该表达式定义的变量只在`if`语句范围类有效

```golang
func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {
    return v
    }
    return lim
}
```

### switch

`switch`会自动`break`，除非使用`fallthrough`

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("When's Saturday?")
    today := time.Now().Weekday()
    switch time.Saturday {
    case today + 0:
        fmt.Println("Today.")
    case today + 1:
        fmt.Println("Tomorrow.")
    case today + 2:
        fmt.Println("In two days.")
    default:
        fmt.Println("Too far away.")
    }
}
```

没有表达式的`switch`相当于`switch true`。这种结构利于用干净的方式写很长的`if-then-else`链。

### for

- go 只有for一个循环语句关键字
- for 的条件里不需要括号
- for的条件里可以省略初始条件（第一次迭代之前执行） 结束条件（每次迭代前执行） 递增表达式（每次迭代后执行）

# Goroutine

非抢占式 由协程自己在切换点交出cpu控制权

Goroutine 可能的切换点

- I/O, select
- channel
- 等待锁
- 函数调用(有时)
- runtime.Gosched()
- 等待锁



# 编码相关

## Code

```go
func TestRune(t *testing.T) {
	s := "12一二"
	t.Log(len(s))
	t.Log("------")
	for i, b := range []byte(s) { // utf8
		t.Logf("%d %x", i, b)
	}
	t.Log("------")
	for i, b := range s { // utf8 --> unicode
		t.Logf("%d %x", i, b)
	}
	t.Log("------")
	for i, b := range []rune(s) { // utf8 --> unicode --> []rune
		t.Logf("%d %x", i, b)
	}
}
```

## Output:

```
8
------
0 31
1 32
2 e4
3 b8
4 80
5 e4
6 ba
7 8c
------
0 31
1 32
2 4e00
5 4e8c
------
0 31
1 32
2 4e00
3 4e8c
```

## Ref

- [字符编码笔记：ASCII，Unicode 和 UTF-8](http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html)


---
#go