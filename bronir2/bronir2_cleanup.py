import pandas as pd

all_df = pd.read_csv('bronir2-all.txt', sep=',', na_values = ['m'])
print(all_df.info())

print(all_df.describe())

# Delete column 'Temp'
all_df = all_df.drop(columns=['Temp'])

# Delete the last 200 columns
all_df = all_df.iloc[:, :-200]

# Replace '.0' with '' in column names
all_df.columns = all_df.columns.str.replace('.0', '', regex=False)

# Find all unique values in the 'Catalyst' column
#unique_catalysts = all_df['Catalyst'].unique()
#print("Unique catalysts:", unique_catalysts)
cat_replacement = {
    0: 'Cat A',
    1: 'Cat B',
    2: 'Cat C',
    3: 'Cat D',
}
# Replace numerical values in 'Catalyst' with car names
all_df['Catalyst'] = all_df['Catalyst'].replace(cat_replacement)


#unique_products = all_df['Product'].unique()
#print("Unique products:", unique_products)
product_replacement = {
    0: 'Prod 1',
    1: 'Prod 2',
    2: 'Prod 3',
    3: 'Prod 4',
    4: 'Prod 5',
    5: 'Prod 6',
    6: 'Prod 7',
    7: 'Prod 8',
    8: 'Prod 9',
    9: 'Prod 10',
    10: 'Prod 11',
    11: 'Prod 12',
    12: 'Prod 13',
    13: 'Prod 14',
    14: 'Prod 15'
}
# Replace numerical values in 'Product' with product names
all_df['Product'] = all_df['Product'].replace(product_replacement)

print(all_df.head(5))
print(all_df.head(-5))

all_df.to_csv('bronir2.csv')