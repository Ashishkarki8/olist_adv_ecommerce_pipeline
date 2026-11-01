"""
YOUR QUESTIONS (kept here so Python doesn't crash on bare text - plain text
anywhere else in a .py file is a SyntaxError; that's what comments are for):

  Q1: "does df store the data as a list of dictionaries or dictionaries?
       so df here becomes a dictionary?"
  Q2: "give me a scenario where there is an empty case so that I can print
       and look - first I wanna see what isna does"

Both are answered IN ORDER below. Work top to bottom, one STEP at a time.
Run from the project root:
    ./venv/Scripts/python.exe src/transform/inspect_dates.py
"""

import io      # lets us build a tiny CSV from text, for the STEP 5 demo
import pandas as pd    # our library, nicknamed pd so we type less


# ==================================================================
# STEP 1 - Read the CSV into a DataFrame
# ==================================================================
df = pd.read_csv("data/source/olist_orders_dataset.csv")   # source file: read only, never modified
print(df) # looks like table in structure, but is actually a DataFrame object stored in column way




# When you select one column, Pandas returns a "Series" (a single column)
order_ids = df["order_id"]
print(type(order_ids)) 
# Output: <class 'pandas.core.series.Series'>

subset=df[["order_id","order_purchase_timestamp"]]
print(type(subset)) 
# Output: <class 'pandas.core.frame.DataFrame'>

print("total rows:", df["order_id"].size) #total rows: 99441

print(df[["order_id","order_purchase_timestamp"]]) # two columns data
# Why double brackets? Because ["name", "spend"] is a Python list. You are telling Pandas: "Please select this list of columns."


data = {
    "order_id": [1, 2, 3, 4,5],
    "order_purchase_timestamp": [
        "2017-10-02 10:56:33",
        None,                  # <--- HERE IS THE MISSING DATA
        "2018-08-08 08:38:49",
        "2017-11-18 19:28:06",
        None                # <--- HERE IS ANOTHER MISSING DATA
    ]
}

# Pandas needs both lists to have the same number of values because each value in a column corresponds to a row.
df = pd.DataFrame(data)
print(f"DataFrame:\n{df}")

missing_values=df["order_purchase_timestamp"].isna().sum() #so sum counts the number of True values, which is the number of missing values in the column
print(missing_values)

# to find the place where the missing values are located, we can use the following code:

rows_with_missing = df[df["order_purchase_timestamp"].isna()]
print("--- Rows with missing timestamps ---")
print(rows_with_missing)

#   order_id order_purchase_timestamp
# 1         2                      NaN
# 4         5                      NaN

missing_indices = df[df["order_purchase_timestamp"].isna()].index.tolist()
print(f"Missing values are located at indices: {missing_indices}")
# output:  Missing values are located at indices: [1, 4]


broken_ids = df.loc[df["order_purchase_timestamp"].isna(), "order_id"].tolist()
print("Broken IDs:", broken_ids)  # Output: [2, 5]
# Broken IDs: [2, 5]




# You Write	What You Get	Use Case of nested []
# df["age"]	Series (1D)	Doing math, plotting, checking stats on one column.
# df[["age", "name"]]	DataFrame (2D)	Saving a subset of columns to a file, or passing to a model.
# df[df["age"] > 18]	DataFrame (Filtered)	Keeping only rows that meet a condition.
# df[df["age"] > 18][["name"]]	DataFrame (Filtered + Column)	"Give me the names of only adults."




parsed = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
print("parsed:\n", parsed)
# if empty or out of format it prints NaT (Not a Time) instead of crashing. This is the "coerce" part.
# parsed:
#  0   2017-10-02 10:56:33
# 1                   NaT
# 2   2018-08-08 08:38:49
# 3   2017-11-18 19:28:06
# 4                   NaT
print(f"\nData type now: {parsed.dtype}") 
# 3. Count the missing values AGAIN, but this time on the new parsed column
print(f"Missing after parsing: {parsed.isna().sum()}")

# 4. Find exactly WHERE they are missing now
print(df[parsed.isna()])






# # ==================================================================
# # STEP 2 - ANSWER TO YOUR Q1: what IS df, really?
# # It is neither a list nor a dictionary. It is a DataFrame - pandas'
# # own table type: rows down the side, named columns across the top.
# # It only LOOKS like a dictionary because df["order_purchase_timestamp"]
# # uses the same square brackets as dict["key"]. That's a look-up, not a type.
# # Proof below: print the type, then watch ONE row become a real dictionary
# # on demand - conversion is something YOU do, not what df secretly is.
# # ==================================================================
# print("--- STEP 2: what kind of thing is df? ---")
# print("type(df)          =", type(df))          # <class 'pandas.DataFrame'>
# print("type(df.columns)  =", type(df.columns))  # the column NAMES
# one_row = df.to_dict(orient="records")[0]       # convert row 0 into a dictionary
# print("row 0 as a dict   =", one_row)           # to_dict(orient="records") = list of dicts, one per row
# print("type(that row)    =", type(one_row))     # <class 'dict'> - a dict only AFTER we ask for one


# # ==================================================================
# # STEP 3 - Eyeball the raw timestamps (10 rows)
# # pandas says dtype: str at the bottom - this is TEXT, not a date yet.
# # ==================================================================
# print()
# print("--- STEP 3: first 10 raw values (eyeball check) ---")
# print(df["order_purchase_timestamp"].head(10))   # head(10) = first 10 rows only


# # ==================================================================
# # STEP 4 - isna() on our REAL column
# # isna() looks at every cell and asks "are you empty?" - True or False.
# # .sum() adds up the Trues (True counts as 1, False as 0).
# # It WILL print 0 here, and that is NOT a broken demo: isna() DID fire on
# # all 99,441 rows, it just answered False every time, because Kaggle's
# # file has no empty timestamps. Nothing to see is the finding itself.
# # ==================================================================
# print()
# print("--- STEP 4: isna() on the real column (watch it print 0) ---")
# flags = df["order_purchase_timestamp"].isna()    # one True/False per row
# print("type(flags)       =", type(flags))        # a Series of True/False
# print("first 10 flags    =", list(flags.head(10)))   # all False = no empties in sight
# print("empty values      =", flags.sum())        # expect 0


# # ==================================================================
# # STEP 5 - YOUR Q2: a scenario where isna() actually FIRES (True)
# # Our real file has no empties, so nothing real can show you a True.
# # This is the ONE invented example in this project - and it uses the
# # SAME tool (pd.read_csv) as your real file, so the mechanism is identical:
# # read_csv sees an empty cell in the CSV and stores it as NaN (a blank).
# # ==================================================================
# print()
# print("--- STEP 5: demo - an empty cell, so isna() can fire ---")

# demo_csv = """order_id,city
# o1,Recife
# o2,
# o3,Sao Paulo"""                       # row o2 has NOTHING after the comma = empty cell

# demo = pd.read_csv(io.StringIO(demo_csv))   # parse that text exactly like a real CSV file
# print(demo)                                  # o2's city shows as NaN (Not a Number)
# print("flags:", list(demo["city"].isna()))   # -> [False, True, False]  <-- isna FIRED
# print("count:", demo["city"].isna().sum())   # -> 1  (this is the same line as STEP 4)
# # Compare: same code, two files. ours = [False x 99441] -> 0, demo = one True -> 1.


# # ==================================================================
# # STEP 6 - Convert text into real datetimes
# # Pandas thinks "2017-10-02 10:56:33" is a sentence, not a date.
# # errors="coerce" = "if a value makes no sense, don't crash - write blank
# # instead", so ONE bad row can never stop the whole run.
# # ==================================================================
# print()
# print("--- STEP 6: text -> real dates ---")
# parsed = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")


# # ==================================================================
# # STEP 7 - How many FAILED to convert?
# # coerce wrote blanks where it got confused, so counting blanks =
# # counting failures. This is the real cleaning question.
# # ==================================================================
# print("--- STEP 7: rows that could NOT be parsed ---")
# print(parsed.isna().sum())            # expect 0 = column needs no cleaning


# # ==================================================================
# # STEP 8 - Sanity-check the range
# # ==================================================================
# print("--- STEP 8: date range ---")
# print("earliest:", parsed.min())      # expect 2016-09-04 21:15:19
# print(" latest:", parsed.max())       # expect 2018-10-17 17:30:18
