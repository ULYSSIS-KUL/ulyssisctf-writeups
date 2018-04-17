# Message Digest Five
> I found this [zip file](challenge.zip) in my back yard, but only have a note with the hash of the password: 9cc2ae8a1ba7a93da39b46fc1019c481. Can you help me?

## Write-up
Googling the provided hash reveals that it is the MD5 hash of "correct horse battery staple". The
zip file can be decrypted using that string as a password.
