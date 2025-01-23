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

# %% Load the data from the CSV file
filename = "d:/cybo/website_exports/Programme_2025 - Sheet10.csv"
talk_data = pd.read_csv(filename)

# %% Reshape talk_data to have one "First Name" and one "Last Name" column per row
talk_data_a = talk_data[['Date', 'Time', 'Activity', 'First Name - Track A', 'Last Name - Track A', 'Session - Track A']]
talk_data_a = talk_data_a.rename(columns={
    'First Name - Track A': 'First Name A',
    'Last Name - Track A': 'Last Name A',
    'Session - Track A': 'Session A',
    'Title - Track A': 'Title A'
})

talk_data_b = talk_data[['Date', 'Time', 'Activity', 'First Name - Track B', 'Last Name - Track B', 'Session - Track B']]
talk_data_b = talk_data_b.rename(columns={
    'First Name - Track B': 'First Name B',
    'Last Name - Track B': 'Last Name B',
    'Session - Track B': 'Session B',
    'Title - Track B': 'Title B'
})

reshaped_talk_data = pd.merge(talk_data_a, talk_data_b, on=['Date', 'Time', 'Activity'], how='outer')

# %% Load the data containing abstract information
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[_redux].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
abstract_data = pd.read_csv(filename, skipinitialspace=True)

# %% Merge the reshaped talk data and author data
merged_data = pd.merge(reshaped_talk_data, abstract_data, left_on=['First Name A', 'Last Name A'], right_on=['First Name', 'Last Name'], how='left')
merged_data = pd.merge(merged_data, abstract_data, left_on=['First Name B', 'Last Name B'], right_on=['First Name', 'Last Name'], how='left', suffixes=('_A', '_B'))

# %% Function to generate HTML table for a given day
def generate_html_table(data, day, color_mode="background"):
    html_table = '<table border="1" style="border-collapse: collapse; width: 100%;">\n'
    html_table += '  <tr>\n    <th style="width: 20%;">Time</th>\n    <th style="width: 40%;">Track A</th>\n    <th style="width: 40%;">Track B</th>\n  </tr>\n'
    
    day_data = data[data['Date'] == day]
    
    for _, row in day_data.iterrows():
        if row.isnull().all() or "Room 1" in row.values or "Room 2" in row.values:
            continue
        
        time_slot = row["Time"]
        activity = row["Activity"]
        
        first_name_a = row["First Name A"] if pd.notna(row["First Name A"]) else ""
        last_name_a = row["Last Name A"] if pd.notna(row["Last Name A"]) else ""
        session_a = row["Session A"] if pd.notna(row["Session A"]) else ""
        title_a = row["Title_A"] if pd.notna(row["Title_A"]) else ""
        url_a = row["URL_A"] if pd.notna(row["URL_A"]) else ""
        
        first_name_b = row["First Name B"] if pd.notna(row["First Name B"]) else ""
        last_name_b = row["Last Name B"] if pd.notna(row["Last Name B"]) else ""
        session_b = row["Session B"] if pd.notna(row["Session B"]) else ""
        title_b = row["Title_B"] if pd.notna(row["Title_B"]) else ""
        url_b = row["URL_B"] if pd.notna(row["URL_B"]) else ""
        
        author_a = f'{first_name_a} {last_name_a}' if first_name_a and last_name_a else ""
        author_b = f'{first_name_b} {last_name_b}' if first_name_b and last_name_b else ""
        
        color_a = palette.get(session_a, "#FFFFFF")
        color_b = palette.get(session_b, "#FFFFFF")
        
        style_a = ' style="text-align: center;"'
        style_b = ' style="text-align: center;"'
        color_square_a = ''
        color_square_b = ''
        
        if color_mode in ["background", "both"]:
            style_a = f' style="background-color: {color_a}; text-align: center;"' if color_a else ' style="text-align: center;"'
            style_b = f' style="background-color: {color_b}; text-align: center;"' if color_b else ' style="text-align: center;"'
        
        if color_mode in ["square", "both"]:
            color_square_a = f'<span style="display:inline-block; width:10px; height:10px; background-color:{color_a}; margin-right:5px;"></span>' if color_a else ""
            color_square_b = f'<span style="display:inline-block; width:10px; height:10px; background-color:{color_b}; margin-right:5px;"></span>' if color_b else ""
        
        if pd.notna(activity):
            html_table += f'  <tr>\n    <td>{time_slot}</td>\n    <td colspan="2" style="text-align: center;">{activity}</td>\n  </tr>\n'
        else:
            html_table += f'  <tr>\n    <td>{time_slot}</td>\n    <td{style_a}>{color_square_a}{author_a}<br><a href="{url_a}">{title_a}</a></td>\n    <td{style_b}>{color_square_b}{author_b}<br><a href="{url_b}">{title_b}</a></td>\n  </tr>\n'
    
    html_table += '</table>\n'
    return html_table

# %% Generate HTML tables for each day
unique_days = merged_data['Date'].dropna().unique()
for day in unique_days:
    html_table = generate_html_table(merged_data, day, color_mode="square")
    # Save the HTML content to a file with utf-8 encoding
    filename = f"../website_exports/HTML_tables/talks_table_{day.replace(' ', '_').replace(':', '-')}.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_table)
    print(f"HTML table for {day} generated and saved to {filename}")
# %%
