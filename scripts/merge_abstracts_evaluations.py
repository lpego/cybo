import pandas as pd
import re
import os

### Provide file name here
abstracts = pd.read_csv("..\\website_exports\\abstracts_redux_parsed.csv")
evaluations = pd.read_csv("..\\website_exports\\evf-entry-export-abstract-evaluation-2024-12-11-9622391a024e2387a88157a78094f283.csv")
evaluations = evaluations.drop(["Date Created", "User Device", "User IP Address"], axis=1)

### Merge by URL
merged = abstracts.merge(evaluations, left_on="URL", right_on="Link to the abstract", how="left")

### write out to file
merged.to_csv("..\website_exports\merged_abstracts_evaluations.csv")
