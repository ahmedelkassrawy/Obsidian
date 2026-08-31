we created two files , these files are untracked, this means the Git is aware they exist in the folder, its not recording those yet

```git
git status
git add hello.txt notes.txt
git commit -m "Initial commit"
git log
```

---
concept -> --amend 
fixes the last commit instead of making a new one
like we forgot "file2.txt" and you stage it and fold it into the existing add files commit
now the end result is still one commit and holding both files

amend doesnt edit the commit in place, it replaces it with a new commit that has a new hash
the new hash means that the old commit is discarded, so this is you first taste of rewriting history .
never amend a commit you have already pushed/shared -- the hash changes

```git
git status
git add file2.txt
git commit --amend --no-edit
```
the --no-edit is to not edit the commit message

```git 
git show HEAD       #should list both file1.txt and file2.txt
git log --oneline
```

git show HEAD -> shows the head commit
and the online is to see the commit 

---
you made a commit but immedialty realized you forgot to include another change, you want to uncommit the last commit so that you can add more files to it and you dont want to lose the code you wrote

```git
git reset --soft HEAD~1
git log
git status
```

**`--soft HEAD~1`** — moves the pointer, and the undone commit's changes stay **staged** (green). ← this task.

---
You need to develop a new feature without messing up the stable code on main so we make a new branch just a movable pointer to a commit

```git
git switch -c feature-idea
echo "my idea" > idea.txt
git add idea.txt
git commit -m "feat: add new idea"
```

---
while you were updating the main branch and we finished the feature and want to be merged to the main branch

```git
git merge branch-name

#check them using the 
git log --oneline --graph
```

fast forward merge -> if your branch hasn't moved since the split , git just slides the pointer forward -  no extra commit

true merge -> both branches got new commits after they split , we need to create a merge commit that ties the 2 histories together.

---
you and teammate both edited the same line in todo.md at the same time on different branches
when you try to merge his work into yours git gets confused because it doesnt know which line is the truth , so it stops the merge and asks you to decide

