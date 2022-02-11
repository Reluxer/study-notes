
# comment 规范

`{type}: {subject}`

type, 必须

提交类型 type 用来描述一次提交行为的改动方向。

type 的可选值如下。注意：Git log 的 type 和 changelog 的 type 存在紧密联系；然而它们两者之间并非一一对应，比如在 changelog 中一般不会指出文档 docs 或测试用例 test 等方面发生的变化。

- feat: 新增功能。（task功能提交）
- fix: 修复 bug。(bug修复)
- docs: 文档相关的改动。(在线文档，说明文档，注释内容)
- style: 对代码的格式化改动，代码逻辑并未产生任何变化。(样式文件修改)
- test: 新增或修改测试用例。
- refactor: 重构代码或其他优化举措。
- chore: 项目工程方面的改动，代码逻辑并未产生任何变化。


---
#git