import pandas as pd
import numpy as np
import streamlit as st
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df1= pd.read_csv('athlete_events.csv')

df2= pd.read_csv('noc_regions.csv')

df1= preprocessor.preprocess(df1, df2)
st.sidebar.title('Olympic Analysis')

st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJAUDKt4QwzvRLWel0FNz_F0wsTtjw2v9ZbQ&s')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country= helper.country_year_list_func(df1)
    selected_year= st.sidebar.selectbox("Select Year", years)
    selected_country= st.sidebar.selectbox("Select Country", country)

    medal_tally= helper.fetch_medal_tally(df1,selected_year, selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    if selected_year!='Overall' and selected_country=='Overall':
        st.title(f'{selected_year}- Tally with all countries')
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(f'Analysis for all years - {selected_country}')
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(f'{selected_country} analysis - {selected_year}')
    st.table(medal_tally)


if user_menu=='Overall Analysis':
    editions= df1['Year'].unique().shape[0]-1
    cities = df1['City'].unique().shape[0]
    events= df1['Event'].unique().shape[0]
    sports= df1['Sport'].unique().shape[0]
    athletes= df1['Name'].unique().shape[0]
    nations= df1['region'].unique().shape[0]

    st.title('Top Statistics')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Cities")
        st.title(cities)

    with col3:
        st.header("Events")
        st.title(events)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.header("Sports")
        st.title(sports)

    with col5:
        st.header("Athletes")
        st.title(athletes)

    with col6:
        st.header("Nations")
        st.title(nations)

    nations_over_time= helper.count_of_nations(df1)
    Events_per_edition= helper.Events_per_edition(df1)
    Athletes_per_edition= helper.Athletes_per_edition(df1)


    fig= px.line(nations_over_time, x='Olympic Edition', y='Countries participated')
    st.title('Participating nations over the time')
    st.plotly_chart(fig)



    fig2= px.line(Events_per_edition, x='Olympic Edition', y='Number of Events')
    st.title('Events per olympics over the time')
    st.plotly_chart(fig2)

    fig3= px.line(Athletes_per_edition, x='Olympic Edition', y='Number of Athletes')
    st.title('Athletes per olympics over the time')
    st.plotly_chart(fig3)

    st.title('Number of events per each sport in every edition')
    fig4, ax= plt.subplots(figsize=(25,25))
    x= df1.drop_duplicates(subset=['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event',aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig4)

    st.title('Most Successful Athletes')
    sport = helper.sport_list(df1)
    selected_sport= st.selectbox("Select Sport", sport)

    succesful_athletes= helper.most_successful_by_sport(df1,selected_sport)

    st.table(succesful_athletes)


if user_menu == 'Country wise Analysis':
    st.sidebar.header('Select country and year')
    country= helper.country_year(df1)
    selected_country= st.sidebar.selectbox("Select Country", country)
    st.header(f'{selected_country}-year wise analysis')

    final_k = helper.country_medal_yearly(df1, selected_country)

    fig5= px.line(final_k, x='Year', y='Medal')
    st.plotly_chart(fig5)


    st.title(f'Number of medals per each sport for {selected_country} in every edition')
    fig6, ax= plt.subplots(figsize=(25,25))
    x= df1[df1['region']== selected_country]
    x= x.dropna(subset=['Medal'])
    x= x.drop_duplicates(subset=['Year','Sport','Event','Medal'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Medal',aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig6)

    st.title(f'Successful atheletes for {selected_country}')
    region_wise = helper.most_successful_by_region(df1, selected_country)
    st.table(region_wise)


if user_menu=='Athlete wise analysis':
    st.title('Athlete wise age analysis')
    athlete_df= df1.drop_duplicates(subset=['Name','region'])

    x1= athlete_df['Age'].dropna()
    x2= athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3= athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4= athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig= ff.create_distplot([x1,x2,x3,x4],['Over all Age','Gold','Silver','Bronze'], show_hist=False, show_rug=False)
    st.plotly_chart(fig)


    imag= athlete_df['Sport'].value_counts().reset_index()

    imag= imag[imag['count']>470]

    imag_list= imag['Sport'].tolist()


    x=[]

    name= []

    for sport in imag_list:
        temp_df= athlete_df[athlete_df['Sport']== sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig= ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title('Athelete wise age analysis- by Sport (Gold medalists)')
    st.plotly_chart(fig)


    sport = helper.sport_list(df1)
    st.title('Height vs Weight')
    selected_sport= st.selectbox("Select Sport", sport)
    athlete_df_wt_ht=helper.weight_vs_height(df1,selected_sport)
    fig,ax= plt.subplots()
    ax= sns.scatterplot(athlete_df_wt_ht['Weight'], athlete_df_wt_ht['Height'], hue=athlete_df_wt_ht['Medal'], style=athlete_df_wt_ht['Sex'], s= 50)
    st.pyplot(fig)