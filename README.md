# musx-extensions

This repository is home to two different extensions for the Python MIDI generation package, [musx](https://github.com/ricktaube/musx). musx was first developed by UIUC music composition/theory professor Rick Taube for his pilot of [Music 499: Music Representation and Composition in Spring 2021](http://cmp.music.illinois.edu/courses/taube/mus499mrc/) (note that some information here may be outdated). musx's strength is its ability to generate complex and tightly timed sequences of MIDI that can be either read as a file or streamed live to other synthesis software to generate music. These extensions are meant to operate like additional submodules of musx. That being said, neither have been rigorously tested to unearth bugs, so expect that there may be some strange behavior with some of the functions.


## musx-reaper

Music 499 covered two example use cases of musx used for live playback. One was sending MIDI to a [disklavier](https://en.wikipedia.org/wiki/Disklavier) by opening a MIDI port with [rtMIDI](https://pypi.org/project/python-rtmidi/) enabling a physical piano to be played with mechanical precision. The other was sending MIDI to [SuperCollider](https://supercollider.github.io/) over [open sound control](https://en.wikipedia.org/wiki/Open_Sound_Control) with [python-osc](https://pypi.org/project/python-osc/), allowing musx to tap into a custom SuperCollider instrument. I quickly wondered if it would be possible to control a digital audio workstation (DAW) with musx, as DAWs commonly use external MIDI keyboards as a source of input. Some experimentation and development later, musx-reaper popped out. 'Reaper' refers to my DAW of choice, [REAPER](https://www.reaper.fm/), but any DAW should work. I just think that musx-reaper sounds cooler than musx-daw, that's all :smile:.

While taking Music 499, I was also taking Music 409: Electroacoustic Music Techniques II. The final project for that class was an open-ended final electroacoustic composition, so I decided to put musx-reaper to work. The idea behind "Random Resonances" was that all of my tracks would be prepared in REAPER ahead of time, so samples would be loaded in alongside any additional plugins. However, the timeline on the project itself would be completely blank. Musx-reaper would control both the notes played and all additional parameters, and the track would be recorded to REAPER in real time. "Random Resonances" was set up such that the code was not deterministic; the composition would have the same overarching structure on each run through, but the individual details would vary. In this sense, "Random Resonances" straddles the line between traditional fixed media and live electronics.

Feel free to check out the `musx-reaper` subdirectory for more details.


## musx-images

musx-images is an image sonification library for musx. [Sonification](https://en.wikipedia.org/wiki/Sonification) is the act of taking some data source and translating it into sound. In this case, going from images to sound. musx-images provides the tools to load images and mangle them in interesting ways via OpenCV, and then it is up to the composer to decide how to precisely sonify the image. Often times this involves using some sort of mapping from a pixel color value to a frequency, but there's no 'correct' way to sonify.

musx-images was my final project for Music 499. It was inspired by a previous sonification project I had completed a few years ago, [ChromesthesiaSynth](https://github.com/chbkull/ChromesthesiaSynth). ChromesthesiaSynth was a four track audio player built in C++ that sonifies images in tandem. The project did work, but it was a bit limited in its functionality. musx-images is the spirtual successor to ChromesthesiaSynth in that it accomplishes the same goal but has been built with a bit more programming and musical maturity, and as such is a bit more capable.

Interestingly enough, musx-images is not strictly limited to images. musx's MIDI generation is primarily based on Python generators, which uses a priority queue of sorts to arrange MIDI. However, musx's built in generators only really work in one dimension. musx-images, on the other hand, implements generators that work in two dimensions. Images have pixels arranged in positions, so musx-images' generators can do interesting traversals through images that can then be sonified. However, the idea of an image is abstracted away from the generators so they should be able to work on any information passed into them that is at least two dimensions.

Feel free to check out the `musx-images` subdirectory for more details.


## Installation



Required software:
- [Python 3.9+](https://www.python.org/) - these projects were specifically developed in [Python 3.9.4](https://www.python.org/downloads/release/python-394/)
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) (musx-reaper only) - Windows does not natively support virtual MIDI cables, which is required to route Python to a DAW. loopMIDI is the workaround. Note that if you are on MacOS/Linux you will not need loopMIDI
- DAW of choice (musx-reaper only) - I specifically used [REAPER](https://www.reaper.fm/), but any DAW capable of receiving MIDI input should work
- Software capable of playing a MIDI file (musx-images only) - It is possible your system may be able to do this out of the box, otherwise try [Fluidsynth](https://www.fluidsynth.org/) in tandem with a soundfont

Note that any dependencies for packages will also need to be installed. 
Explicitly required packages:
- [musx 1.4.0](http://cmp.music.illinois.edu/courses/taube/mus499mrc/downloads/musx-1.4.0.zip) - the current release of musx is musx 2.0.4 (which can be obtained with `pip install musx`), but both projects were built while 1.4 was the newest version. The main difference between 1.4 and 2.0 was name changes, so both packages will break if 2.0 is used. The unzipped download is also included under the `musx-1.4.0` subdirectory in case the link breaks
- [rtMIDI](https://pypi.org/project/python-rtmidi/) (musx-reaper only) - enables Python to send MIDI messages in real time
- [numpy](https://pypi.org/project/numpy/) (musx-images only) - fast array manipulation
- [matplotlib](https://pypi.org/project/matplotlib/) (musx-images only) - image plotting
- [openCV](https://pypi.org/project/opencv-python/) (musx-images only) - image processing


In order to utilize either package, just direct the import to wherever you end up putting `musx_images.py` or `musx_reaper.py`.