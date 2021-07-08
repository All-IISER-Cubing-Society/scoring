#%% 
import pandas as pd
import numpy as np
import os
import sys
from datetime import date, datetime

pd.options.mode.chained_assignment = None  # default='warn'

# %%
def ao5_calc(row, event=1):
	"""Compute Average of 5 for a given row and event id
	as per Regulations 9f8 and 9f9

	Args:
		row (pd.DataFrame row): DataFrame row containing name, institute and times
		event (int, optional): Event Number. Defaults to 1.

	Returns:
		float or str: AO5 score or DNF
	"""

	# Generate event time column names
	# For example, in event=1: e1t1, e1t2, e1t3, e1t4, e1t5
	indexes = [f"e{event}t{i}" for i in range(1, 6)]

	# Get times for the event
	times = [row[index] for index in indexes]

	dnf_counter = 0
	conv_times = []

	for i in times:
		if str(i).upper() == "DNF" or str(i).upper() == "DNS":
			dnf_counter += 1
			continue
		elif str(i) == "":
			dnf_counter += 1
			continue
		conv_times.append(float(i))

	# If there are 2 or more DNFs (or DNS), return DNF
	# As per Regulation 9f9
	if dnf_counter >= 2:
		return("DNF")

	# Sum all times
	temp = sum(conv_times)

	# If all times present, subtract best and worst
	if len(conv_times)==5 :
		tt = temp - max(conv_times) - min(conv_times)
		return round(tt/3.0,2)
	
	# If one attempt is DNF/DNS, subtract only the best (as DNF/DNS is the worst)
	elif len(conv_times)==4 :
		tt = temp - min(conv_times)
		return round(tt/3.0,2)


def whatsapp_string(row):
	"""Generate WhatsApp String for a given DataFrame row

	Args:
		row (pd.DataFrame row): DataFrame row containing AO5, Name, Insitute data

	Returns:
		str: WhatsApp String of the form "• AO5 - Name - Institute"
	"""

	if row['Institute']:
		institute_string = f" - {row['Institute']}"
	else:
		institute_string = ""

	return f"• {str(row['AO5'])} - {row['Name']}{institute_string}"

# %%
def format_time(time):

	# Remove the last four zeros in microseconds
	time = time[:-4]

	# If minutes is 00, remove it
	minutes = time[:2]
	if minutes == "00":
		time = time[3:]

	return time

# %%
def scores(responses="responses.csv", eventdate=date.today().isoformat()):
	"""Scores calculation and printing for a given event date
	It generates results in the results directory, 
	and also prints WhatsApp and Markdown Strings to the screen

	Args:
		responses (str, optional): File name of responses data. Defaults to "responses.csv".
		eventdate (str, optional): Event date in ISO Format. Defaults to date.today().isoformat().
	"""
	# Read responses file
	df = pd.read_csv(responses)

	# Extract number of columns
	cols = df.shape[1]

	# Compute number of events
	no_of_events = (cols - 3) // 6
	
	# If division remainder is not 0, sheet structure has changed
	if (cols - 3) % 6 != 0:
		print("SHEET STRUCTURE ERROR.")

	# Set column names
	# Format: timestamp, name, institute
	# And then for each event i: eit1, eit2, eit3, eit4, eit5, eidrive
	colnames = ['timestamp', 'name', 'institute'] + [f"e{i}t{j}" if j < 6 else f"e{i}drive" for i in range(1, no_of_events + 1) for j in range(1, 7)]

	df.columns = colnames

	# Drop drive link columns
	drives = [f"e{i}drive" for i in range(1, no_of_events + 1)]
	df.drop(columns=drives, inplace=True)

	# Set timestamp as datetime type, timezone-naive
	# To make timezone aware: df['timestamp].dt.tz_localize('Asia/Kolkata)
	df['timestamp'] = pd.to_datetime(df['timestamp'])

	# Convert event date to datetime type
	eventdatestr = eventdate
	eventdate = datetime.fromisoformat(eventdate)

	# Keep only eventdate data in df
	mask = (df['timestamp'].dt.date == eventdate.date())
	df = df.loc[mask]

	if df.empty:
		print("No data for given event date. Supply a valid date.")
		return
	
	# Compute AO5 for each event
	for i in range(1, no_of_events + 1):
		df[f"e{i}ao5"] = df.apply(lambda row: ao5_calc(row, i), axis=1)


	# Results Printing and Storing
	for i in range(no_of_events):
		eventao5 = f"e{i+1}ao5"

		# Sorting will fail if AO5 column contains DNF
		# Replace DNF with 99999 temporarily
		df[eventao5] = df[eventao5].replace("DNF", 99999)

		# Sort by event
		df.sort_values(eventao5, inplace=True)

		# Replace 99999 with DNF again
		df[eventao5] = df[eventao5].replace(99999, "DNF")

		# Extract event specific results
		results = df[[eventao5, 'name', 'institute']]

		# Set new column names
		results.columns = ['AO5', 'Name', 'Institute']
		
		# Drop NA values
		results.dropna(inplace=True)

		# If no data here, skip
		if results.empty:
			continue

		# Create results directory if not present
		if not os.path.isdir('results'):
			os.mkdir('results')

		# Save event results in TSV (Tab Separated Values) file
		resultspath = f"results/{eventdatestr}_event_{i+1}.tsv"
		results.to_csv(resultspath, index=False, sep='\t')
		print(f"Event {i+1} Results saved to {resultspath}\n")

		# Replace DNF with 99999 temporarily
		results['AO5'] = results['AO5'].replace("DNF", 99999)

		# Format time
		results['AO5'] = pd.to_datetime(results['AO5'], unit='s').dt.strftime("%M:%S.%f")
		results['AO5'] = results['AO5'].apply(format_time)

		# Convert 99999 back to DNF
		# 99999 formatted to 46:39.00 by the code above
		results['AO5'] = results['AO5'].replace("46:39.00", "DNF")

		# Compute strings
		markdown_str = results.to_markdown(index=False, floatfmt=".2f", colalign=('center', 'left', 'left'))
		results['whatsapp_str'] = results.apply(whatsapp_string, axis=1)

		# Print Strings
		print(f"WhatsApp String - Event {i+1}\n")
		for j in range(len(results)):
			print(results.iloc[j]['whatsapp_str'])

		print()
		print(f"Markdown String - Event {i+1}\n")
		print(markdown_str)

		print("\n\n--------------------------------\n\n")

	print("COMPLETE")

		

# %%
if __name__ == "__main__":
	n = len(sys.argv)

	if n == 1:
		scores()
	elif n == 2:
		if ".csv" in sys.argv[1]:
			scores(responses=sys.argv[1])
		else:
			scores(eventdate=sys.argv[1])
	elif n == 3:
		scores(eventdate=sys.argv[1], responses=sys.argv[2])
	else:
		print("Invalid Command Line Arguments. Correct Usage:")
		print(f"python {__file__} [yyyy-mm-dd] [filename.csv]")
		print(f"""
	Example Usages:
	-> python {__file__} 2021-06-05
	-> python {__file__} datafilename.csv
	-> python {__file__} 2021-06-05 datafilename.csv 
	""")

# %%
