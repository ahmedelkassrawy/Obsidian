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

```git 
git merge feature-conflict     #this will fail

so we edit the file that is wrong and finish it 

git add -file that was edited-
git commit
```

after the conflict, you must **`add` + `commit` while the merge is still in progress** — that's what produces the merge commit. 
If you abort or start over, you get a plain linear commit and the judge won't see a merge.

---
You are in the middle of complex configuration change on main
Your code is currently broken and not ready to be commited
an urgent bug appears on a branch
git wont let you switch branches because of the uncommited changes , 
you need to pause your work safly without commiting it

stash -> temporary drawer for uncommited work

your config.json change is half done and you cant switch branches with it dirty
stash shelves it and you handle the urgent fix and then you pop it back exactly as it was

- When you `stash`, it doesn't just save your changes — it also **cleans your working files** back to the last commit, so your branch is tidy and you can switch freely.
- The shelf is actually a **stack** — you can stash several times. `pop` takes the **most recent** one off and reapplies it; `git stash list` shows them all.

```git
git stash              #put on the shelf
git switch urgent-fix         #to fix a bug
git commit -m "Commit messsage"
git switch master             #return to the master branch
git stash pop           #bring the on shelf back
```

git stash -> save your changes to the drawer AND revert your files to clean.
git stash pop -> take the most recent stash and reapply it
git stash list -> show whats on the shelf
git stash apply -> reapplies but keeps it in the drawer (opposite of the pop)

---
your `feature-darkmode` has "Start dark mode," and `master` moved ahead with "Critical bug fix." They forked from "Initial commit." You want your feature to sit **on top of** master's latest, as a straight line — no merge commit.

rebase -> it lifts your commits off and moves the tip of the other branch and replays your commits on top as if you started from the latest version all along

**Merge** keeps both lines and ties them with a merge commit. History shows the fork — honest, but messier.

**Rebase** moves your commits on top for a **straight line** — cleaner, but it **rewrites your commits**

Before the rebase

              (B) Start dark mode        <- feature-darkmode (your work)
             /
  (o) Initial
             \
              (C) Critical bug fix        <- master

After the rebase

  (o) Initial  ->  (C) Critical bug fix  ->  (B') Start dark mode      <- feature-darkmode

Your "Start dark mode" now sits **above** "Critical bug fix." No merge commit.

```git
git rebase master
git log --oneline
git status
```

---
while developig func A , you made several messy commits , about to open a PR for code review , to make it easier for the seniors to review the work , we want to combine those messy commits into one clean commit

Use an interactive rebase to squash the last 3 commits into 1 single commit 

squash means fold this commit into the one above it 
you keep the first comit as is and the squash next two into it as a single commit

```git
git config --global core.editor notepad

git rebase -i HEAD~3         # last 3 commits

in the notepad change the last 2 from pick to squash and leave the first as pick as it is and save 
then write 1 commit message only
```

---
you realized the second commit in history has a messy message since it isnt the most recent commit and you cant use the simple amend because it only fixes the last commit so for an older one you use a intactive rebase with reword

reword -> changes the messge only the content is untouched ,
rebase just rewrites one message

```git
git rebase -i HEAD~2     #because the commit was 2 back 

in the last 2 commits 
in the first line change the pick to reword and save then
change the commit message
```