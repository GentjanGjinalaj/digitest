import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

# File names for your main company and competitors
main_company_file = 'C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\test1.csv'
competitor_files = ['DigiScore\\DataML\\Competitors\\seoCompetitor_1.csv', 'DigiScore\\DataML\\Competitors\\seoCompetitor_2.csv', 'DigiScore\\DataML\\Competitors\\seoCompetitor_3.csv', 'DigiScore\\DataML\\Competitors\\seoCompetitor_4.csv', 'DigiScore\\DataML\\Competitors\\seoCompetitor_5.csv']

# Define a function to get a specific data value
def get_data_value(df, column, data_type):
    value = df[df[column] == data_type]['Website Data'].values[0] if column == 'Website Data Type' else df[df[column] == data_type]['SemRush API Data'].values[0]
    return value

# Function to filter out unwanted rows
def filter_rows(df, unwanted_values):
    for column in df.columns:
        df = df[~df[column].isin(unwanted_values)]
    return df

# Load the main company data
main_df = pd.read_csv(main_company_file)
unwanted_values = ['Website Panel', 'Competitors Panel', 'Marketing Channel Distribution Panel', 'Keywords Panel', np.nan]
main_df = filter_rows(main_df, unwanted_values)
main_df['Company'] = 'Main Company'

# Load competitor data
competitor_dfs = []
unwanted_values.extend(['First Competitor', 'Second Competitor', 'Third Competitor', 'Fourth Competitor', 'Fifth Competitor'])
for file in competitor_files:
    df = pd.read_csv(file)
    df = filter_rows(df, unwanted_values)
    df['Company'] = 'Competitor ' + file.split('_')[-1].split('.')[0]  # Get the competitor number from file name
    competitor_dfs.append(df)

# Combine all data
all_dfs = [main_df] + competitor_dfs
combined_df = pd.concat(all_dfs, ignore_index=True)

# Get all unique data types
website_data_types = combined_df['Website Data Type'].unique()
semrush_data_types = combined_df['SemRush API Data Type'].unique()

# Iterate over each company and each data type, printing the value for each
for company in combined_df['Company'].unique():
    company_df = combined_df[combined_df['Company'] == company]
    print(f'{company}:')
    for data_type in website_data_types:
        # Use a try-except block to handle the cases where a certain data_type may not exist for the current company
        try:
            data_value = get_data_value(company_df, 'Website Data Type', data_type)
            print(f'Website {data_type}: {data_value}')
        except IndexError:  # This happens if the data_type does not exist in company_df
            print(f'Website {data_type}: N/A', np.nan)

    for data_type in semrush_data_types:
        try:
            data_value = get_data_value(company_df, 'SemRush API Data Type', data_type)
            print(f'SemRush {data_type}: {data_value}')
        except IndexError:  # This happens if the data_type does not exist in company_df
            print(f'SemRush {data_type}: N/A', np.nan)

    print('----------------------------------')

combined_df.replace('N/A', np.nan, inplace=True)
combined_df.to_csv('Actual\\testsss\\DataNormalRating\\combined_df.csv')

df=combined_df
print(df.columns)

# Assuming df is your DataFrame

# Convert percentage strings to floats
percentage_data_types = ['Website Bounce Rate', 'Website Direct', 'Website Paid Search',
                         'Website Organic Keywords Percentage', 'Website Paid Keywords Percentage',
                         'Website Referrals', 'Website Organic Search', 'Website Mail', 'Website Display']

for data_type in percentage_data_types:
    mask = df['Website Data Type'] == data_type
    df.loc[mask, 'Website Data'] = df.loc[mask, 'Website Data'].str.rstrip('%').astype('float') / 100.0


# Convert 'Website Average Visit Duration' to seconds or minutes
mask = df['Website Data Type'] == 'Website Average Visit Duration'
df.loc[mask, 'Website Data'] = df.loc[mask, 'Website Data'].apply(lambda x: pd.to_timedelta(x).total_seconds())


# After this, you should be able to convert the 'Website Data' column to float
def is_convertible(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False

mask = df['Website Data'].apply(is_convertible)
df = df[mask]


# Impute missing data with a constant value (0 in this case)
df.fillna(0, inplace=True)

# Now handle the non-numeric columns (exclude them for this example)
df['Website Data'] = df['Website Data'].astype(float)
numeric_columns = ['Website Data']

# Use MinMaxScaler to scale the numeric columns
#scaler = MinMaxScaler()
#df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
df.to_csv('Actual\\testsss\\DataNormalRating\\normal.csv')
print(df)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #print(df)
