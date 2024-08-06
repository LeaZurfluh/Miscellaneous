'''
Lea's python playground
'''

#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl 
#%%
file_path = '/Users/leazurfluh/Downloads/2023_bumble_marketing_spend_.xlsx'
folder_parth = '/Users/leazurfluh/Downloads/'
new_csv = '/Users/leazurfluh/Downloads/2023_bumble_marketing_spend_only2023.csv'
# %%
csv = pd.read_csv(new_csv)
# %%
df = pd.read_excel(file_path)
# %%
df['Year'] = pd.DatetimeIndex(df['Date']).year
df['Month'] = pd.DatetimeIndex(df['Date']).month
# %%
df.head()
# %%
df_not2023 = df[df['Year'] != 2023]
df_2023 = df[df['Year'] == 2023]
# %%
len(df_not2023)
# %%
df_2023.to_excel(folder_parth + '2023_bumble_marketing_spend_only2023.xlsx')
df_2023.to_csv(folder_parth + '2023_bumble_marketing_spend_only2023.csv')
# %%
df_2023.Country.unique()
# %%
df['Date'] = df['Date'].astype('datetime64[ns]')
df[['Year']].groupby([df['Year'], df['Month']]).count().plot(kind='bar')
df[['Month']].groupby( df['Month']).count().plot(kind='bar')
# %%
df.groupby(df.Year).count()
# %%
df_testing = df[(df['Platform'] == 'Uber') & (df['Quarter'] == 'Q3')]
df_testing[['Year']].groupby([df_testing['Year'], df_testing['Month']]).count().plot(kind='bar')

# %%
len(csv)
# %%
df.iloc[581664]
# %%
