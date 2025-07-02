### This script uses a manually curated list of attendees to the conference
### and merges it with abstract and evaluation data as well as curated institutions names
### to create the base data for the book of abstracts data generation. 

# %% 
import csv
import pandas as pd
from glob import glob
from latest_file import find_most_recent_file
import re

# %% Read in manually checked presences
presences = pd.read_csv('..\website_exports\presenti_CYBO2025_12Feb.csv', sep=';')

# %% Clean up and rename columns
presences = presences.drop(["Unnamed: 5", "Unnamed: 6"], axis=1)
presences.columns = ["First Name", "Last Name", "Email address", "Career stage", "Contribution"]
presences["First Name"] = presences["First Name"].str.title()
presences["Last Name"] = presences["Last Name"].str.title()

# %% Read in data for title of contribution
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[_redux].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
abstracts = pd.read_csv(filename, skipinitialspace=True)
abstracts = abstracts.rename(columns=lambda x: x.strip())
abstracts = abstracts.map(lambda x: x.strip() if isinstance(x, str) else x)
abstracts = abstracts.drop("Unnamed: 0", axis=1)
abstracts["First Name"] = abstracts["First Name"].str.title()
abstracts["Last Name"] = abstracts["Last Name"].str.title()

# %% Read in most recent version of abstracts evaluations (i.e. Dashboard > Everest Forms > Entries > Export CSV)
filelist = glob("..\website_exports\evf-entry-export-abstract-evaluation-*.csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
# stripping rogue newlines from the contents
with open(filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
# Convert the rows back to a pandas DataFrame
evaluations = pd.DataFrame(rows)
# Ensure all fields are stripped of rogue newlines
evaluations = evaluations.applymap(lambda x: str(x).replace('\n', ' ') if isinstance(x, str) else x)
evaluations = evaluations.rename(columns=lambda x: x.strip())
# Rename column for consistency
if "Link to the abstract" in evaluations.columns:
    evaluations = evaluations.rename(columns={"Link to the abstract": "Link_to_abstract"})
evaluations = evaluations.drop(["Date Created", "User Device", "User IP Address"], axis=1)

# %% Read in shortened institutions dictionary
affiliations_contributes = pd.read_csv('..\\website_exports\\unique_institutions.csv', index_col=False)
affiliations_att_only = pd.read_csv("..\website_exports\cybo-2025-registration,-attendance-only_institutionsFILLED.csv", skipinitialspace=True)
affiliations_att_only = affiliations_att_only.drop(["User ID", "Gender", "Country"], axis=1)

# %% Read in final assignment to sessions and contribution type
final_assignments = pd.read_csv('..\\website_exports\\Programme_2025 - Detailed_programme.csv', index_col=False)
final_assignments = final_assignments[["First Name", "Last Name", "Email address", "Final contribution", "Final session"]]
final_assignments.dropna(how='all', inplace=True) # remove rows that are completely empty

# %% Merge abstracts and evaluations by URL
merged = abstracts.merge(evaluations, left_on="URL", right_on="Link_to_abstract", how="left")
# merged = merged[["First Name", "Last Name", "Email address", "Contributing author's institution", "Career stage", "Title", "Link_to_abstract", "Reccommended type of contribution", "Reccommended session"]]

# %% Merge presences by name, surname and email
presences_merged = presences.merge(merged, on=["First Name", "Last Name", "Email address"], how="left")
presences_merged["Name"] = presences_merged["First Name"] + " " + presences_merged["Last Name"]

# %% Merge with affiliations to add "Short Affiliation" and for those without contribution
presences_merged = presences_merged.merge(affiliations_contributes, left_on="Contributing author's institution", right_on="original", how="left")
presences_merged = presences_merged.merge(affiliations_att_only, on=["First Name", "Last Name"], how="left")
### some people still are without affiliation, nothing to do there...
presences_merged.to_csv("..\website_exports\\test.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

# %% Merge with final sessions and contribution type
presences_merged = presences_merged.merge(final_assignments, on=["First Name", "Last Name"], how="left")

# %% Fill "Final contribution" and "Final session" for Poster contributions (posters were never switched to other sessions)
poster_condition = presences_merged["What type of contribution would you prefer to submit?"] == "Poster"
presences_merged.loc[poster_condition, "Final contribution"] = presences_merged.loc[poster_condition, "What type of contribution would you prefer to submit?"]
presences_merged.loc[poster_condition, "Final session"] = presences_merged.loc[poster_condition, "Preferred session"]

# %% fix last problems with dataframe
presences_merged["Institution"].fillna(presences_merged["shortened"], inplace=True) # fill missing values in "shortened" with values from "Institution"
presences_merged.dropna(how='all', inplace=True) # remove rows that are completely empty

# %% write out to file for book of abstracts generation
presences_merged.to_csv("..\website_exports\presences_for_book_of_abstracts.csv", encoding="utf-8", index=False, quoting=csv.QUOTE_ALL)

# %% reduce to only necessary columns
presences_merged_redux = presences_merged[["Name", "Email address_x", "Link_to_abstract", 
                                           "Final contribution", "Final session", 
                                           "Title", "Abstract", 
                                           "Contributing author's institution", 
                                           "Author 2", "Author 3", "Author 4", "Author 5", "Author 6", "Author 7", "Author 8", "Author 9", "Additional authors", 
                                           "Author 2 affiliation", "Author 3 affiliation", "Author 4 affiliation", "Author 5 affiliation", "Author 6 affiliation", "Author 7 affiliation", "Author 8 affiliation", "Author 9 affiliation", "Additional authors affiliations"
                                           ]]
presences_merged_redux.dropna(subset=["Abstract"], inplace=True)  # Remove rows with no data for Abstract

# Extract numeric index from "Final session" and sort
presences_merged_redux["Final session index"] = presences_merged_redux["Final session"].str.extract(r'(\d+)').astype(float)
presences_merged_redux.sort_values(by=["Final session index", "Name"], inplace=True)
presences_merged_redux.drop(columns=["Final session index"], inplace=True)  # Remove helper column

presences_merged_redux.to_csv("..\website_exports\presences_for_book_of_abstracts_redux.csv", encoding="utf-8", index=False, quoting=csv.QUOTE_ALL)

# %% From ChatGPT
presences_merged_redux_dict = presences_merged_redux

# Base author and affiliation columns
author_cols = ['Name', 'Author 2', 'Author 3', 'Author 4', 'Author 5',
               'Author 6', 'Author 7', 'Author 8', 'Author 9']
affil_cols = ['Contributing author\'s institution', 'Author 2 affiliation', 'Author 3 affiliation',
              'Author 4 affiliation', 'Author 5 affiliation', 'Author 6 affiliation',
              'Author 7 affiliation', 'Author 8 affiliation', 'Author 9 affiliation']

def build_author_dict(row):
    # 1. Get named authors and affiliations
    authors = [row[col] for col in author_cols if pd.notna(row[col])]
    affiliations = [row[col] for col in affil_cols if pd.notna(row[col])]
    
    # 2. Handle additional authors
    add_authors_str = row.get('Additional authors', '')
    add_affils_str = row.get('Additional authors affiliations', '')
    
    # Split by semicolon and strip whitespace
    if pd.notna(add_authors_str):
        add_authors = [a.strip() for a in add_authors_str.split(';') if a.strip()]
    else:
        add_authors = []
    
    if pd.notna(add_affils_str):
        add_affils = [a.strip() for a in add_affils_str.split(';') if a.strip()]
    else:
        add_affils = []
    
    # Ensure they are paired
    if len(add_authors) != len(add_affils):
        print(f"Warning: Mismatched additional authors/affiliations in row {row.name}")
    
    # Combine core and additional authors
    all_authors = authors + add_authors
    all_affils = affiliations + add_affils
    
    # Pair authors with affiliations
    paired = list(zip(all_authors, all_affils))
    
    # Assign superscripts
    affil_to_sup = {}
    current_sup = 1
    author_list = []
    
    for author, affil in paired:
        if affil not in affil_to_sup:
            affil_to_sup[affil] = current_sup
            current_sup += 1
        author_list.append({
            "name": author,
            "affiliation": affil,
            "superscript": affil_to_sup[affil]
        })
    
    return author_list

# Apply the function
presences_merged_redux_dict["author_affil_map"] = presences_merged_redux_dict.apply(build_author_dict, axis=1)

# %% Extract authors and their assigned superscript into a separate column
def format_authors_latex(author_affil_map):
    return ", ".join(
        f"{entry['name']}\\textsuperscript{{{entry['superscript']}}}" for entry in author_affil_map
    )

# apply to the dataframe
presences_merged_redux_dict["latex_authors_string"] = presences_merged_redux_dict["author_affil_map"].apply(format_authors_latex)

# %% Extract affiliations into a separate column
def extract_affil_list(author_affil_map):
    # Use a dict to preserve insertion order (Python 3.7+)
    affil_to_sup = {}
    for entry in author_affil_map:
        affil = entry["affiliation"]
        sup = entry["superscript"]
        if affil not in affil_to_sup:
            affil_to_sup[affil] = sup
    # Format for LaTeX
    formatted = [f"\\textsuperscript{{{sup}}} {affil}" for affil, sup in affil_to_sup.items()]
    return formatted

# format the string for LaTeX with newlines escaped
def format_affiliations_latex_multiline(author_affil_map):
    affil_to_sup = {}
    for entry in author_affil_map:
        affil = entry["affiliation"]
        sup = entry["superscript"]
        if affil not in affil_to_sup:
            affil_to_sup[affil] = sup
    # Use double backslashes, but escape them as `\\` in the CSV string
    lines = [f"\\textsuperscript{{{sup}}} {affil}" for affil, sup in affil_to_sup.items()]
    return "; ".join(lines)  # double backslash with space for LaTeX line break

presences_merged_redux_dict["latex_affiliations_multiline"] = presences_merged_redux_dict["author_affil_map"].apply(format_affiliations_latex_multiline)

# %% LaTeX special character escaping
def remove_nbsp(s):
    if not isinstance(s, str):
        return s
    # Replace non-breaking spaces with normal spaces
    s = s.replace('\u00a0', ' ')
    s = s.replace('\xa0', ' ')
    s = s.replace(chr(160), ' ')
    return s

# %% write out to another file
presences_merged_redux_dict.to_csv("..\website_exports\presences_for_book_of_abstracts_redux_dictionary.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

# Apply removing non-breaking spaces to all string fields in the DataFrame
presences_merged_redux_dict_no_nbsp = presences_merged_redux_dict.applymap(remove_nbsp)
presences_merged_redux_dict_no_nbsp.to_csv("..\website_exports\presences_for_book_of_abstracts_redux_dictionary_nbsp.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

def escape_latex(s):
    if not isinstance(s, str):
        return s
    # Order matters: escape backslash first
    s = s.replace('\\', r'\textbackslash{}')
    s = s.replace('&', r'\&')
    s = s.replace('%', r'\%')
    s = s.replace('$', r'\$')
    s = s.replace('#', r'\#')
    s = s.replace('_', r'\_')
    s = s.replace('{', r'\{')
    s = s.replace('}', r'\}')
    s = s.replace('~', r'\textasciitilde{}')
    s = s.replace('^', r'\textasciicircum{}')
    return s

# Apply escaping to all string fields in the DataFrame (directly from presences_merged_redux_dict, not from a previous escaped version)
presences_merged_redux_dict_escaped = presences_merged_redux_dict.applymap(escape_latex)

# Save to new CSV with _escaped suffix
presences_merged_redux_dict_escaped.to_csv(
    "..\\website_exports\\presences_for_book_of_abstracts_redux_dictionary_escaped.csv",
    index=False, encoding="utf-8", quoting=csv.QUOTE_ALL
)

# %%
