################################################################################
"""
Isorhythmic piano and cello parts to Liturgie de Cristal, by Olivier Messiaen.

Both parts employ a rotational technique taken from isorythmic motets in the 
middle ages that produce cyclical patterns of rhythms (talea) and pitches 
(color) that don't line up each time they repeat.

For larger examples using paint.py see the demos gamelan.py and blues.py.

To run this script cd to the parent directory of musx_demos/ and do:
```bash
python3 -m musx_demos.messiaen
```
"""


from musx.paint import brush, spray
from musx.midi import MidiNote, MidiSeq, MidiFile
from musx.scheduler import Scheduler
from musx.tools import playfile, setmidiplayer
from musx.rhythm import rhythm
from musx.scales import keynum
from musx.midi.gm import AcousticGrandPiano, Violin


piano_talea = rhythm('q q q e e. e e e e e. e. e. s e e. q h', tempo=80)


piano_color = keynum(["f3 g bf c4 ef b e5",  "f3 g bf c4 e a d5", 
                      "f3 af bf df4 ef a d5", "f3 af bf df4 ef g c5",
                      "f3 g bf d4 fs b c5", "f3 g bf d4 e a c5",
                      "f3 a c4 d g cs5 fs", "f3 g c4 d g b e5", 
                      "f3 bf df4 gf e5", "f3 b d4 g e5 g", "f3 c4 ef af g5", 
                      "f3 cs4 e a g5 b", "af3 ef4 gf bf ef5 gf cf6", 
                      "af3 ef4 f bf df5 f5 bf5", "gf3 df4 af ef af cf6 ef", 
                      "gf3 df4 bf d5 f bf d6", "a3 c4 d fs bf df5 gf bf df6", 
                      "bf3 cs e gs c5 d gs c6", "c4 d f a4 cs5 e a", 
                      "cs4 e fs bf d5 f", "fs4 g bf d5 fs a",
                      "fs4 a b ds5 es gs", "f4 bf d5 e g", 
                      "e4 af cs5 d", "d4 g b cs5 e", "cs4 f bf b f5",
                      "b3 e4 af bf", "af3 cs4 f g", "gf3 cf4 ef f"])


cello_talea = rhythm('h q. h h e e q. e e e e q. e e h', tempo=80)


cello_color = keynum('c6 e d f# bf5')


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq(ins={0: AcousticGrandPiano, 1: Violin})
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.[84, 88, 86, 90, 82]
    q = Scheduler(t1)
    # Create the piano and cello composers.
    piano=brush(q, len=len(piano_talea) * 8 + 14, rhy=piano_talea,
                key=piano_color, chan=0)
    cello=brush(q, len=len(cello_talea) * 6, rhy=cello_talea,
                amp=.2, key=cello_color, chan=1)
    # Start our composers in the scheduler, this creates the composition.
    q.compose([[0, piano], [5.5, cello]])
    # Write a midi file with our track data.
    f = MidiFile("messiaen.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)
