import pandas as pd

df = pd.read_csv('debates.csv')
df1 = pd.read_csv('names.csv')
df = df.merge(df1, left_on='debate_politician_url', right_on='url', how='outer')
df.to_csv('merged.csv')
