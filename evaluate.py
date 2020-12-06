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

def plotDurByDate(name):
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
	ax.bar(dts.date2num(date_list), dur_list, color='blue')
	ax.bar(dts.date2num(date_list2), dur_list2, color='red')
	ax.xaxis_date()

	plt.show()
	plt.pause(10000)

plotDurByDate('<NAME>')
