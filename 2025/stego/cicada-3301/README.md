# cicada-3301 writeup

We are greeted with a web interface where you see an image that says there is a message hidden in the image.

One of the most common ways information is hidden in an image is in the exif-data. This can be viewed using a tool like exiftool https://exiftool.org/
Running exiftool on the file will reveal the flag in the Comments field of the image. This flag looks like it has the right format but the FLG is encoded with ROT13, suggesting the flag itself will probably be as well. Passing it through a ROT13-decoder or manually shifting it will reveal the flag.