# Cisca

> Lots of routers accessible over the internet nowadays. From people's homes to big corporations. But this one's different. You know why? It has a flag of course!

## Write-up

This challenge was solved by almost every team.

It's a simple reference to the fact that many people and companies don't change the default login of many of their devices. Cisca is a parody version of the company name Cisco. Just like Cisco uses cisco as default username and password on many of its devices, so does Cisca use cisca. As there are also a few other common combinations such as admin and password, you could try 25 times before being locked out temporarily, to prevent brute forcing.

After logging in, the flag was part of the version string of the firmware.
