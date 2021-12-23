springmvc 父子容器？

```java
import org.springframework.web.servlet.support.AbstractAnnotationConfigDispatcherServletInitializer;

public class MvcAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {
    // 父容器
    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class<?>[]{SpringContrainer.class};
    }

    // 子容器
    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?>[]{MvcContrainer.class};
    }

    @Override
    protected String[] getServletMappings() {
        return new String[]{"/"};
    }
}
```

```java
import org.springframework.context.annotation.ComponentScan;

@ComponentScan("com.xx")
public class SpringContrainer {
}
```
```java
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.FilterType;
import org.springframework.stereotype.Controller;

//@ComponentScan(value = "com.XXX", includeFilters = {
//        @ComponentScan.Filter(type = FilterType.ANNOTATION, value = {Controller.class})
//}, useDefaultFilters = false)
public class MvcContrainer {
}
```

可以没有子容器吗？ 可以
@service中引用@controller可以吗？
不可以，会有检查

https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#spring-web
