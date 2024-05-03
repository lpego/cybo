import pandas as pd
import re
import os

### Provide file name here
filename = "cybo-webinars-2024-registration-2024-05-02_17 50 33.csv"

data = pd.read_csv(filename, skipinitialspace=True)
data.columns = data.columns.str.strip()
# webinars = data.iloc[:,7].to_list()
# certificate = data.iloc[:,8]
        
speakers = ['Antonelli', 'Riva', 'Martinez-Suz', 'Yannelli', 'Temunovic', 'Willems']

for speaker in speakers:
    data[speaker] = data['What webinars are you interested in?'].apply(lambda x: 1 if re.search(speaker, x) else 0)
# print(data)

data.to_csv(os.path.splitext(filename)[0]+"_parsed.csv")

# print(data[data['Riva'] == 1][['User Email', 'Do you need an attendance certificate?']])
