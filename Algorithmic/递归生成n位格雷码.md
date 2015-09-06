##  描述

产生n位元的所有格雷码。

## 解法

> 参考这里：http://blog.csdn.net/beiyeqingteng/article/details/7044471

## code

```java
public String[] GrayCode(int n) {

    // produce 2^n grade codes
    String[] graycode = new String[(int) Math.pow(2, n)];

    if (n == 1) {
        graycode[0] = "0";
        graycode[1] = "1";
        return graycode;
    }

    String[] last = GrayCode(n - 1);

    for (int i = 0; i < last.length; i++) {
        graycode[i] = "0" + last[i];
        graycode[graycode.length - 1 - i] = "1" + last[i];
    }

    return graycode;
}
```
