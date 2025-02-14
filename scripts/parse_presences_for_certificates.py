# %% 
import pandas as pd
from glob import glob
from latest_file import find_most_recent_file

# %% Read in manually checked presences
presences = pd.read_csv('..\website_exports\presenti_CYBO2025_12Feb.csv', sep=';')

# %% Clean up and rename columns
# presences.head()
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
evaluations = pd.read_csv(filename, skipinitialspace=True)
evaluations = evaluations.rename(columns=lambda x: x.strip())
evaluations = evaluations.map(lambda x: x.strip() if isinstance(x, str) else x)
evaluations = evaluations.drop(["Date Created", "User Device", "User IP Address"], axis=1)

# %% Read in shortened institutions dictionary
affiliations_contributes = pd.read_csv('..\\website_exports\\unique_institutions.csv', index_col=False)
affiliations_att_only = pd.read_csv("..\website_exports\cybo-2025-registration,-attendance-only_institutionsFILLED.csv", skipinitialspace=True)
affiliations_att_only = affiliations_att_only.drop(["User ID", "Gender", "Country"], axis=1)

# %% Merge abstracts and evaluations by URL
merged = abstracts.merge(evaluations, left_on="URL", right_on="Link to the abstract", how="left")
merged = merged[["First Name", "Last Name", "Email address", "Contributing author's institution", "Career stage", "Title", "Link to the abstract", "Reccommended type of contribution", "Reccommended session"]]

# %% Merge presences by name, surname and email
presences_merged = presences.merge(merged, on=["First Name", "Last Name", "Email address", "Career stage"], how="left")
presences_merged["Name"] = presences_merged["First Name"] + " " + presences_merged["Last Name"]

# %% Merge with affiliations to add "Short Affiliation" and for those without contribution
presences_merged = presences_merged.merge(affiliations_contributes, left_on="Contributing author's institution", right_on="original", how="left")
presences_merged = presences_merged.merge(affiliations_att_only, on=["First Name", "Last Name"], how="left")

### some people still are without affiliation, nothing to do there...

# %% fix last problems with dataframe
presences_merged["Institution"].fillna(presences_merged["shortened"], inplace=True) # fill missing values in "shortened" with values from "Institution"
presences_merged.dropna(how='all', inplace=True) # remove rows that are completely empty

# %% write out to file for certificate generation
presences_merged.to_csv("..\website_exports\presences_for_certificates.csv", index=False)

# %%
