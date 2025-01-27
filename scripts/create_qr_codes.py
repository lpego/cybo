### This scripts generates QR codes based on abstract URLs
### for name badges

# %%
import os
import pandas as pd
from glob import glob
import random
from latest_file import find_most_recent_file
import qrcode
import qrcode.image.svg
from qrcode.image.pure import PyPNGImage

# %% Read in most recent version of abstracts data
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[_redux].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
abstract_data = pd.read_csv(filename, skipinitialspace=True)

# %% get list of URLs, check if only unique values
abstract_URLs = abstract_data["URL"].tolist()
len(abstract_URLs) == len(set(abstract_URLs)) # only unique values?

# %% Create save dir for QR codes if it doesn't exist
save_dir = "../website_exports/QR_codes"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# # %% Generate QR codes for all URLs
# for index, row in abstract_data.iterrows():
#     url = row["URL"]
#     surname = row["Last Name"].replace(" ", "-")
#     name = row["First Name"].replace(" ", "-")
#     filename = f"{surname}_{name}"
#     print(url)
#     ### SVG 
#     img_svg = qrcode.make(url, image_factory=qrcode.image.svg.SvgImage)
#     with open(f'{save_dir}/{filename}.svg', 'wb') as qr:
#         img_svg.save(qr)
#     ### PNG
#     img_png = qrcode.make(url, image_factory=PyPNGImage)
#     with open(f'{save_dir}/{filename}.png', 'wb') as qr:
#         img_png.save(qr)

# %% Generate LaTeX code for name badges, with four fields
backgrounds = ['BC_1_noqr.svg', 'BC_2_noqr.svg', 'BC_3_noqr.svg']
latex_code = []
for index, row in abstract_data.iterrows():
    first_name = row["First Name"]
    last_name = row["Last Name"]
    institution = row["Contributing author's institution"]
    bkg = random.choice(backgrounds)
    surname = last_name.replace(" ", "-")
    name = first_name.replace(" ", "-")
    filename = f"{surname}_{name}"
    latex_code.append(f"\\confpin{{{first_name} {last_name}}}{{{institution}}}{{{filename}.svg}}{{{bkg}}}")

# Print LaTeX code
for line in latex_code:
    print(line)
