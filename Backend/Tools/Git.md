branch is a parallel version of your project 
```bash
git add readme.md
```

commiting is like taking a screenshot of the code at any sort of time
```bash
git commit -m 'Add readme.md file'
```
-m stands for message

```bash
git add ./ 
```

adds all files in folder

```bash
git log //press q to close it
```

head is a pointer which refers to the pointer pointing on the latest commit you've done once we do another commit the head gets shifted to the new commit created

```bash
git checkout 3397375890923-0235285-2
```
so when you checkout you just let the head go one step back but these files are still there somewhere but not available for head to display
```bash
git checkout main or git checkout -f main
```

it just lets us let the head forward to the latest commit as it was and discarding any before change

```bash
git branch -M main 
```
to name the branch with main

```bash
git remote add origin https://github.com/ahmedelkassrawy/mastering_git.git
```

to connect the remote repo on github with the local one we just created
```bash
git push -u origin main
```

used to push all the thing we did to origin (typical name for the repo we just created ) and choosing the branch main 
```bash
git branch branch-name
git checkout branch-name
```

```bash
git checkout -b feature-name
```

when you create a branch it will be based on the branch you are currently on
so the new branch will contain the code from the main branch at that time so you should either first switch to the branch you want to base from

```bash
git branch new-branch-name source branch
```

```bash
git push --set-upstream origin feature-branch
```

used to push a local branch to a remote repo and set it the upstream branch
so the first push will push the branch
--set-upstream --> links the local branch to the remote branch
git will remember the relationship between the local feature-branch and remote feature- branch

**set the upstream tracking relationship** between a local branch and a remote branch

- With `--set-upstream`, Git automatically knows where to push or pull from, making your workflow faster and more efficient.
```bash
git pull
```
to pull any changes happened to the remote repo
### Git Reset
```bash
git reset
```

it will remove the commits but will leave them in working directory and unstage changes , keeps the changes in working directory

```bash
git revert 
```

undo a commit by creating a new commit that reverses the changes introduced by the specified commit

```bash
git stash 
```
used to do temporary fixes to file while having a copy of what you where working on  
```bash
git stash apply
```
to get those code back