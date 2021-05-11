import musx
import rtmidi
import rtmidi.midiconstants


# ------------------- #
# MIDI Port Functions # 
# ------------------- #

def panic(port):
    """Severs a MIDI connection, in case of emergency.
    Sends note-off and control change reset messages on all channels.
    Closes down the MIDI port.

    Arguments:
        port: rtmidi MidiOut object, port to be closed down 
    """
    for channel in range(16):
        port.send_message([rtmidi.midiconstants.CONTROL_CHANGE, rtmidi.midiconstants.ALL_SOUND_OFF, 0])
        port.send_message([rtmidi.midiconstants.CONTROL_CHANGE, rtmidi.midiconstants.RESET_ALL_CONTROLLERS, 0])
    port.close_port()


def midi_restart(port, portname):
    """Closes a MIDI port and opens another.
    
    Arguments:
        port: rtmidi MidiOut object, port to be closed down
        portname: string, name of MIDI port to reopen

    Returns:
        rtmidi MidiOut object, the opened MIDI port.
    """
    panic(port)
    newport = rtmidi.MidiOut()
    newport.open_port(newport.get_ports().index(portname))
    return newport


# ---------------- #
# Helper Functions #
# ---------------- #

def bjorklund(events, positions):
    """Algorithm for spacing out events as evenly as possible.
    Euclidean-like algorithms are useful for producing rhythms found in world music.
    The most interesting results are when the two arguments have a GCD of 1.
    For example, the Cuban tresillo [x . . x . . x .] can be produced from bjorklund(3, 8), which is
    three events spaced out in an eight positions as evenly as possible.
    See http://cgm.cs.mcgill.ca/~godfried/publications/banff.pdf for more details.
    
    Arguments:
        events: int, number of active events to place
        positions: int, total number of positions that events can be placed

    Returns:
        A list of ones and zeros where ones denote an event and zeros are eventless.

    Raises:
        ValueError: There are either zero events or more events than positions.
    """
    if events > positions:
        raise ValueError("Number of events cannot exceed number of positions")
    if events == 0:
        raise ValueError("Cannot have zero events")

    sequences = ([[1] for _ in range(events)])
    remainder = ([[0] for _ in range(positions - events)])

    while len(remainder) > 0:
        diff = len(sequences) - len(remainder)

        for i in range(min(len(sequences), len(remainder))):
            sequences[i] += remainder.pop()

        if diff > 0:
            remainder = sequences[-1 * diff:].copy()
            sequences = sequences[:-1 * diff].copy()
    
    # List flattening comprehension from here: https://stackoverflow.com/questions/11264684/flatten-list-of-lists
    return [val for sublist in sequences for val in sublist]


# ------------------------- #
# Control Change Generators #
# ------------------------- #

def cc_message(queue, *, chan, ctrl, value):
    """Wrapper for sending a single control change message that can be used by a scheduler.
    
    Arguments:
        queue: musx Scheduler object, scheduler to add events to
        chan: int (0-indexed), MIDI channel to send control change message to
        ctrl: int (0-indexed), control change number
        value: int, control change value

    Yields:
        nothing, yields zero to satisfy requirements for musx Scheduler.
    """
    queue.out.addevent(musx.MidiEvent.control_change(chan, ctrl, value, time=queue.now))
    yield 0


def cc_linear(queue, *, chan, ctrl, length, start, end, low=0, high=1, grain=0.05):
    """Changes a control change value linearly over time.
    Remaps the start/end from low/high to 0-127, then evenly spaces out the changes according to a grain resolution.
    
    Arguments:
        queue: musx Scheduler object, scheduler to add events to
        chan: int (0-indexed), MIDI channel to send control change messages to
        ctrl: int (0-indexed), control change number
        length: number, total number of seconds for shift to take
        start: number, starting value
        end: number, ending value
        low: number, minimum value according to start/end's scale
        high: number, maximum value according to start/end's scale
        grain: number, timestep between control change messages

    Yields:
        number, timestep until new control change message should be sent
    """
    start_rescale = musx.rescale(start, low, high, 0, 127)
    end_rescale = musx.rescale(end, low, high, 0, 127)
    step = (end_rescale - start_rescale) / (length / grain)
    val = start_rescale
    for _ in musx.frange(0, length + grain, grain):
        queue.out.addevent(musx.MidiEvent.control_change(chan, ctrl, round(val), time=queue.now))
        val += step
        yield grain


def cc_distribution(queue, *, chan, ctrl, length, rate, distribution=musx.uniran, low=0, high=1):
    """Changes a control change value according to a distribution.
    Generates a number from the distribution function, then remaps the value from low/high to 0/127.
    
    Arguments:
        queue: musx Scheduler object, scheduler to add events to
        chan: int (0-indexed), MIDI channel to send control change messages to
        ctrl: int (0-indexed), control change number
        length: number, total number of seconds active
        rate: number, how frequently the control change value should be generated in seconds
        distribution: function, function whose returned number dictates the next control change value
        low: number, minimum value according to distribution's scale
        high: number, maximum value according to distribution's scale

    Yields:
        number, timestep until new control change message should be sent
    """
    start_time = queue.now
    while queue.now - start_time < length:
        original = max(low, min(distribution(), high))
        val = int(musx.rescale(original, low, high, 0, 127))
        queue.out.addevent(musx.MidiEvent.control_change(chan, ctrl, val, time=queue.now))
        yield rate


# --------------- #
# Note Generators #
# --------------- #

def distribution(queue, *, chan, length, notes, dur, distribution=musx.uniran, low=0, high=1):
    """Picks notes from a list according to distribution function.
    Generates a number from a distribution function, then remaps the value from low/high to a list index.

    Arguments:
        queue: musx Scheduler object, scheduler to add events to
        chan: int (0-indexed), MIDI channel to send note messages to
        length: number, total number of seconds to generate messages for
        notes: list of ints, list of MIDI note numbers to pick from
        dur: number, duration of each note in seconds
        distribution: function, function whose returned number dictates the next note
        low: number, minimum value according to distribution's scale
        high: number, maximum value according to distribution's scale

    Yields:
        number, timestep until next note should be selected and sent
    """
    start_time = queue.now
    while queue.now - start_time < length:
        selected = round(musx.rescale(distribution(), low, high, 0, len(notes) - 1))
        queue.out.addevent(musx.MidiNote(time=queue.now, dur=dur, key=notes[selected], chan=chan))
        yield dur


def euclidean_rhythm(queue, *, chan, length, keynum, events, positions, cycletime, rotation=0):
    """Plays a Euclidean rhythm.
    Uses Bjorkland's algorithm to space out events between positions evenly, then plays it.

    Arguments:
        queue: musx Scheduler object, scheduler to add events to
        chan: int (0-indexed), MIDI channel to send note messages to
        length: number, total number of seconds to generate messages for
        keynum: int, MIDI note number to send
        events: int, number of active events to place
        positions: int, total number of positions that events can be placed 
        cycletime: number, number of seconds a cycle should take
        rotation: int, position within the rhythm to start at
        
    Yields:
        number, timestep until next note message should be sent
    """
    sequence = bjorklund(events, positions)
    start_time = queue.now
    notelen = cycletime / positions
    i = rotation
    while queue.now - start_time < length:
        if sequence[i] == 1:
            queue.out.addevent(musx.MidiNote(time=queue.now, dur=notelen, key=keynum, chan=chan))
        i += 1
        i %= positions
        yield notelen


def random_ascend(queue, *, chan, length, notes, dur):
    """Plays a list of notes in an upward index trending random pattern.
    First third weights lower, second weights middle, third weights higher.
    Notes can spawn both in series and in parallel on each call.

    Arguments:
        queue: musx Scheduler object, scheduler to add events to
        chan: int (0-indexed), MIDI channel to send note messages to
        length: number, total number of seconds to generate messages for
        notes: list of ints, list of MIDI note numbers to pick from
        dur: number, duration of each note in seconds
        
    Yields:
        number, timestep until next note message should be sent
    """
    rhythms = musx.choose([dur, [0, dur/2], [0, dur/4, dur/2, 3 * (dur/4)], [0, 3 * (dur/4)], [0, 0], [0, 0, dur/2, dur/2], [0, 0, 0]]) # repeated ones are a hack for triads
    start_time = queue.now
    while queue.now - start_time < length:
        if queue.now - start_time < length * 0.33:
            ran_gen = musx.lowran
        elif queue.now - start_time < length * 0.66:
            ran_gen = musx.midran
        else:
            ran_gen = musx.highran

        r = next(rhythms)
        if musx.isnum(r):
            n = int(musx.rescale(ran_gen(), 0, 1, 0, len(notes)))
            m = musx.MidiNote(time=queue.now, dur=dur, key=notes[n], chan=chan)
            queue.out.addevent(m)
        else:
            for time in r:
                n = int(musx.rescale(ran_gen(), 0, 1, 0, len(notes)))
                m = musx.MidiNote(time=queue.now + time, dur=dur, key=notes[n], chan=chan)
                queue.out.addevent(m)
        yield dur

def drunk_walker(queue, *, chan, length, notes, dur):
    """Wrapper on musx's drunk generator to enable a track to drunkenly wander.
    If the generator falls out of bounds the index is reflected back into range.

    Arguments:
        queue: musx Scheduler object, scheduler to add events to
        chan: int (0-indexed), MIDI channel to send note messages to
        length: number, total number of seconds to generate messages for
        notes: list of ints, list of MIDI note numbers to pick from
        dur: number, duration of each note in seconds, chance to be subdivided further
        
    Yields:
        number, timestep until next note message should be sent
    """
    drunk = musx.drunk(int(len(notes) / 2), 2)
    durations = musx.choose([dur, dur/2, dur/4])
    while queue.elapsed < length:
        picked_dur = next(durations)
        index = musx.fit(next(drunk), 0, len(notes) - 1, mode='reflect')
        queue.out.addevent(musx.MidiNote(time=queue.now, dur=picked_dur, key=notes[index], chan=chan))
        yield picked_dur