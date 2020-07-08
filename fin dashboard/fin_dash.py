import pandas as pd
import json

# with open('fin dashboard/data.json') as f:
#     data = json.load(f)
# df = pd.DataFrame(data)

pd.read_json('fin dashboard/data.json', orient='table')

print(df.head())