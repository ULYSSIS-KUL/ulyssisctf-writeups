# dc-timelapse writeup
In this challenge, we get a video of the construction of ICTS' new datacenter, with music. After a few seconds there is an obvious distortion to be heard in the music.
Since the music does seem intact, with the distortion added on top, and with pauses at regular intervals, it seems the key could be encoded in the distortion. After extracting the audio from the video, and generating a spectrogram for it, the flag is easily readable from the spectrogram.
