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
data = pd.read_csv(filename)

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
        first_name_a = row["First Name - Track A"] if pd.notna(row["First Name - Track A"]) else ""
        last_name_a = row["Last Name - Track A"] if pd.notna(row["Last Name - Track A"]) else ""
        session_a = row["Session - Track A"] if pd.notna(row["Session - Track A"]) else ""
        first_name_b = row["First Name - Track B"] if pd.notna(row["First Name - Track B"]) else ""
        last_name_b = row["Last Name - Track B"] if pd.notna(row["Last Name - Track B"]) else ""
        session_b = row["Session - Track B"] if pd.notna(row["Session - Track B"]) else ""
        
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
            html_table += f'  <tr>\n    <td>{time_slot}</td>\n    <td{style_a}>{color_square_a}{author_a}<br>{session_a}</td>\n    <td{style_b}>{color_square_b}{author_b}<br>{session_b}</td>\n  </tr>\n'
    
    html_table += '</table>\n'
    return html_table

# %% Generate HTML tables for each day
unique_days = data['Date'].dropna().unique()
for day in unique_days:
    html_table = generate_html_table(data, day, color_mode="square")
    # Save the HTML content to a file with utf-8 encoding
    filename = f"../website_exports/HTML_tables/talks_table_{day.replace(' ', '_').replace(':', '-')}.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_table)
    print(f"HTML table for {day} generated and saved to {filename}")