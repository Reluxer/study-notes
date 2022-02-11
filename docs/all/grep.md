```
cat /home/admin/cntcp/logs/service_stdout.log  | \
grep -v "CapactiySupplyDemandMatchServiceImpl.matchDetail" | \
grep -v "CapactiySupplyDemandMatchServiceImpl.selfCheck" | \
grep -v "CapactiySupplyDemandMatchServiceImpl.matchDetail" | \
grep -v "MatchDetailTask.cron" |\
grep -i -v "refresh" | \
grep -v "CapacitySupplyInstanceManagerImpl.selectMaxGmtModified" |\
# grep -v "CredentialWatcher" |\
grep -A1500 "WF1_李x_20220120112805"
```


```
tail -f /home/admin/cntcp/logs/service_stdout.log  | \
grep -v "CapactiySupplyDemandMatchServiceImpl.matchDetail" | \
grep -v "CapactiySupplyDemandMatchServiceImpl.selfCheck" | \
grep -v "CapactiySupplyDemandMatchServiceImpl.matchDetail" | \
grep -v "MatchDetailTask.cron" |\
grep -i -v "refresh" | \
grep -v "CapacitySupplyInstanceManagerImpl.selectMaxGmtModified"
```

---
#grep #linux 