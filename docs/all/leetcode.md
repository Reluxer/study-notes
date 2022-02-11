
- [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

  ```go
  func lengthOfLongestSubstring(s string) int {
      var lastOccured = make(map[rune]int)
      start := 0
      maxlength := 0
      for i, ch := range s {
          if lasti, ok := lastOccured[ch]; ok && lasti >= start {
              start = lasti + 1
          }
          lastOccured[ch] = i
          maxlength = maxInt(maxlength, i-start+1)
      }
      return maxlength
  }
  
  func maxInt(a, b int) int {
      if a >= b {
          return a
      }
      return b
  }
  ```

- [12. Integer to Roman](https://leetcode.com/problems/integer-to-roman/)

  ```go
  func intToRoman(num int) string {
      roman := [...]string{"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"}
      ints := [...]int{1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1}
  
      r := strings.Builder{}
      for i := 0; i < len(ints) && num > 0; i++ {
          for num >= ints[i] {
              r.Write([]byte(roman[i]))
              num -= ints[i]
          }
      }
      return r.String()
  }
  ```
  
- [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/)

  ```go
  func romanToInt(s string) int {
      var r = map[byte]int{
          'I': 1,
          'V': 5,
          'X': 10,
          'L': 50,
          'C': 100,
          'D': 500,
          'M': 1000,
      }
      y := []int{}
      for i := 0; i < len(s); i++ {
          y = append(y, r[s[i]])
          if i > 0 && y[i-1] < y[i] {
              y[i-1] = -y[i-1]
          }
      }
      result := 0
      for _, valuex := range y {
          result += valuex
      }
      return result
  }
  ```
  
- [1030. Matrix Cells in Distance Order](https://leetcode.com/problems/matrix-cells-in-distance-order/)

  ```go
  func allCellsDistOrder(R int, C int, r0 int, c0 int) [][]int {
      var s = [][]int{ {r0, c0} }
      pre := 0
      for dep := 1; pre == dep-1; dep++ {
          for x := 0; x <= dep; x++ {
              y := dep - x
              var ds [][]int
              if x == 0 {
                  ds = [][]int{ {x, y}, {x, -1 * y} }
              } else if y == 0 {
                  ds = [][]int{ {x, y}, {-1 * x, y} }
              } else {
                  ds = [][]int{ {x, y}, {-1 * x, y}, {x, -1 * y}, {-1 * x, -1 * y} }
              }
              for i := 0; i < len(ds); i++ {
                  d := ds[i]
                  r := r0 + d[0]
                  c := c0 + d[1]
                  if r < 0 || r >= R || c < 0 || c >= C {
                      continue
                  }
                  s = append(s, []int{r, c})
                  pre = dep
              }
          }
      }
      return s
  }
  ```

- Continue...


---
#leetcode