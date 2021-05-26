# musx-images
Musx-images is an image sonification library for musx.

Musx is a python package containing many tools for algorithmic MIDI composition. Developed by Prof. Rick Taube of University of Illinois at Urbana-Champaign for Music 499: Music Representation and Composition. See the [Music 499 MRC Spring 2021](http://cmp.music.illinois.edu/courses/taube/mus499mrc/) course page for more details, including how to use musx. The backbone of the musx-images package is that the generators included in it work on two dimensional datasets. This is particularly useful for images, which have inherent positional data. That being said, the two dimensional generators should work on any data passed into it that is at least two dimensions.

See the examples directory for three juypter notebooks that walk through some of musx-images' features. They all use the same compositional backbone, but process over images differently. If anything, musx-images is about importing image data into musx, and then going from there. There are not too many different compositional tools included- musx is great at sculpting MIDI by itself. See the images directory for the source images as well as where they were obtained.

## Required Libraries
- musx 1.4.0 (included in this repository)
- numpy
- matplotlib
- openCV
- MIDI file player (Fluidsynth)