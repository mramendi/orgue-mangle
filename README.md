# orgue-mangle

This is a set of utilities for mangling MIDI recordings for GrandOrgue. They are written in Python 3.

By Misha Ramendik mr@ramendik.ru

The do not work on MIDI directly, instead they use the text format from MidiComp https://github.com/markc/midicomp

The utilities are very much a work in progress right now. They include:

* degluk.py: a debouncer, which is currently hardcoded for a 30 ms sensititity
* dumbshift.py: a "dumb" shifter of all timestamps (except 0) by an integer value
* partshift.py: a shifter of all timestamps starting with a given valye by an integer value. This can add a pause - or "cut out" a bit, but cutting only works for periods where there are no MIDI events
* rezak.py: cuts out the first N seconds of the recording, while preserving setup of stops etc
* slower.py: very simple tempo changer that can only make things N times slower. Intended for analysis purposes. Will likely be removed.
* tempochange.py: an actual tempo changer. Changes the tempo to a given percentage, either for the entire recording or from a start position or from a start position to an end position. 

MIT License. Disclaimer: while Misha is a Red Hat employee this is not Red Hat code.

