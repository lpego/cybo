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

# %% Load the data containing author information
filename = "..\website_exports\Abstracts list for evaluation - merged_abstracts_evaluations_2025-01-16_12-16-04_FINAL.csv"
print("Reading from file: ", filename)
author_data = pd.read_csv(filename).drop(['Unnamed: 0'],axis=1)
# Replace NaN values in the 'General comments' column with the string 'none'
author_data['General comments'] = author_data['General comments'].fillna('none')

# %% merge the authors and abstract data
merged = pd.merge(abstract_data, author_data, on=['First Name', 'Last Name', 'What type of contribution would you prefer to submit?', 'Preferred session'], how='left')

# %% Function to generate HTML table for posters
def generate_html_table_posters(data, color_mode="background"):
    html_table = '<table border="1" style="border-collapse: collapse; width: 100%;">\n'
    html_table += '  <tr>\n    <th style="width: 20%;">Author</th>\n    <th style="width: 60%;">Title</th>\n    <th style="width: 20%;">Session</th>\n  </tr>\n'
    
    poster_data = data[data['What type of contribution would you prefer to submit?'] == "Poster"]
    poster_data = poster_data.sort_values(by="Preferred session")
    
    for _, row in poster_data.iterrows():
        first_name = row["First Name"].title() if pd.notna(row["First Name"]) else ""
        last_name = row["Last Name"].title() if pd.notna(row["Last Name"]) else ""
        session = row["Preferred session"] if pd.notna(row["Preferred session"]) else ""
        title = row["Title"] if pd.notna(row["Title"]) else ""
        url = row["URL_x"] if pd.notna(row["URL_x"]) else ""
        
        author = f'{first_name} {last_name}' if first_name and last_name else ""
        
        color = palette.get(session, "#FFFFFF")
        
        style = ' style="text-align: center;"'
        color_square = ''
        
        if color_mode in ["background", "both"]:
            style = f' style="background-color: {color}; text-align: center;"' if color else ' style="text-align: center;"'
        
        if color_mode in ["square", "both"]:
            color_square = f'<span style="display:inline-block; width:10px; height:10px; background-color:{color}; margin-right:5px;"></span>' if color else ""
        
        html_table += f'  <tr>\n    <td{style}>{author}</td>\n    <td{style}><a href="{url}">{title}</a></td>\n    <td{style}>{color_square}{session}</td>\n  </tr>\n'
    
    html_table += '</table>\n'
    return html_table

# %% Generate HTML table for posters
html_table_posters = generate_html_table_posters(merged, color_mode="square")
# Save the HTML content to a file with utf-8 encoding
filename = "../website_exports/HTML_tables/posters_table.html"
with open(filename, "w", encoding="utf-8") as file:
    file.write(html_table_posters)
print(f"HTML table for posters generated and saved to {filename}")