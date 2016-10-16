import pandas as pd

# Load the original csv
df = pd.read_csv('data/carto.csv')

# Group by name of borough
# The output is a list of tuples with ('name of borough', dataframe of that borough)
grouped = list(df.groupby('location_name'))


for x in grouped:
    # Get the name of the borough
    name_of_borough = x[0]

    # Sort the dataframe by date
    sorted_df = x[1].sort(['date'])

    # Create a csv for each dataframe
    sorted_df.to_csv('data/output/' + name_of_borough + '.tsv', index=None, sep='\t')
