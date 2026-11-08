# List of useful `git` commands

This is an unorganized list of git commands to serve as a resource beyond the general github documentation that is included in this directory. 

+ `git log --oneline -- <path_to_file>`: allows you to view the history of a file and copy the identifier for use for reverting a file back to some previous commit. 
+ `git restore --source <commit_hash> <path_to_file>: lets you revert a single file back to its state in a previous commit. The previous commit is determined based on the commit hash that is provided as an argument.  

