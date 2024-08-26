import pandas as pd


def preprocess(df1, df2):

    df1= df1[df1['Season']=='Summer']

    df1= df1.merge(df2, on= 'NOC',how='left')

    df1.drop_duplicates(inplace=True)

    df1= pd.concat([df1, pd.get_dummies(df1['Medal'])], axis =1)

    df1[['Bronze','Gold','Silver']]= df1[['Bronze','Gold','Silver']].astype(int)

    return df1
