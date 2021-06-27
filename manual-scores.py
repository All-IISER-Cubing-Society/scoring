# Original Scoring Code
# Author: Kartik Bhide, IISER TVM
# Comments by Purva

# Script to read participant times, calculate and return averages
import csv

# Calculate Average of 5 for a given set of times
# AO5 Spec: Regulation 9f9 and 959
# https://www.worldcubeassociation.org/regulations/#9f8
def avg_calc(times):
	"""Calculate average of 5 for a given list of times

	Args:
		times (list): List of times, in seconds

	Returns:
		float or str: AO5 score or DNF
	"""
	dnf_counter = 0
	conv_times = []
	
	for i in times:
		if i.upper() == "DNF":
			dnf_counter += 1
			continue
		elif i == "":
			dnf_counter += 1
			continue
		conv_times.append(float(i))
	
	# If there are 2 or more DNFs, return DNF
	# Regulation 9f9
	if dnf_counter >= 2:
		return("DNF")

	# Sum all the times
	temp = sum(conv_times)

	# If all times present, subtract best and worst
	if len(conv_times)==5 :
		tt = temp - max(conv_times) - min(conv_times)
		return round(tt/3.0,2)

	# If one attempt is DNF, subtract only the best (as DNF is the worst)
	elif len(conv_times)==4 :
		tt = temp - min(conv_times)
		return round(tt/3.0,2)
		

# Table Format
# Name | Institute | Time 1 | Time 2 | Time 3 | Time 4 | Time 5


# Read the times.csv file
with open('times.csv', 'r') as csv_file:

	csv_reader = csv.reader(csv_file)
	
	# Pass each times list to function
	for line in csv_reader:
		print (avg_calc(line[2:]))
