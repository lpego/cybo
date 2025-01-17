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
    ["6 February 2025", "16:30-18:00", "Slot 7 - Track A", "Slot 7 - Track B"],
    ["6 February 2025", "19:30-23:00", "Social dinner", "Social dinner"],
    ["7 February 2025", "09:00-10:15", "Slot 8 - Track A", "Slot 8 - Track B"],
    ["7 February 2025", "10:15-11:15", "Coffee break + poster", "Coffee break + poster"],
    ["7 February 2025", "11:15-12:30", "Slot 9 - Track A", "Slot 9 - Track B"],
    ["7 February 2025", "12:30-14:00", "Lunch", "Lunch"],
    ["7 February 2025", "14:00-17:00", "Workshops and Closing Ceremony", "Workshops and Closing Ceremony"]
]

# Define a palette of 6 muted colors for the sessions
palette = {
    "Systematics": "#B0C4DE",
    "Ecology": "#98FB98",
    "Biodiversity": "#FFDAB9",
    "Physiology": "#E6E6FA",
    "Genetics": "#FFB6C1",
    "Society": "#FFFACD"
}

# Assign sessions to slots
session_assignments = {
    "5 February 2025": {
        "Slot 1 - Track A": "Biodiversity",
        "Slot 2 - Track A": "Biodiversity",
        "Slot 3 - Track A": "Biodiversity",
        "Slot 1 - Track B": "Physiology",
        "Slot 2 - Track B": "Physiology",
        "Slot 3 - Track B": "Physiology"
    },
    "6 February 2025": {
        "Slot 4 - Track A": "Biodiversity",
        "Slot 5 - Track A": "Ecology",
        "Slot 6 - Track A": "Ecology",
        "Slot 7 - Track A": "Ecology",
        "Slot 4 - Track B": "Systematics",
        "Slot 5 - Track B": "Systematics",
        "Slot 6 - Track B": "Systematics",
        "Slot 7 - Track B": "Genetics"
    },
    "7 February 2025": {
        "Slot 8 - Track A": "Ecology",
        "Slot 9 - Track A": "Ecology",
        "Slot 8 - Track B": "Society",
        "Slot 9 - Track B": "Society"
    }
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
    html_table += '  <tr>\n    <th style="width: 20%;">Time</th>\n    <th style="width: 40%;">Track A</th>\n    <th style="width: 40%;">Track B</th>\n  </tr>\n'
    
    for _, row in df.iterrows():
        date, time, track_a, track_b = row["Date"], row["Time"], row["Track A"], row["Track B"]
        session_a = session_assignments.get(date, {}).get(track_a, track_a)
        session_b = session_assignments.get(date, {}).get(track_b, track_b)
        background_color_a = palette.get(session_a, "#FFFFFF")
        background_color_b = palette.get(session_b, "#FFFFFF")
        style_a = f' style="background-color: {background_color_a}; text-align: center;"' if background_color_a else ' style="text-align: center;"'
        style_b = f' style="background-color: {background_color_b}; text-align: center;"' if background_color_b else ' style="text-align: center;"'
        
        if date == day or date == "":
            if "Slot" in track_a and "Slot" in track_b:
                start_time, end_time = time.split("-")
                num_talks = calculate_talks(start_time, end_time)
                for i in range(num_talks):
                    talk_time = f"{start_time}-{end_time}" if i == 0 else ""
                    html_table += f'  <tr>\n    <td>{talk_time}</td>\n    <td{style_a}>Talk {i+1}</td>\n    <td{style_b}>Talk {i+1}</td>\n  </tr>\n'
            elif track_a == track_b:
                html_table += f'  <tr>\n    <td>{time}</td>\n    <td colspan="2"{style_a}>{track_a}</td>\n  </tr>\n'
            else:
                html_table += f'  <tr>\n    <td>{time}</td>\n    <td{style_a}>{track_a}</td>\n    <td{style_b}>{track_b}</td>\n  </tr>\n'
    
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