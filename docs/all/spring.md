服务启动加载顺序：

1. SpringApplicationRunListener
2. ApplicationListener《ApplicationEnvironmentPreparedEvent》
3. ApplicationContextInitializer
4. ApplicationListener《ApplicationPreparedEvent》
5. @PostConstruct
6. InitializingBean接口
7. ApplicationListener《ApplicationStartedEvent》
8. ApplicationListener《SpringApplicationEvent》
9. ApplicationListener《ApplicationReadyEvent》
> https://blog.csdn.net/qq_38496991/article/details/124406059


# 记录bean初始化耗时
```java
@Service
@Slf4j
public class BeanInitMetrics implements BeanPostProcessor {

    private final Map<String, Long> stats = new HashMap<>();

    public static final Map<String,Long> metrics = new HashMap<>();

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        stats.put(beanName, System.currentTimeMillis());
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        Long start = stats.get(beanName);
        if (start != null) {
            metrics.put(beanName, System.currentTimeMillis() - start);
            log.warn("v3BeanInitMetrics beanName {} #{}",beanName, System.currentTimeMillis() - start);
        }
        return bean;
    }

}  
```