#%% 
import pandas as pd
import numpy as np
from datetime import datetime

# %%

# Read file
df = pd.read_csv("responses.csv")

cols = df.shape[1]
no_of_events = (cols - 3) // 6

if (cols - 3) % 6 != 0:
	print("SHEET STRUCTURE ERROR.")

# %%
# Name of columns
colnames = ['timestamp', 'name', 'institute'] + [f"e{i}t{j}" if j < 6 else f"e{i}drive" for i in range(1, no_of_events + 1) for j in range(1, 7)]

df.columns = colnames

df

# %%
# Drop drive link columns
drives = [f"e{i}drive" for i in range(1, no_of_events + 1)]
df.drop(columns=drives, inplace=True)

df

# %%

df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('Asia/Kolkata')
df

# %%

eventdate = "2021-06-05"
eventdate = datetime.fromisoformat(eventdate)

mask = (df['timestamp'].dt.date == eventdate.date())

df = df.loc[mask]

df
# %%
def avg_calc(row, event=1):
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


# %%
# Compute A05
for i in range(1, no_of_events + 1):
	df[f"e{i}ao5"] = df.apply(lambda row: avg_calc(row, i), axis=1)

df

# %%

df.sort_values('e1ao5', inplace=True)
# %%
df
# %%
results = df[['e1ao5', 'name', 'institute']]
results.columns = ['AO5', 'Name', 'Institute']
results.dropna(inplace=True)

results
# %%
results.to_csv("teste1.tsv", index=False, sep='\t')
# %%

def whatsapp_string(row):
	return f"• {row['AO5']:.2f} - {row['Name']} - {row['Institute']}"

def markdown_string(row):
	return f"| {row['AO5']:.2f} | {row['Name']} | {row['Institute']} |"

results['whatsapp_str'] = results.apply(whatsapp_string, axis=1)
results['markdown_str'] = results.apply(markdown_string, axis=1)

results
# %%
for i in range(len(results)):
	print(results.iloc[i]['whatsapp_str'])

print()
print("Markdown\n")
print("| Average | Name | Institute |")
print("| :---: | --- | --- |")
for i in range(len(results)):
	print(results.iloc[i]['markdown_str'])

# %%
