# For using GSpread, first refer to Authentication Docs:
# https://docs.gspread.org/en/v3.7.0/oauth2.html#for-bots-using-service-account
# Make sure to share spreadsheet with the service account email

import gspread
import pandas as pd


gc = gspread.service_account()

# Open spreadsheet
sh = gc.open("All IISER Cubing Society - Weekly Race Responses")

# Get all values from first sheet - the responses sheet
df = pd.DataFrame(sh.sheet1.get_all_values())

# Rename columns with first row values
df.columns = df.iloc[0]

# Drop the first row, as it is redundant now
df.drop(0, inplace=True)

# Save as CSV
df.to_csv("responses.csv", index=False)
