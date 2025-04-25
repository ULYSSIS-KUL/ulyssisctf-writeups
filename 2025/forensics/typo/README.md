# typo writeup

In this challenge, you are given an API which seems to be malfunctioning. When clicking the given link `192.168.0.0?res=flqg`, we get an error message. What gives? 

Let's take a look at the error message: 

```
{"result":"Unknown endpoint: flqg. Please try something which does exist!"}
```

We notice that the endpoint `flqg` does not exist. However, we do notice that the endpoint is misspelled, it should be `flag`. By changing the GET parameter in the url yields this: `192.168.0.0?res=flag`. This then gives us the flag as promised. Nice and ez. 
