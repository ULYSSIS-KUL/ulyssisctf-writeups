# Up

> hi i have an AWESOME nwe wwebsite please visit it thanks :)

## Write-up

Up is a fast, functional, aesthetically pleasing website. The homepage is extremely secure, and will reveal nothing except great taste. However, the ASCII art which is proudly linked to is displayed using a PHP script. This script will display the text contents of any file it receives, such as the various arts located in the ```art/``` subdirectory.

This subdirectory is a big hint to the vulnerability in this site: the file argument will take any file path, relative to the root directory of the website. In most filesystems, ```..``` is a valid part of any path. Thus, any file in the filesystem can be read using this PHP file. You only has to go "up" enough times!


Even /etc/passwd, containing the login information for every user, is accessible, using an url ending with something like ```example.org/files.php?file=../../../../etc/passwd```. Here you will find a user with the name "timmy", the login shell of ```/bin/cowsay```, the home directory of ```/lost+found``` and a password starting with "FLG{".

