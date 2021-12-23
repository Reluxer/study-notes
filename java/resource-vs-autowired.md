
@Resource 按名字，是JDK的
@Autowired 按类型，是Spring的。

@Autowired 默认按照类型装配，默认情况下它要求依赖对象必须存在，不存在会NullpointException.
如果允许为null，可以设置它required属性为false.
如果我们想使用按照名称装配，可以结合@Qualifier注解一起使用.


@Resource 默认按照名称装配，当找不到与名称匹配的bean才会按照类型装配.
可以通过name属性指定.
如果没有指定name属性，当注解标注在字段上，即默认取字段的名称作为bean名称寻找依赖对象，
当注解标注在属性的setter方法上，即默认取属性名作为bean名称寻找依赖对象.
