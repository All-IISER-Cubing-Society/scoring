#%% 
import pandas as pd
import numpy as np
import os
from datetime import date, datetime

pd.options.mode.chained_assignment = None  # default='warn'

# %%

# Create results directory if not present
if not os.path.isdir('results'):
	os.mkdir('results')

def ao5_calc(row, event=1):
	indexes = [f"e{event}t{i}" for i in range(1, 6)]
	times = [row[index] for index in indexes]

	dnf_counter = 0
	conv_times = []

	for i in times:
		if str(i).upper() == "DNF" or str(i).upper == "DNS":
			dnf_counter += 1
			continue
		elif str(i) == "":
			dnf_counter += 1
			continue
		conv_times.append(float(i))
	if dnf_counter >= 2:
		return("DNF")
	temp = sum(conv_times)

	if len(conv_times)==5 :
		tt = temp - max(conv_times) - min(conv_times)
		return round(tt/3.0,2)
	elif len(conv_times)==4 :
		tt = temp - min(conv_times)
		return round(tt/3.0,2)


def whatsapp_string(row):
	return f"• {str(row['AO5'])} - {row['Name']} - {row['Institute']}"

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
		return None
	
	# Compute AO5 for each event
	for i in range(1, no_of_events + 1):
		df[f"e{i}ao5"] = df.apply(lambda row: ao5_calc(row, i), axis=1)


	# Results Printing and Storing
	for i in range(no_of_events):
		eventname = f"e{i+1}ao5"

		# Sort by event
		df.sort_values(eventname, inplace=True)

		# Extract event specific results
		results = df[[eventname, 'name', 'institute']]

		# Set new column names
		results.columns = ['AO5', 'Name', 'Institute']
		
		# Drop NA values
		results.dropna(inplace=True)

		# Save event results in TSV (Tab Separated Values) file
		resultspath = f"results/{eventdatestr}_event_{i+1}.tsv"
		results.to_csv(resultspath, index=False, sep='\t')
		print(f"Event {i+1} Results saved to {resultspath}\n")

		# Format time
		results['AO5'] = pd.to_datetime(results['AO5'], unit='s').dt.strftime("%M:%S.%f")
		results['AO5'] = results['AO5'].apply(format_time)

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
	scores(eventdate='2021-06-05')
# %%
