# AICS - Scoring

Code used in scoring/result generation for AICS events.

[AICS](https://all-iiser-cubing-society.github.io/) conducts weekly events. A combination of Python code and Google Sheet formulas are used to generate results.

---

## Response Sheet Format

The following columns:

- Timestamp
- Name
- Institute
- For each event, the following columns
    - Time for Solve Attempt 1
    - Time for Solve Attempt 2
    - Time for Solve Attempt 3
    - Time for Solve Attempt 4
    - Time for Solve Attempt 5
    - Google Drive link for Recording

---

## Getting Started

- Make sure you have Python installed and on PATH.

- Download this repository.

  - If you are comfortable with git, clone it

    ```bash
    $ git clone git@github.com:All-IISER-Cubing-Society/scoring.git
    ```

  - Else, [Download main branch as a ZIP archive](https://github.com/All-IISER-Cubing-Society/scoring/archive/refs/heads/main.zip) and extract it.

- Open a terminal, navigate to the directory where the ZIP file has been unarchived, and install the requirements:

  ```bash
  $ pip3 install -r requirements.txt
  ```

---

## Scoring - How to compute results

- **IMPORTANT:** Make sure the times are correctly written, and in seconds. Do not format it as `mm:ss` yet. 

  - So, for example, a time of 1 minute 13.42 seconds would be written as `73.42`. 
  - `DNF` or `DNS` can be left as it is, but make sure there are no extra spaces.

- Download the full sheet as a CSV file, save it as `responses.csv`. Move this file to the directory where the code file is present.

- If the current date is also the event date for which you want to compute results, then you can simply run the program directly:

  ```bash
  $ python new-scores.py
  ```

  The program takes the current date and the `responses.csv` filename by default.

- Another date can be specified in the `YYYY-MM-DD` format (which is also called the ISO Format). Similarly, a separate filename can also be specified. Open the `new-scores.py` file and modify the very last function where the `scores` function is called as:

  ```python
  scores(eventdate='YYYY-MM-DD', responses='filename.csv')
  ```

  And then run the program.



### Program Output

- The program outputs results for each event in a `results/` directory, with the naming convention of `YYYY-MM-DD_event_id.tsv` for each event `id`.  The file can be opened in a text editor and the whole thing can be copy pasted neatly onto any Spreadsheet Program, like Google Sheets or Excel.

- The program also outputs two things for each event on the screen:

  - **WhatsApp String**
    The results are printed in a sorted order in the format:

    ```
    • AO5 - Name - Institute
    ```

    This can directly be copied and pasted onto WhatsApp.

  - **Markdown String**
    This is just the results presented as a table in Markdown. This is used to update the [Website](https://all-iiser-cubing-society.github.io/).



---

## Manual Scoring

If the scoring program fails and you are unable to figure out why, the older scoring method can be used as a fallback.

**IMPORTANT:** This needs to be done separately for each event.

### Data Preparation

- Correct any time format errors, specify them all in seconds.
  - For example, a time of 1 minute 13.42 seconds would be `73.42`.

- Copy the following columns, only of the relevant event date, onto a new worksheet on Google Sheets.

  `Name, Institute, Time 1, Time 2, Time 3, Time 4, Time 5`

  There shouldn't be any headers, only the raw data.

- Download this worksheet, rename it to `times.csv`, and move it to the folder where the code exists.



### Computing Results

- Run the `manual-scores.py` program, and it will output the AO5 result for each participant in a separate line. It outputs just the average computed times.
- Copy this whole output from the screen, and onto a new column in Google Sheets in the worksheet you formed to download as `times.csv`. [And not on the main responses worksheet.]
  - It is recommended to create a new column just left to the Names column and paste this data there.
- Since the AO5 results column has been created, the 5 columns containing times for each attempt can be deleted.
- Create a new row at the top, and write headers (for readability). 
  - Example: `AO5, Name, Institute`
- Select the data range containing the relevant data, go to `Data` Menu, and select `Create a filter`. Now the data can be sorted. Sort by the `AO5` column.



**TIP:** TIP: It is recommended to format the AO5 column as numbers with 2 decimal places, so they look uniform. Use these "Increase/Decrease decimal places" buttons to format the column.

![](https://i.imgur.com/RDs3mrJ.png)



If you want to create a WhatsApp String column like usually posted as results, create a new column, and use the following Google Sheets formula (or copy it from any of the other worksheets made):

[Assume AO5 in A2, Name in B2, Institute in C2]

```vbscript
=CONCATENATE("• ", TO_TEXT(A2) " - " B2, " - ", C2)
```

(The `TO_TEXT()` function makes sure the number formatting of 2 decimal places is maintained.)

Drag the formula down to each row, and then the whole column can be copied and pasted onto WhatsApp.

Markdown Strings are generated in a similar way.

