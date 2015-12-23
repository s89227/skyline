import mido
import operator
from mido import MidiFile


filename = 'test2'
mid_in = MidiFile(filename+'.mid')

#change time
"""for i in range(0,len(mid_in.tracks)-1,1):
    t=0
    for j in range(1,len(mid_in.tracks[i])-1,1):
       	t += mid_in.tracks[i][j].time
       	mid_in.tracks[i][j].time = t"""

mid_out = MidiFile()
now_on = []
now_on_msg = []
sky = mido.Message('note_on', note=0, velocity=0, time=0)
tick = 0

#mido.merge_tracks(mid_in.tracks)

#set file
mid_out.ticks_per_beat = mid_in.ticks_per_beat
mid_out.type = mid_in.type
mid_out.charset = mid_in.charset

#skyline for every tracks
for i, track in enumerate(mid_in.tracks):
	#create same number of track of mid_in for mid_out
	mid_out.add_track()
	#mid_out.tracks[i].name = track.name

	for message in track:
		#meta message
		if message.type != 'note_on' and message.type != 'note_off':
			#message.time += tick
			#tick = 0
			#mid_out.tracks[i].append(message)
			print(1)

		#note on event
		elif message.type == 'note_on' and message.velocity != 0:
			if message.note >= sky.note:
				if(sky.note > 0):
					sky.time = 0
					now_on.append(sky.note)
					now_on_msg.append(sky)
					#sort by note(low to high)
					now_on.sort()
					now_on_msg.sort(key=lambda message: message.note)

					temp = mido.Message('note_off')
					temp.note = sky.note
					temp.channel = sky.channel
					temp.velocity = 0
					temp.time = message.time
					message.time = tick
					tick = 0
					mid_out.tracks[i].append(temp)
					mid_out.tracks[i].append(message)
					sky = message
				else:
					message.time += tick
					tick = 0
					mid_out.tracks[i].append(message)
					sky = message

			elif not(message.note in now_on):
				tick += message.time
				message.time = 0
				now_on.append(message.note)
				now_on_msg.append(message)
				#sort by note(low to high)
				now_on.sort()
				now_on_msg.sort(key=lambda message: message.note)

			else:
				tick += message.time
				now_on_msg.pop(now_on.index(message.note))
				now_on_msg.insert(now_on.index(message.note),message)

		#note off event
		else:
			if message.note >= sky.note:
				message.time += tick
				mid_out.tracks[i].append(message)
				tick = 0
				if len(now_on)!=0:
					now_on.pop()
					message = now_on_msg.pop()
					message.time = 0
					mid_out.tracks[i].append(message)
					sky = message
				else:
					sky = mido.Message('note_on', note=0, velocity=0, time=0)

			else:
				tick += message.time
				if message in now_on_msg:
					now_on_msg.pop(now_on_msg.index(message))
				if message.note in now_on:
					now_on.remove(message.note)

	del now_on[:]
	del now_on_msg[:]
	sky = mido.Message('note_on', note=0, velocity=0, time=0)
	tick = 0

#change time back
"""for i in range(len(mid_out.tracks)-1,0,-1):
	for j in range(len(mid_out.tracks[i])-1,1,-1):
		mid_out.tracks[i][j].time = mid_out.tracks[i][j].time - mid_out.tracks[i][j-1].time
		if mid_out.tracks[i][j].time < 0:
			mid_out.tracks[i][j].time = 0"""

"""for i, track in enumerate(mid_out.tracks):
    print('Track {}: {}'.format(i, track.name))
    for message in track:
        print(message)"""

mid_out.save(filename+'_1.mid')