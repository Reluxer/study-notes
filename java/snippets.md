### List 排序

1. 原始的写法

```java
Collections.sort(this.getTimeSlices(), new Comparator<TimeSlice>() {
                public int compare(TimeSlice o1, TimeSlice o2) {
                    return o1.getBeginDate().compareTo(o2.getBeginDate());
                }
            });
```

2. 第一次改进
```java
this.getTimeSlices().sort((o1, o2) -> o1.getBeginDate().compareTo(o2.getBeginDate()));
```

3. 最终
```java
this.getTimeSlices().sort(Comparator.comparing(TimeSlice::getBeginDate));
```

### 构造器的具体处理步骤

1. 所有数据域被初始化（0，false，null）
2. 按照申明的顺序执行域初始化语句和初始化块
3. 如果第一行调用了另一个构造器，执行该构造器
4. 执行构造器主题

### SQL 原生查询

```java
int cnt = (org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate)jdbcTemplate.execute(sql,params , thisClass::doInPreparedStatement);

private static Integer doInPreparedStatement(PreparedStatement pstmt) throws SQLException {
    pstmt.execute();
    ResultSet rs = pstmt.getResultSet();
    rs.next();
    return rs.getInt(1);
}
```