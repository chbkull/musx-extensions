import musx
import rtmidi
import rtmidi.midiconstants

def panic(port):
    for channel in range(16):
        port.send_message([rtmidi.midiconstants.CONTROL_CHANGE, rtmidi.midiconstants.ALL_SOUND_OFF, 0])
        port.send_message([rtmidi.midiconstants.CONTROL_CHANGE, rtmidi.midiconstants.RESET_ALL_CONTROLLERS, 0])
    port.close_port()

def cc_linear(queue, chan, ctrl, *, length, start, end, low=0, high=1, grain=0.05):
    start_rescale = musx.rescale(start, low, high, 0, 127)
    end_rescale = musx.rescale(end, low, high, 0, 127)
    step = (end_rescale - start_rescale) / (length / grain)
    val = start_rescale
    for _ in musx.frange(0, length + grain, grain):
        queue.out.addevent(musx.MidiEvent.control_change(chan, ctrl, round(val), time=queue.now))
        val += step
        yield grain

def midi_restart(port, portname):
    panic(port)
    newport = rtmidi.MidiOut()
    newport.open_port(newport.get_ports().index(portname))
    return newport


def bjorklund(events, steps):
    """
    This is a test docstring.
    """
    if events > steps:
        raise ValueError("Number of events cannot exceed number of steps")

    sequences = ([[1] for _ in range(events)])
    remainder = ([[0] for _ in range(steps - events)])

    while len(remainder) > 0:
        diff = len(sequences) - len(remainder)
        for i in range(min(len(sequences), len(remainder))):
            sequences[i] += remainder.pop()

        if diff > 0:
            remainder = sequences[-1 * diff:].copy()
            sequences = sequences[:-1 * diff].copy()
    
    # List flattening comprehension from here: https://stackoverflow.com/questions/11264684/flatten-list-of-lists
    return [val for sublist in sequences for val in sublist]