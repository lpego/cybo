### This script reads in abstracts and sessions data 
### and creates a HTML table with coloured sessions etc
### no need to read final sessions, since none were changed

# %% libraries
import os
import pandas as pd
from glob import glob
from latest_file import find_most_recent_file
import datetime

# %% colour palette
palette = {
    "1. Systematics, phylogenetics, biogeography and evolution": "#A0C1E6",
    "2. Ecology": "#D5B3AE",
    "3. Biodiversity and global change": "#CE7773",
    "4. Structure, physiology, and development": "#D9CBDD",
    "5. Genetics, genomics, and bioinformatics": "#907A9D",
    "6. Plants, Fungi and Society": "#4F81BB",
}

# %% Read in most recent version of abstracts data
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[_redux].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
abstract_data = pd.read_csv(filename, skipinitialspace=True)

# %% Function to generate HTML table for a given day
def generate_html_table_posters(data, color_mode="background"):
    html_table = '<table border="1" style="border-collapse: collapse; width: 100%;">\n'
    html_table += '  <tr>\n    <th style="width: 40%;">Author</th>\n    <th style="width: 60%;">Session</th>\n  </tr>\n'
    
    poster_data = data[data['What type of contribution would you prefer to submit?'] == "Poster"]
    
    for _, row in poster_data.iterrows():
        first_name = row["First Name"] if pd.notna(row["First Name"]) else ""
        last_name = row["Last Name"] if pd.notna(row["Last Name"]) else ""
        session = row["Preferred session"] if pd.notna(row["Preferred session"]) else ""
        
        author = f'{first_name} {last_name}' if first_name and last_name else ""
        
        color = palette.get(session, "#FFFFFF")
        
        style = ' style="text-align: center;"'
        color_square = ''
        
        if color_mode in ["background", "both"]:
            style = f' style="background-color: {color}; text-align: center;"' if color else ' style="text-align: center;"'
        
        if color_mode in ["square", "both"]:
            color_square = f'<span style="display:inline-block; width:10px; height:10px; background-color:{color}; margin-right:5px;"></span>' if color else ""
        
        html_table += f'  <tr>\n    <td{style}>{color_square}{author}</td>\n    <td{style}>{color_square}{session}</td>\n  </tr>\n'
    
    html_table += '</table>\n'
    return html_table

# %% Generate HTML table for posters
html_table_posters = generate_html_table_posters(abstract_data, color_mode="square")
# Save the HTML content to a file with utf-8 encoding
filename = "posters_table.html"
with open(filename, "w", encoding="utf-8") as file:
    file.write(html_table_posters)
print(f"HTML table for posters generated and saved to {filename}")