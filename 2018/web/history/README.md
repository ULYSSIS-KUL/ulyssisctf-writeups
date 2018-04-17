# History

> We lost our database password for our wiki and now we can't figure out how to do anything! Please help! I think the previous IT-guy said something about "version control". But I don't even know what that means.

## Write-up

History is a dokuwiki wiki with an incorrect database password. All directories are traversable from the internet, and thus also the configuration files in which the database password may be found. Here one finds that the database password (which is the flag) has been removed.

Closer inspection reveals a ```.git``` directory, indicating that the website is stored and deployed using the Git version control system. [This is not a good idea](https://twitter.com/hanno/status/982530027135922179). This means the website and its entire history can be cloned using git (git clone needs to be pointed at the ```.git``` directory directly, e.g. ```git clone http://www.history.org/.git```) or downloaded using wget or similar utilities. As the name of the challenge suggests, the flag may then be found in the history of the repository (using ```git log --oneline --graph``` or ```git -SFLG``` to find the offending commit and ```git checkout <commit>``` or ```git show <commit>``` to look at the commit's files).

Technical fun fact: inserting the flag into the commit history was done using a rebase. This, however, also had the side effect of flattening the history and thus making it fairly obvious where the two commits were inserted.

