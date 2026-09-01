---
title: "Git — hands-on reference (Git-Gud workshop)"
type: reference-note
tags: [git, version-control, rebase, reflog]
source: "Git-Gud workshop (16 exercises), 2026-08"
date: 2026-08-31
---

# Git — hands-on reference

Notes from working through the Git-Gud challenges by hand. Organized as: save work → undo → branches → rewrite history → navigate & recover.

## The mental model (read this first)

**Three places your work lives:**

- **Working directory** — your actual files.

- **Staging area** — what you've marked (`git add`) to save in the next commit.

- **Repository** — the committed history.

Almost every command just moves work between these three.

**Two more ideas that make the rest click:**

- A **commit** is a saved snapshot (think: a photo).

- **HEAD** and each **branch** are **bookmarks** pointing at "where you are." `git log` only shows what a bookmark can **reach**.

- **Rewriting history** (amend, rebase) doesn't edit a commit in place — it makes a **new commit with a new hash**. So the rule everywhere: **never rewrite commits you've already pushed/shared** — the hash changes and your history splits from everyone else's.

---

## 1. Save work

### commit — the basic flow

Untracked files exist in the folder but Git isn't recording them yet. `add` stages them, `commit` saves them to history.

```bash
git status
git add hello.txt notes.txt
git commit -m "Initial commit"
git log
```

### amend — fix the LAST commit

Forgot a file, or want to fix the message, on the most recent commit? Fold it in instead of making a new commit.

```bash
git add file2.txt
git commit --amend --no-edit     # --no-edit keeps the old message
```

- Still one commit, now holding both files.

- Amend **replaces** the commit with a new one (new hash) — your first taste of rewriting history. Don't amend pushed commits.

---

## 2. Undo

### reset — move the branch pointer back

`git reset <mode> HEAD~1` moves your branch back one commit. The **mode** decides how much it keeps. The **target** (`HEAD~1`) is which commit; leave it off and it defaults to HEAD (a no-op).

| mode | commit | staging area | working files |
| --- | --- | --- | --- |
| `--soft` | back | **keeps** (staged) | keeps |
| `--mixed` (default) | back | unstages | keeps |
| `--hard` | back | throws away | **throws away** |

```bash
git reset --soft HEAD~1     # un-commit but keep changes staged (green)
```

- `--hard` is the dangerous one your history gets burned by — but even it is recoverable via reflog (see the end).

---

## 3. Branches

### branch + switch — parallel work

A branch is just a movable pointer to a commit.

```bash
git switch -c feature-idea     # create AND switch (older: git checkout -b)
echo "my idea" > idea.txt
git add idea.txt
git commit -m "feat: add new idea"
```

- `git branch name` creates without switching. `git switch name` switches to an existing one. `*` in `git branch` marks where you are.

### merge — combine a branch back

```bash
git merge feature-login
git log --oneline --graph      # see the shape
```

- **Fast-forward:** if your branch hasn't moved since the split, Git just slides the pointer forward — no extra commit.

- **True merge:** both branches gained commits after the split, so Git makes a **merge commit** (two parents) tying the histories together.

### merge conflict — Git hands you the decision

When two branches change the **same line**, Git can't pick a winner. It stops and writes both versions into the file with markers:

```
<<<<<<< HEAD
your current branch's version
=======
the incoming branch's version
>>>>>>> other-branch
```

Fix it by hand, then finish the merge:

```bash
git merge other-branch     # fails with a conflict
# edit the file: keep the right content, delete all <<<<<<< ======= >>>>>>> lines
git add <the-file>
git commit                 # completes the merge -> a merge commit
```

- You must `add` + `commit` **while the merge is in progress** — that's what makes the merge commit. Abort or start over and you get a plain linear commit instead.

### stash — a temporary drawer

Shelve unfinished work so you can switch tasks, then bring it back.

```bash
git stash            # save changes AND clean your files back to the last commit
git switch urgent-fix
git commit -m "fix: done"
git switch master
git stash pop        # bring your shelved changes back
```

- The shelf is a **stack**. `pop` = take the newest off and reapply. `git stash list` = see them all. `git stash apply` = reapply but keep it on the shelf.

---

## 4. Rewrite history (the rebase family)

> Set a friendly editor first — interactive rebase opens one, and the default (Vim) is painful on Windows:
> ```bash
> git config --global core.editor notepad
> ```

### rebase — replay your commits on a new base

Make your feature sit **on top of** the latest of another branch, as a straight line — no merge commit.

```bash
git rebase master     # run while ON your feature branch
```

**Before**
```
              (B) Start dark mode      <- feature (your work)
             /
  (o) Initial
             \
              (C) Critical bug fix      <- master
```

**After `git rebase master`**
```
  (o) Initial  ->  (C) Critical bug fix  ->  (B') Start dark mode   <- feature
```

- Merge keeps both lines (honest, messier). Rebase moves your commits on top (cleaner, but **rewrites them** → new hashes → never rebase pushed commits).

### interactive rebase — history surgery

`git rebase -i HEAD~N` opens a to-do list of the last N commits (oldest at top). You change the verb in front of each line:

| verb | does |
| --- | --- |
| `pick` | keep the commit as-is |
| `squash` | fold this commit **into the one above** |
| `reword` | change this commit's **message** only |
| `drop` | delete this commit entirely (or just delete its line) |
| `edit` | **pause** here so you can change the commit's **content** |
| (reorder) | swap the **line order** = swap the commit order |

**Squash** (combine messy commits into one):
```bash
git rebase -i HEAD~3
# change the 2nd and 3rd 'pick' to 'squash', save
# second editor opens -> write ONE clean message
```

**Reword** (fix an older message):
```bash
git rebase -i HEAD~2
# change the target line's 'pick' to 'reword', save
# second editor -> type the new message
```

**Drop** (remove a commit, e.g. a leaked secret):
```bash
git rebase -i HEAD~2
# change its 'pick' to 'drop' (or delete the line), save
```
- Caveat: if the bad commit was already **pushed**, drop only fixes YOUR copy — the secret is still in the remote + everyone's clone + reflog. Rotate the secret anyway.

**Reorder** (swap order):
```bash
git rebase -i HEAD~2
# swap the two lines, save
```

**Edit** (change a commit's content in place):
```bash
git rebase -i HEAD~2
# change the target line's 'pick' to 'edit', save
# git STOPS at that commit; now fix the file:
git add <file>
git commit --amend --no-edit
git rebase --continue          # resume back to the present
```

---

## 5. Navigate & recover

### detached HEAD — standing on a commit, not a branch

Normally **HEAD → branch → commit**. Check out a raw commit and **HEAD points straight at it, no branch** = detached. Safe for *looking* at old code; the warning is just informational.

```bash
git log --oneline
git checkout <old-hash>     # detached HEAD (the warning is expected)
git switch master           # re-attach to the branch
```

- Danger: commits made *while detached* belong to no branch, so they look "lost" when you leave. Recoverable via reflog.

### cherry-pick — copy ONE commit

Grab a single commit from another branch (a fix) without dragging the whole branch.

```bash
git log --oneline experimental    # find the commit's hash
git cherry-pick <hash>
```

- Merge/rebase move whole branches; cherry-pick copies one commit (new hash). Can conflict, same resolve-then-continue.

### reflog — the safety net (why rebase/reset are actually safe)

You ran `git reset --hard HEAD~1` and Version 2 vanished from `git log`. It is **NOT deleted.**

- `reset --hard` just **moved the branch bookmark back**. Version 2's snapshot still exists on disk — but no bookmark points to it, so `git log` (which only shows reachable commits) can't see it. It's **unbookmarked**, not gone.

- `git reflog` is a **diary of every place HEAD has ever been** (commits, resets, checkouts, rebases), newest first:

```
9c33636 HEAD@{0}: reset: moving to HEAD~1     <- now: Version 1
f78bd71 HEAD@{1}: commit: Version 2           <- one move ago: the "lost" commit
9c33636 HEAD@{2}: commit (initial): Version 1
```

- `HEAD@{0}` = where you are now; `HEAD@{1}` = one move ago; the hash is on the left.

Recover by moving the bookmark back onto it:

```bash
git reflog
git reset --hard HEAD@{1}     # or: git reset --hard <that-hash>
```

**The whole point:** reset / rebase / drop only **move bookmarks** — they don't delete snapshots, and reflog remembers every position (~90 days). So nothing here was ever truly lost. **Rebase and reset are safe because reflog has your back.**

---

## Quick reference

| I want to… | command |
| --- | --- |
| stage + save | `git add <f>` → `git commit -m "..."` |
| fix the last commit | `git commit --amend --no-edit` |
| un-commit, keep work staged | `git reset --soft HEAD~1` |
| throw away last commit + changes | `git reset --hard HEAD~1` (recoverable via reflog) |
| new branch + switch | `git switch -c <name>` |
| combine a branch in | `git merge <branch>` |
| shelve / restore work | `git stash` / `git stash pop` |
| replay onto latest | `git rebase <base>` |
| squash / reword / drop / reorder / edit | `git rebase -i HEAD~N` |
| look at an old commit | `git checkout <hash>` → `git switch master` |
| copy one commit | `git cherry-pick <hash>` |
| recover a "lost" commit | `git reflog` → `git reset --hard HEAD@{n}` |
