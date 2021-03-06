################################################################################
"""
gamelan.py generates a gamelan composition using the `brush()` and `spray()`
generators in paint.py. Composer: Ming-ching Chiu.

To run this script cd to the parent directory of musx_demos/ and do:
```bash
python3 -m musx_demos.gamelan
```
"""


if __name__ == '__main__':
    from musx.paint import brush, spray
    from musx.midi import MidiNote, MidiSeq, MidiFile
    from musx.scheduler import Scheduler
    from musx.generators import cycle, choose
    from musx.tools import playfile, setmidiplayer
    from musx.midi.gm import Vibraphone

    # Scale1 is a 7-tone microtonal scale that evokes the Pelog scale.
    scale1 = [0, 2.2, 3.8, 6.6, 7.1, 9.3, 10, 12, 14.4, 15.8, 18.6, 19.1]
    # Scale2 is a 5-tone pentatonic scale that evokes the Slendro scale.
    scale2 = [0, 2, 3.7, 6.9, 9.1]
    scale3 = [[0, 6.9], [2, 6.9], [3.7, 9.1], [9.1, 14], [3.7, 12]]
    melody = [[36, 43.1, 46], [42.6, 50.2], [38.2, 48, 51.8], [39.8, 46, 54.6],
              [54.6, 62.2, 66.6], [57.3, 66.6, 69.3], [58, 62.2, 67.1], 
              [36, 45.3, 48], [60, 66.6, 69.3], [46, 55.1, 60], 
              [42.6, 50.2, 57.3], [46, 55.1, 60], [57, 66.6, 69.3], 
              [57.3, 66.6, 69.3], [54.6, 62.2, 66.6]]
    # Amplitude scaler to adapt to different sound fonts. this is for fluidsynth
    def A(a): return ([s * 1.35 for s in a] if type(a) is list else a*1.5)
    # Microtonal divisions of the semitone. 2 is quartertone (50 cents) etc.
    tuning=7
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq(ins={i: Vibraphone for i in range(tuning)}, tuning=tuning)
    # Track 1 holds the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)
     # The sections of the piece
    s1=spray(q, key=48, dur=3, rhy=[1, .5], amp=A([.3, .35, .4]),
                band=scale1, end=40, tuning=tuning)
    s2=spray(q, key=48, dur=3, rhy=[1, .5], amp=A([.4, .45, .5]), 
                band=scale3, end=25, tuning=tuning)
    s3=spray(q, key=72, dur=3, rhy=[.75, .25, .5], amp=A([.4, .3, .35]),
                band=[3.8, 7.1, [9.3, 14.4]], end=35, tuning=tuning)
    s4=spray(q, key=72, dur=3, rhy=[.75, .25, .5], amp=A([.6, .5, .55]),
                band=[9.3, 12, 14.2, 18.6, [26.2, 30.6]], end=30, tuning=tuning)
    s5=spray(q, key=84,  dur=3, rhy=[.75, .25, .5], amp=A([.6, .5, .55]),
                band=[3.8, 7.1, 9.3, [7.1, 12]],  end=15, tuning=tuning)
    s6=spray(q, key=24,  dur=5, rhy=[1, 1, .5, 2, 2], amp=A(.5),
                band=scale2, end=55, tuning=tuning)

    s7=brush(q, key=[86.2, 93.3, 87.8, 91.1], dur=4, rhy=[.25, .25, .5], 
                amp=A(.3), end=50, tuning=tuning)
    s8=brush(q, key=[86.2, [93.3, 98.8], 87.8, 91.1], dur=4,
                rhy=[.25, .25, .25, .25, .5], amp=A(.25), end=10, tuning=tuning)
    s9=brush(q, key=[81.3, 74.4, 78.6, 72], dur=2, rhy=[.5, .25, .25],
                amp=A(.25), end=50, tuning=tuning)
    s10=brush(q, key=melody, dur=8,
                 rhy=[2, 1, 1, .5, .5, 3, 1.5, 1.5, 4, 2, 1, 1, .5, .5, 3, 1.5, 1.5, 1.5, .5, 4],
                 amp=A([.3, .4, .35, .35]), end=40, tuning=tuning)

    s11=spray(q, key=72, dur=2, rhy=1/3, amp=A(.18),
                 band=[[0, 14.4], [3.8, 12], [15.8, 7.1], [2.2, 9.3], [0, 10],
                       [9.3, 2.2], [7.1, 14.4], [0, 9.3], [3.8, 12]],
                 end=36, tuning=tuning)
    s12=spray(q, key=60, dur=2, rhy=.5, amp=A(.25), band=scale2, end=41, tuning=tuning)
    s13=spray(q, key=48, dur=4, rhy=[1, 1, 2, 1, 1, 1, 1, 1, .5, .5, 2, 1, .5, .5, 1, 1, 2, 2, .5, .5, 1, 4],
                 amp=A(.35), band=scale3, end=32, tuning=tuning)
    s14=brush(q, key=[[36, 42.6, 43.1, 48, 51.8, 57.3, 63.8, 86.4], [12, 24, 31.1, 36, 42.6]],
                 len=2, dur=8, rhy=[4, 8], amp=A(.25), tuning=tuning)
    # Start our composers in the scheduler, this creates the composition.
    q.compose([[0, s1], [40, s2], [10, s3], [40, s4], [50, s5], [20, s6],
               [65, s7], [80, s8], [73, s9], [79, s10],
               [121, s11], [121, s12], [129, s13], [162, s14] ] )
    # Write a midi file with our track data.
    f = MidiFile("gamelan.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)
