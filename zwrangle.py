

def get_url(db):
    '''
    This function takes in a database name and returns a url (using the specified 
    database name as well as host, user, and password from env.py) for use in the 
    pandas.read_sql() function.
    '''
    from env import host, user, password
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def cols_missing_rows(df):
    df = pd.DataFrame(data={'num_rows_missing':df.isnull().sum(), 
              'pct_rows_missing':df.isnull().sum()/len(df)}, index=df.columns)
    return df

def rows_missing_cols(df):
    df = pd.DataFrame({'num_cols_missing':df.isnull().sum(axis=1).value_counts().index,
                       'pct_cols_missing':df.isnull().sum(axis=1).value_counts().index/len(df.columns),
                       'num_rows':df.isnull().sum(axis=1).value_counts()}).reset_index(drop=True)
    return df

def only_single_units(zillow):
    '''
    This function takes in the zillow dataframe and removes any properties not believed
    to be single-unit properties. It returns zillow without those properties.
    '''
    zillow_filt = zillow[zillow.propertylandusetypeid.isin([261, 262, 263, 264, 266, 268, 273, 276, 279])]
    zillow_filt = zillow_filt[(zillow.bathroomcnt > 0) & (zillow.calculatedfinishedsquarefeet > 300)]
    zillow_filt = zillow_filt[(zillow_filt.unitcnt == 1) | (zillow_filt.unitcnt.isnull())]
    return zillow_filt

def handle_missing_values(df, prop_req_col, prop_req_row):
    '''
    This function takes in a dataframe, a max proportion of null values for each 
    column, and a max proportion of null values for each row. It returns the 
    dataframe less any rows or columns with more than the max proportion of nulls.
    '''
    df = df.dropna(axis=1, thresh=prop_req_col*len(df))
    df = df.dropna(thresh=prop_req_row*len(df.columns))
    return df