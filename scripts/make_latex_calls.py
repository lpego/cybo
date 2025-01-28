### This scripts generates the LaTeX \confpin calls
### based on name patterns and file names

# %%
import os
import pandas as pd
from glob import glob
import random
from latest_file import find_most_recent_file

# %% Read in most recent version of abstracts data
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[_redux].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
abstract_data = pd.read_csv(filename, skipinitialspace=True)

# %% use manually checked affiliations for nametags
institution = pd.read_csv("..\\website_exports\\unique_institutions.csv")
abstract_data_new = abstract_data.merge(institution, left_on="Contributing author's institution", right_on="original", how="left")
len(abstract_data_new) == len(abstract_data) # check if all rows are still there

# %% Generate LaTeX code for name badges, with four fields
backgrounds = ['BC_1_noqr.svg', 'BC_2_noqr.svg', 'BC_3_noqr.svg']
latex_code = []
for index, row in abstract_data_new.iterrows():
    first_name = row["First Name"].title()
    last_name = row["Last Name"].title()
    institution = row["shortened"]
    country = row["country"]
    institution_country = f"{institution} ({country})"
    bkg = random.choice(backgrounds)
    surname = last_name.replace(" ", "-")
    name = first_name.replace(" ", "-")
    filename = f"{surname}_{name}"
    latex_code.append(f"\\confpin{{{first_name} {last_name}}}{{{institution_country}}}{{{filename}.svg}}{{{bkg}}}")

# Print LaTeX code
for line in latex_code:
    print(line)
