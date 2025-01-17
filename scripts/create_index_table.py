### This script generates an HTML table to paste in Wordpress
### with custom CSS applied to specific cells (i.e. specific cells)
### and with custom links to abstracts on the website

# %%
import pandas as pd

# Define the schedule data with two tracks
schedule = [
    ["5 February 2025", "09:00-10:00", "Registration and welcome coffee break", "Registration and welcome coffee break"],
    ["5 February 2025", "10:00-11:00", "Opening Ceremony", "Opening Ceremony"],
    ["5 February 2025", "11:00-12:30", "Slot 1 - Track A", "Slot 1 - Track B"],
    ["5 February 2025", "12:30-14:00", "Lunch", "Lunch"],
    ["5 February 2025", "14:00-15:30", "Slot 2 - Track A", "Slot 2 - Track B"],
    ["5 February 2025", "15:30-16:30", "Coffee break + poster", "Coffee break + poster"],
    ["5 February 2025", "16:30-18:00", "Slot 3 - Track A", "Slot 3 - Track B"],
    ["6 February 2025", "09:00-10:15", "Slot 4 - Track A", "Slot 4 - Track B"],
    ["6 February 2025", "10:15-11:15", "Coffee break + poster", "Coffee break + poster"],
    ["6 February 2025", "11:15-12:30", "Slot 5 - Track A", "Slot 5 - Track B"],
    ["6 February 2025", "12:30-14:00", "Lunch", "Lunch"],
    ["6 February 2025", "14:00-15:30", "Slot 6 - Track A", "Slot 6 - Track B"],
    ["6 February 2025", "15:30-16:30", "Coffee break + poster", "Coffee break + poster"],
    ["6 February 2025", "16:30-18:00", "Slot 8 - Track A", "Slot 8 - Track B"],
    ["6 February 2025", "19:30-23:00", "Social dinner", "Social dinner"],
    ["7 February 2025", "09:00-10:15", "Slot 9 - Track A", "Slot 9 - Track B"],
    ["7 February 2025", "10:15-11:15", "Coffee break + poster", "Coffee break + poster"],
    ["7 February 2025", "11:15-12:30", "Slot 10 - Track A", "Slot 10 - Track B"],
    ["7 February 2025", "12:30-14:00", "Lunch", "Lunch"],
    ["7 February 2025", "14:00-17:00", "Workshops and Closing Ceremony", "Workshops and Closing Ceremony"]
]

# Define the background colors for specific cells
background_colors = {
    "Registration and welcome coffee break": "#FFFFFF",
    "Opening Ceremony": "#FFFFFF",
    "Lunch": "#FFFFFF",
    "Coffee break + poster": "#FFFFFF",
    "Social dinner": "#FFFFFF",
    "Slot 1 - Track A": "#FFCCCC",
    "Slot 1 - Track B": "#FFCCCC",
    "Slot 2 - Track A": "#CCFFCC",
    "Slot 2 - Track B": "#CCFFCC",
    "Slot 3 - Track A": "#CCCCFF",
    "Slot 3 - Track B": "#CCCCFF",
    "Slot 4 - Track A": "#FFFFCC",
    "Slot 4 - Track B": "#FFFFCC",
    "Slot 5 - Track A": "#FFCCFF",
    "Slot 5 - Track B": "#FFCCFF",
    "Slot 6 - Track A": "#CCFFFF",
    "Slot 6 - Track B": "#CCFFFF",
    "Slot 8 - Track A": "#FFCC99",
    "Slot 8 - Track B": "#FFCC99",
    "Slot 9 - Track A": "#99CCFF",
    "Slot 9 - Track B": "#99CCFF",
    "Slot 10 - Track A": "#FF99CC",
    "Slot 10 - Track B": "#FF99CC",
    "Workshops and Closing Ceremony": "#FFFFFF"
}

# Function to calculate the number of talks in a slot
def calculate_talks(start_time, end_time):
    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))
    start_total_minutes = start_hour * 60 + start_minute
    end_total_minutes = end_hour * 60 + end_minute
    duration_minutes = end_total_minutes - start_total_minutes
    return duration_minutes // 15

# Create a DataFrame from the schedule data
df = pd.DataFrame(schedule, columns=["Date", "Time", "Track A", "Track B"])

# Function to generate HTML table for a given day
def generate_html_table(df, day):
    html_table = '<table border="1" style="border-collapse: collapse; width: 100%;">\n'
    html_table += '  <tr>\n    <th>Date</th>\n    <th>Time</th>\n    <th>Track A</th>\n    <th>Track B</th>\n  </tr>\n'
    
    for _, row in df.iterrows():
        date, time, track_a, track_b = row["Date"], row["Time"], row["Track A"], row["Track B"]
        background_color_a = background_colors.get(track_a, "#FFFFFF")
        background_color_b = background_colors.get(track_b, "#FFFFFF")
        style_a = f' style="background-color: {background_color_a}; text-align: center;"' if background_color_a else ' style="text-align: center;"'
        style_b = f' style="background-color: {background_color_b}; text-align: center;"' if background_color_b else ' style="text-align: center;"'
        
        if date == day or date == "":
            if "Slot" in track_a and "Slot" in track_b:
                start_time, end_time = time.split("-")
                num_talks = calculate_talks(start_time, end_time)
                for i in range(num_talks):
                    talk_time = f"{start_time}-{end_time}" if i == 0 else ""
                    html_table += f'  <tr>\n    <td>{day}</td>\n    <td>{talk_time}</td>\n    <td{style_a}>Talk {i+1}</td>\n    <td{style_b}>Talk {i+1}</td>\n  </tr>\n'
            elif track_a == track_b:
                html_table += f'  <tr>\n    <td>{day}</td>\n    <td>{time}</td>\n    <td colspan="2"{style_a}>{track_a}</td>\n  </tr>\n'
            else:
                html_table += f'  <tr>\n    <td>{day}</td>\n    <td>{time}</td>\n    <td{style_a}>{track_a}</td>\n    <td{style_b}>{track_b}</td>\n  </tr>\n'
    
    html_table += '</table>\n'
    return html_table

# Generate HTML tables for each day
days = ["5 February 2025", "6 February 2025", "7 February 2025"]
html_tables = [generate_html_table(df, day) for day in days]

# Combine the tables into a single HTML file
html_content = "<html>\n<head>\n<title>Conference Schedule</title>\n</head>\n<body>\n"
for table in html_tables:
    html_content += table + "<br>\n"
html_content += "</body>\n</html>"

# Save the HTML content to a file
with open("schedule_table.html", "w") as file:
    file.write(html_content)

print("HTML tables generated and saved to schedule_table.html")