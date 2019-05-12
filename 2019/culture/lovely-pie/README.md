# lovely-pie

> Tommy bought a raspberry pi and did a default raspbian install with some commonly used software to be able to set it up in a remote location.
> But now he needs access to it. Can you help him?

There are 2 important pieces here. 
The first one is "commonly used software [...] a remote location", which should tell you that you have to use ssh.
The second one is "default raspbian install". The default user:password combination on raspbian is 'pi:raspberry'.

If we try to ssh to the container using the pi:raspberry login combination, we are greeted with some motd and the flag, after which the connection exits.
