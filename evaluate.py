from xml.dom import minidom
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as dts

FILENAME = 'logs.xml'

file = minidom.parse(FILENAME)
calls = file.getElementsByTagName('log')

# name, date, time, dur, type {1: eingehend 2: ausgehend 3: verpasst}
log = []

for call in calls:
	log.append([call.attributes['name'].value, datetime.strptime(call.attributes['time'].value[:10], '%d.%m.%Y'), call.attributes['time'].value[11:], int(call.attributes['dur'].value), int(call.attributes['type'].value)])
	# if str(log[-1][2]).startswith("06"):
	#	print(log[-1])

def map(value, start1, stop1, start2, stop2):
	return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

# Plotting the call duration by date. The parameter <name> allows you to plot calls for a specific contact on your phone [but is not necessary].
def plotDurByDate(name = '#'):
	date_list = []
	dur_list = []
	current_date = log[0][1]
	current_dur = 0

	date_list2 = []
	dur_list2 = []
	current_date2 = log[0][1]
	current_dur2 = 0

	for entry in log:
		if entry[0] == name:
			if entry[1] == current_date:
				current_dur += entry[3]
			else:
				date_list.append(current_date)
				dur_list.append(current_dur)
				current_date = entry[1]
				current_dur = entry[3]
		else:
			if entry[1] == current_date2:
				current_dur2 += entry[3]
			else:
				date_list2.append(current_date2)
				dur_list2.append(current_dur2)
				current_date2 = entry[1]
				current_dur2 = entry[3]
	
	# plt.plot_date(dts.date2num(date_list), dur_list, '.b')

	ax = plt.subplot(111)
	ax.bar(dts.date2num(date_list), dur_list, color='red')
	ax.bar(dts.date2num(date_list2), dur_list2, color='blue')
	ax.xaxis_date()

	plt.show()
	plt.pause(10000)

def plotAmountByTime(name = '#'):
	time_list = []
	times_list = []
	n = -1
	for entry in log:
		if entry[0] == name:
			hour = int(str(entry[2])[0:2]) * 100
			minu = int(str(entry[2]).replace(':', '')[2:-2])

			mapped = map(minu, 0, 59, 0, 99)
			tmp = hour + mapped

			# print(str(entry[2]), '->', str(hour) + ':' + str(minu), 'Mapped:', mapped, 'hour + mapped', tmp)

			if tmp not in times_list:
				times_list.append(tmp)
				time_list.append(1)
				n += 1
			else:
				for i in range(0, n):
					if times_list[i] == tmp:
						time_list[i] += 1
	plt.style.use('dark_background')
	times_list, time_list = zip(*sorted(zip(times_list, time_list)))
	plt.plot(times_list, time_list, '-m')
	# plt.scatter(times_list, time_list)
	plt.show()
	plt.pause(10000)


# plotAmountByTime()
plotDurByDate()