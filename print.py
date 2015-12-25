from mido import MidiFile

mid = MidiFile('tarantella1_1.mid')

for i, track in enumerate(mid.tracks):
    print('Track {}:'.format(i))
    for message in track:
        print(message)