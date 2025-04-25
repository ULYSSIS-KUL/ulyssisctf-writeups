# void writeup

The challenge shows a login screen resembling that of macOS. The page title specifies that it's version High Sierra 10.13. We also know from the challenge's flavortext that we want to log in with admin rights.

This version of macOS had a critical bug that let you log in as admin without a password. To get the flag, you just had to enter `root` in the username field, leave the password field empty, and press Enter.

Read more about this bug:

* [macOS bug lets you log in as admin with no password required - Ars Technica](https://arstechnica.com/information-technology/2017/11/macos-bug-lets-you-log-in-as-admin-with-no-password-required/)
* [CVE-2017-13872 Detail - NIST](https://nvd.nist.gov/vuln/detail/CVE-2017-13872)
