# musx-reaper
(Work in progress)

Contains code for "Random Resonances" (UIUC Music 409 Spring 2021), as well as utility functions for connecting MIDI-generating Python code to a DAW.

## Required Tools

- [Python 3](https://www.python.org/) - the base language that all of the scripting is done in.
- [musx 1.4.0+](http://cmp.music.illinois.edu/courses/taube/mus499mrc/downloads/musx-1.4.0.zip) - Python package containing many tools for algorithmic MIDI composition. Developed by Prof. Rick Taube of University of Illinois at Urbana-Champaign for Music 499: Music Representation and Composition. See the [Music 499 MRC Spring 2021 course page](http://cmp.music.illinois.edu/courses/taube/mus499mrc/) for more details, including how to use musx.
- [rtmidi](https://pypi.org/project/python-rtmidi/) - Python package that provides an API for realtime MIDI input and output
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) - Software that creates a virtual MIDI cable. Windows machines do not support virtual ports created by rtmidi, so loopMIDI is the workaround. Mac/Linux machines likely do not need loopMIDI.
- Digital audio workstation of choice - in my case I used [REAPER](https://www.reaper.fm/), but everything should generalize to other DAWs

## Included Files

- `custom_utils.py` - contains a variety of higher level functions that compose more complex MIDI sequences and control change curves, as well as other useful functions
- `random_resonances.ipynb` - notebook code used to generate MIDI for my Music 409 final project, "Random Resonances." Note that the REAPER project files are not included