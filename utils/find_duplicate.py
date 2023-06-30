
def find_duplicate(properties_data_df):
    '''function that receives a Data Frame as a parameter and cleans the information inside it.'''

    # remove rows with a NULL value in the "country" column:
    properties_data_df.dropna(subset=['country'], inplace = True)
    # remove rows with a NULL value in the address ('street', 'number', 'box') column:
    properties_data_df.dropna(subset=['street', 'number'], inplace = True, how = 'all')
    # dataset removing symbols in field number of address
    properties_data_df['number'] = properties_data_df['number'].replace({'-':'', '!': '', ',' :''}, regex=True)

    # duplicated elements based on postalCode,	street,	number
    duplicate = properties_data_df[properties_data_df.duplicated(['postalCode','street', 'number', 'price', 'bedroomCount'])]

    return duplicate