# authors writeup

So we got this PDF file, what do we do with it? Well, let's just open it in Firefox or any other PDF viewer. A quick search through the document doesn't reveal any "FLG"s, so the flag isn't inside the document content. Perhaps there's some data in the PDF file that's not displayed by the PDF viewer? The challenge is named "authors"... A lot of document formats have some kind of authors metadata, maybe PDF does too? Let's view the document properties in Firefox. Indeed, the Author key has the flag in it (and some other authors).

Opening the document in notepad (although counterintuitive) or running the `strings` command on Linux, would have revealed the flag faster. `strings` is one of the most useful utilities when solving stego challenges and is always worth a try!
