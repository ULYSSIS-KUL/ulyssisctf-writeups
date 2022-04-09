# my-cute-tea writeup

This challenge is fairly straightforward.
We are confronted with a URL pointing to a "MQTT broker".
A quick online search teaches us that MQTT is a protocol often used to communicate with Internet of Things devices, and that "brokers" serve as a place for clients to read data and sensors to publish data.

So we try to find a suitable MQTT client. [Mosquitto](https://mosquitto.org/) will do.
We type `mosquitto_sub -h 172.16.10.10 -t tea` to connect to the broker and are greeted with a temperature around 90 degrees, every four seconds or so.
While poring over the possible meaning behind this temperature, we suddenly see a FLG{}! And we've solved the challenge!
