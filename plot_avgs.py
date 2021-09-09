import matplotlib.pyplot as plt
from matplotlib import pylab
import json
import cv2
import re

num_robots = [2, 3, 4, 5, 6]
seeds = [2, 6, 8]
difficulties = ['easy', 'medium', 'hard']

for difficulty in range(len(difficulties)):

	f_clean = open(difficulties[difficulty] + '_clean.txt', 'w')
	f_combined = open(difficulties[difficulty] + '_40_' + 'combined.txt', 'w')

	srednje_vrijednosti_clean = []

	srednje_vrijednosti_combined = []

	for robot in num_robots:

		file_clean = open('podaci' + str(robot) + '_' + str(difficulty) + '.txt', 'r')

		podaci = []
		it = 0

		for line in file_clean:
			if 'Vrijeme izvršavanja: ' in line:
				num = re.findall('[0-9]+.', line)
				minute = float(num[1][1])*60
				num = float(num[2] + num[3]) + minute
				podaci.append(num)


		sr_vr = sum(podaci)/len(podaci)
		srednje_vrijednosti_clean.append(sr_vr)
		
		srednje_vrijednosti_combined_seeds = []

		for seed in seeds:

			file_combined = open('podaci' + str(robot) + '_' + str(difficulty) + '_' + str(seed) + '_' + '40' + '.txt', 'r')

			podaci_c = []
			it = 0

			for line_c in file_combined:
				if 'Vrijeme izvršavanja: ' in line_c:
					num = re.findall('[0-9]+.', line_c)
					minute = float(num[1][1])*60
					num = float(num[2] + num[3]) + minute
					podaci_c.append(num)


			sr_vr = "{:.2e}".format(sr_vr)

			if len(podaci_c) != 0:
				sr_vr = sum(podaci_c)/len(podaci_c)
			else:
				sr_vr = 0

			srednje_vrijednosti_combined_seeds.append(sr_vr)

			if seed == 8:
				srednje_vrijednosti_combined.append(sum(srednje_vrijednosti_combined_seeds)/len(srednje_vrijednosti_combined_seeds))
				srednje_vrijednosti_combined_seeds = []

		file_combined.close()

	file_clean.close()

	# fig, ax = plt.subplots(figsize=(20, 20))
	# ax.imshow(grid, cmap='binary_r')

	plt.plot(num_robots, srednje_vrijednosti_clean)
	plt.title('Porast vremena izvršavanja sa\n porastom broja robota za ' + str(difficulties[difficulty]) + ' prepreku')
	values = ['A', 'B', 'C', 'D','E','F'] 
	plt.xlabel("Broj robota")
	plt.ylabel("Vrijeme [s]")
	plt.xticks(num_robots, num_robots)
	pylab.savefig('porast_' + difficulties[difficulty] + '.png')

	plt.clf()

	plt.plot(num_robots, srednje_vrijednosti_combined)
	plt.title('Porast vremena izvršavanja sa porastom broja robota\n za ' + str(difficulties[difficulty]) + ' prepreku sa 40 nasumičnih prepreka')
	values = ['A', 'B', 'C', 'D','E','F'] 
	plt.xlabel("Broj robota")
	plt.ylabel("Vrijeme [s]")
	plt.xticks(num_robots, num_robots)
	pylab.savefig('porast_' + difficulties[difficulty] + '_40' + '.png')

	plt.clf()


	plt.plot(num_robots, srednje_vrijednosti_clean, label="bez nasumičnih prepreka")
	plt.plot(num_robots, srednje_vrijednosti_combined, label="sa 40 nasumičnih prepreka")
	plt.legend(loc='best')
	values = ['A', 'B', 'C', 'D','E','F'] 
	plt.title('Usporedba porasta vremena izvršavanja za ' + str(difficulties[difficulty]) + '\n prepreku za slučajeve sa i bez nasumičnih prepreka' )
	plt.xlabel("Broj robota")
	plt.ylabel("Vrijeme [s]")
	plt.xticks(num_robots, num_robots)
	pylab.savefig('porast_' + difficulties[difficulty] + '_usporedba' + '.png')

	plt.clf()

