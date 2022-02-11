撤销中间某次commit

1. 

git revert commit_id

2. 

git rebase -i id_before_commit_id; pick -> drop; git push -f


revert之后再次合并，代码没合并上？

再次revert