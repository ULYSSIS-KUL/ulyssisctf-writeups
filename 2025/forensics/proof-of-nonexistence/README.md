# proof-of-non-existence writeup

There are a few hints given:
1. The name of the challenge is "proof-of-nonexistence". There has to be a mechanic to cryptographically sign something that doesn't exist. This is one of the big issues in DNSSEC and is solved with NSEC(3) records, which points at the Next SECure record if you query a record that doesn't exist.
2. What you're looking for is a DNS-record "We assume they use the DNS-server to communicate".

So when you query the given nameserver with the given domain and look for NSEC-records by using +dnssec (ANY is not allowed, and AXFR/IXFR are also not allowed, so no easy solves :) ), you will find a first clue:

```
❯ dig @127.0.66.1 f.elite-hacker.be +dnssec

; <<>> DiG 9.20.8 <<>> @127.0.66.1 f.elite-hacker.be +dnssec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 11720
;; flags: qr aa rd; QUERY: 1, ANSWER: 0, AUTHORITY: 4, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: ffc909a6eef709420100000068054518d95e52d17fb6023d (good)
;; QUESTION SECTION:
;f.elite-hacker.be.		IN	A

;; AUTHORITY SECTION:
elite-hacker.be.	60	IN	SOA	ns.elite-hacker.be. root.elite-hacker.be. 7 60 60 60 60
elite-hacker.be.	60	IN	RRSIG	SOA 13 2 60 20250504185927 20250420175927 54898 elite-hacker.be. NEjbJ0HPbwMUhs0PjfevElnX/wU6TYmTl/rduMlGMj8nzkGz/UBM81Iq H9vg2494CrQjYFbgSw4IUnVSQiwlwA==
elite-hacker.be.	60	IN	NSEC	hint.elite-hacker.be. NS SOA TXT RRSIG NSEC DNSKEY TYPE65534
elite-hacker.be.	60	IN	RRSIG	NSEC 13 2 60 20250504180808 20250420175927 54898 elite-hacker.be. 9dSCsH1pRnH7yxCOgicr8lJEWsWy6RrkDevlZ4nyJOYLxJc+SgsMbJYk dAYQe5c1nhdizf+zT4TGZHwuKzQjBw==

;; Query time: 0 msec
;; SERVER: 127.0.66.1#53(127.0.66.1) (UDP)
;; WHEN: Sun Apr 20 21:03:52 CEST 2025
;; MSG SIZE  rcvd: 417
```

There's an NSEC-record at the apex of the domain pointing to the next secure domain, "hint.elite-hacker.be". Querying that reveals nothing except a useless IP (10.0.0.0/8 range). Querying again with +dnssec and this time specifying NSEC as record-type, we reveal another NSEC-record and another layer deep in the tree.

```
❯ dig @127.0.66.1 hint.elite-hacker.be +dnssec NSEC

; <<>> DiG 9.20.8 <<>> @127.0.66.1 hint.elite-hacker.be +dnssec NSEC
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 26828
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: 3a480f086a9136e101000000680546aa7af11aec42ca5cbb (good)
;; QUESTION SECTION:
;hint.elite-hacker.be.		IN	NSEC

;; ANSWER SECTION:
hint.elite-hacker.be.	60	IN	NSEC	trail.hint.elite-hacker.be. A TXT RRSIG NSEC
hint.elite-hacker.be.	60	IN	RRSIG	NSEC 13 3 60 20250504114708 20250420175927 54898 elite-hacker.be. AaEyjpUBImz4fR3/c4h1iV5SK6aX4r6zfFyQP4xvINvV6jfe3ab3hUIB qXiewt+C26pZAo3uAG6mtHruZlzc2g==

;; Query time: 0 msec
;; SERVER: 127.0.66.1#53(127.0.66.1) (UDP)
;; WHEN: Sun Apr 20 21:10:34 CEST 2025
;; MSG SIZE  rcvd: 236
```

The "next secure" domain is trail.hint.elite-hacker.be, when we query that using the same arguments, we can see a pattern forming.

```
❯ dig @127.0.66.1 trail.hint.elite-hacker.be +dnssec NSEC

; <<>> DiG 9.20.8 <<>> @127.0.66.1 trail.hint.elite-hacker.be +dnssec NSEC
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 18309
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: b0c6ef03b8ec6e6301000000680546cd4fe9395444aa442e (good)
;; QUESTION SECTION:
;trail.hint.elite-hacker.be.	IN	NSEC

;; ANSWER SECTION:
trail.hint.elite-hacker.be. 60	IN	NSEC	steps.trail.hint.elite-hacker.be. A TXT RRSIG NSEC
trail.hint.elite-hacker.be. 60	IN	RRSIG	NSEC 13 4 60 20250504114708 20250420175927 54898 elite-hacker.be. AD/i4gi0tG1UM2C7HYq/++MHAO+6XUGgIq7iXq/JbffWT957scpx+Qz9 ngaMCJWI3wO24AEfAM0nuOx/TajGxw==

;; Query time: 1 msec
;; SERVER: 127.0.66.1#53(127.0.66.1) (UDP)
;; WHEN: Sun Apr 20 21:11:09 CEST 2025
;; MSG SIZE  rcvd: 248
```

Repeat this enough times to traverse the whole hierarchy and you will reach the end. Alternatively, you can use something like https://github.com/Harrison-Mitchell/NSEC-3-Walker or dns-nsec3-enum from nmap or any other tool that does this. You will often have to change their default DNS server though.

Example output from NSEC-3-Walker:
```
❯ python3 nsec-walker.py elite-hacker.be
Crawling elite-hacker.be using NS(s): 127.0.66.1
elite-hacker.be
	DNSKEY	257 3 13 6TVxRQFLFFBvB1S2dKaJ1y4ZmLAdCLij rOzui8FYxP+ppGnaDd33DZnCOJcKwq6s FQnAptKkn3LnhqAw4PyNHQ==
	NS	ns.elite-hacker.be.
	SOA	ns.elite-hacker.be. root.elite-hacker.be. 7 60 60 60 60
	TXT	"hackerDNSbb v1.0"
	TYPE65534	\# 5 0dd6720001
hint.elite-hacker.be
	A	10.0.0.3
	TXT	"A whisper in the void."
trail.hint.elite-hacker.be
	A	10.0.0.4
	TXT	"Names lead to names. Follow the trail."
steps.trail.hint.elite-hacker.be
	A	10.0.0.5
	TXT	"Every denial is a direction."
void.steps.trail.hint.elite-hacker.be
	A	10.0.0.6
	TXT	"You are walking through the void."
echo.void.steps.trail.hint.elite-hacker.be
	A	10.0.0.7
	TXT	"What you hear might be what they hide."
loop.echo.void.steps.trail.hint.elite-hacker.be
	A	10.0.0.8
	TXT	"You've been here before. Or have you?"
deny.loop.echo.void.steps.trail.hint.elite-hacker.be
	A	10.0.0.9
	TXT	"Nothing exists here. Keep looking."
nsec.deny.loop.echo.void.steps.trail.hint.elite-hacker.be
	A	10.0.0.10
	TXT	"This record proves nothing\226\128\166 or everything."
flag.nsec.deny.loop.echo.void.steps.trail.hint.elite-hacker.be
	TXT	"FLG{44-character-hex-string}"
ns.elite-hacker.be
	A	127.0.66.1
```
