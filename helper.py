import numpy as np

def medal_tally(frame):

    medal_tally= frame.drop_duplicates(subset=['Team','NOC','Games','Year','Sport','Event','Medal'])

    medal_tally=medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values(by='Gold',ascending=False).reset_index()

    medal_tally['total']= medal_tally['Gold']+ medal_tally['Silver']+ medal_tally['Bronze']
    
    medal_tally['Gold']= medal_tally['Gold'].astype('int')

    return medal_tally

def country_year_list_func(df1):
    years= df1['Year'].unique().tolist()

    years.sort()

    years.insert(0,'Overall')

    country= np.unique(df1['region'].dropna().values).tolist()

    country.sort()

    country.insert(0,'Overall')

    return years, country

def fetch_medal_tally(df1, year, country):
    medal_df= df1.drop_duplicates(subset=['Team','NOC','Games','Year','Sport','Event','Medal'])
    flag=0
    if year == 'Overall' and country =='Overall':
        temp_df= medal_df
        
    if year == 'Overall' and country !='Overall':
        temp_df= medal_df[medal_df['region']== country]
        flag=1
        
    if year != 'Overall' and country =='Overall':
        temp_df= medal_df[medal_df['Year']== year]

    if year != 'Overall' and country !='Overall':
        temp_df= medal_df[(medal_df['Year']== year) & (medal_df['region']==country)]
    
    if flag ==1:
        x= temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values(by='Year').reset_index()

    
    
    else:
        x= temp_df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values(by='Gold',ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']
    
    return x

def count_of_nations(df1):
    nations_over_time = df1.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values(by='Year')
    nations_over_time.rename(columns={'Year':  'Olympic Edition', 'count': 'Countries participated'}, inplace=True)
    return nations_over_time


def Events_per_edition(df1):
    Events_per_edition = df1.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values(by='Year')
    Events_per_edition.rename(columns={'Year':  'Olympic Edition', 'count': 'Number of Events'}, inplace=True)
    return Events_per_edition

def Athletes_per_edition(df1):
    Athletes_per_edition = df1.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values(by='Year')
    Athletes_per_edition.rename(columns={'Year':  'Olympic Edition', 'count': 'Number of Athletes'}, inplace=True)
    return Athletes_per_edition


def most_successful_by_sport(df,sport):
    temp_df= df.dropna(subset='Medal')

    if sport!= 'Overall':
        temp_df= temp_df[temp_df['Sport']==sport]
        
    x= temp_df['Name'].value_counts().reset_index()
    x.rename(columns={'count':'Total Medals'}, inplace=True)
    x= x.merge(temp_df, on ='Name', how= 'inner')
    x= x[['Name','region','Sport','Total Medals']]
    x=x.drop_duplicates().head(20)
    return x




def country_medal_yearly(df1,country):
    k= df1.dropna(subset='Medal')
    k= k.drop_duplicates(subset=['Team','NOC','Games','Year','Sport','Event','Medal'])
    k= k[k['region']==country]
    final_k= k.groupby('Year')['Medal'].count().reset_index()

    return final_k

def sport_list(df1):
    sport= df1['Sport'].unique().tolist()

    sport.sort()

    sport.insert(0,'Overall')

    return sport

def country_year(df1):


    country= np.unique(df1['region'].dropna().values).tolist()

    country.sort()


    return  country

def most_successful_by_region(df,region):
    temp_df= df.dropna(subset='Medal')
    temp_df= temp_df[temp_df['region']==region]
    x= temp_df['Name'].value_counts().reset_index()
    x.rename(columns={'count':'Total Medals'}, inplace=True)
    x= x.merge(temp_df, on ='Name', how= 'inner')
    x= x[['Name','Sport','Total Medals']]
    x=x.drop_duplicates().head(20)
    return x

def weight_vs_height(df, sport):
    athlete_df= df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No medal', inplace=True)
    if sport != 'Overall':
       athlete_df_wt_ht= athlete_df[athlete_df['Sport']== sport]

       return athlete_df_wt_ht
    
    return athlete_df



