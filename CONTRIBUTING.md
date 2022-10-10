# Contributing Guidelines 🤝

</br>

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](#)
&nbsp;
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](#)


This documentation contains a set of guidelines to help you during the contribution process.
We are happy to welcome all the contributions from anyone willing to improve/add new scripts to this project.
Thank you for helping out and remember, **no contribution is too small.**
Being an open source contributor doesn't just mean writing code, either. You can help out by writing documentation, tests, or even giving suggestions. 🏆


###  1 : Set up the project in your local machine

- Fork [this](https://github.com/kanakmi/Detective-Discord) Repository. This will create a Copy of the Repository on your Github account.
- To migrate the project on your local machine, you need to clone the forked repo.
 Also have to keep a reference to the original project in `upstream` remote.  

```bash
git clone https://github.com/<your-username>/Detective-Discord.git 
cd Detective-Discord  
git remote add upstream https://github.com/kanakmi/Detective-Discord.git
```   

- If you have already forked the project, update your copy before working. It is important to sync your fork with the original repository.

```bash
git remote update
git checkout <branch-name>
git rebase upstream/<branch-name>
```

**OR**


```
git pull upstream master
```


###  2 : Branch

###    Create a new branch after setting up the project locally before making any changes, so as to avoid merge conflicts while making PRs .
Use it's name to identify the issue your addressing. Feature, Bug Fix or Enhancement.

```bash
# It will create a new branch with name Branch_Name and switch to that branch 
git checkout -b branch_name
```


###  3 : Work on the issue assigned

- Work on the issue(s) assigned to you.
- Make any required changes to the codebase or add any files/folders
- After you've made changes or made your contribution to the project, add changes to the staging area of the branch you've just created by:

```bash  
# To add all new files and changes to branch Branch_Name  [ staging ]
git add .  
# To add only a few files to Branch_Name
git add <some files>
```


###  4 : Commit

- This will commit the changes to your branch. To commit give a descriptive message for the convenience of reviewer by:

```bash
# This message get associated with all files you have changed
git commit -m "message"  
```

###  5 : Push to Remote

```bash  
# To push your work to your remote repository (forked)
git push -u origin Branch_Name
```


###  6 : Pull Request

- Go to your repository in browser and click on `compare and pull requests`. Please ensure you compare the changes in your feature branch to the target branch of the repo you are supposed to make a PR to. <br>
- 
** Add an appropriate title and description to your pull request explaining your changes and efforts done. Add screenshots if adding a new command (**mandotory**). ** Then click on `Create Pull Request`.


### 7 : Review

- 🎉🌟Congratulations! Sit and relax, you've made your PR to Detective Discord project. Wait until the PR is reviewed and make any changes suggested by the maintainers. Following which the PR can be successfully merged and your contribution is incorporated into the project !
🎉🎊



In case of any help, please free to message me on <a href="https://twitter.com/Kanakmi">Twitter</a>

## ❤️ Project Admin
|                                     <a href="https://github.com/kanakmi"><img src="https://avatars.githubusercontent.com/u/54859521?v=4" width=150px height=150px /></a>                                      |
| :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                                                                      **[Kanak Mittal](https://twitter.com/Kanakmi)**                                                                                    |

