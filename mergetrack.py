import mido
from mido import MidiFile

filename = 'waltz8'
mid_in = MidiFile(filename+'_1.mid')
mid_out = MidiFile()

mid_out.ticks_per_beat = mid_in.ticks_per_beat
mid_out.type = mid_in.type
mid_out.charset = mid_in.charset
mid_out.add_track()
mid_out.tracks[0] = mido.merge_tracks(mid_in.tracks)

mid_out.save(filename+'_2.mid')