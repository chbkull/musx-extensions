################################################################################
"""
This demo uses the rotation() pattern to produce a change-ringing pattern called
Plain Hunt Minimus for 10 bells from the Cathedral Church of St. Michael in
Coventry, England. See: www.hibberts.co.uk/collect/coventry_old.htm for more
information.

To run this script cd to the parent directory of musx_demos/ and do:
```bash
python3 -m musx_demos.coventry
```
"""
__pdoc__ = {
    'conventry_fkeys': False,
}

from musx import keynum, MidiNote, allrotations


coventry_bells = {
#         hum    prime  tierce quint  nominal superq  octnom
    'a': [377,   620.5, 825.5, 1162,  1376,   2032.5, 2753.5],
    'b': [345.5, 577,   750.5, 1064,  1244,   1831,   2483],
    'c': [296,   499,   665,   874,   1114,   1647,   2241],
    'd': [285.5, 483,   626,   855.5, 1044,   1546.5, 2119],
    'e': [261,   432,   564,   760.5, 928,    1366,   1858],
    'f': [234.5, 410,   514,   672,   842,    1239,   1697],
    'g': [201,   360,   444,   598,   740,    1103,   1517],
    'h': [186,   365,   427,   552.5, 695.5,  1025.5, 1404.5],
    'i': [175,   304,   376,   514.5, 616,    908,    1243],
    'j': [159,   283.5, 343,   453.5, 558,    823,    1126]
}
"""
Conventry had 10 bells, represented here as letters 'a' to 'j'
with 'a' being the highest bell.  Rows are bell harmonics,
with the 'prime' harmonic being the main tone in each bell.
"""
    
# convert bell hertz values into equivalent floating point key numbers
_conventry_fkeys = {b: [keynum(h, filt=None) for h in l]
                       for b,l in coventry_bells.items()}


def playbells(q, peal, bells, rhy, dur, amp):
    # each bell represented by its 'prime' harmonic.
    primes = {k: bells[k][1] for k in bells.keys()}
    # play the peal (the ordered list of bells to play)
    for b in peal:
        # emphasize top and bottom bell by playing all its harmonics.
        if b in ['a','j']: 
            # keynums are quantized to 25 cents
            for k in [x for x in bells[b]]:
                m = MidiNote(time=q.now, dur=dur*4, key=k, amp=amp, tuning=4)            
                q.out.addevent(m)
        else: # else play single 'prime' note 
            k = primes[b]
            m = MidiNote(time=q.now, dur=dur, key=k, amp=amp, tuning=4)
            q.out.addevent(m)
        yield rhy


if __name__ == '__main__':
    from musx.midi.gm import Celesta, Glockenspiel, MusicBox, Vibraphone,\
        Marimba, Xylophone, TubularBells
    from musx import MidiSeq, MidiFile
    from musx import Scheduler

    # Plain Hunt change ringing for 10 bells.
    items = ['a','b','c','d','e','f','g','h','i','j']
    rules = [[0, 2, 1], [1, 2, 1]]
    items = allrotations(items, rules, False, True)
    m = MidiSeq.metaseq(ins={0: TubularBells, 1: TubularBells, 
        2: TubularBells, 3: TubularBells}, tuning=4)
    s = MidiSeq()
    q = Scheduler(s)
    q.compose(playbells(q, items, _conventry_fkeys, .25, .6, .8))
    f = MidiFile("coventry.mid", [m, s]).write()
