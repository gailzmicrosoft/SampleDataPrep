

## Commonly Used `git` Commands for Beginners 

**Step 1: Make new branch and work on new branch** 

```sh
git checkout main                (switch to local main branch)
git pull origin main             (pull latest remote main branch to local main)
git checkout -b my-work-branch   (make a new local branch my-work-branch off local main)
git push origin my-work-branch   (publish my-work-branch to remote my-work-branch)

... work on code and documents, commit and sync up with remote branch, using Visual Studio Code User Interface 
   
Below steps are only needed if you want to pull latest remote main and merge into your current branch, for example, you want to integrate updates made by your co-worker that is already merged into remote main through a pull request.  

git checkout main                (switch to local main branch)
git pull origin main             (pull latest remote branch to local main)
git checkout my-work-branch      (switch to local my-work-branch)
git merge main                   (Merge local main to local my-work-branch)
```

When you are ready to submit a pull request, go to ADO, submit PR and merge your changes to remote main. 

**Sync your local branch to remote branch Periodically**

It is a best practice that you periodically pushing updates to remote branch so that all your changes are kept in the remote server, not just on your computer local branch. 

This also helps if you and you co-worker(s) need to work on the same branch. 

```sh
... you are already working on my-work-branch.
git pull origin my-work-branch   (pull latest from remote my-work-branch to local)
git push origin my-work-branch   (push latest from local my-work-branch to remote)
```

**Step 2: delete local branch after your pull request is complete** 

```sh
git checkout main                (switch to local main branch)
git pull origin main             (pull latest remote main to local main)
git branch -d my-work-branch     (delete local branch my-work-branch)
git branch -D my-work-branch     (force delete local branch my-work-branch)

git branch -r                    (list all remote branches)
git branch                       (list all local branches)
git branch -a                    (list all remote and local branches)

git checkout main 
git fetch --prune                (This deletes local branches already merged in remote) 
```

