import streamlit as st
import pandas as pd
import plotly_express as px

df = pd.read_csv('vehicles_us.csv', na_values=[])
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# create a text header above the dataframe
st.header('Vehicles data')
# display the dataframe with the streamlit
st.dataframe(df)


st.header('Factors which influence the price')
st.write("""Let's examine the factors, which influence car price: fuel, condition, transmition, manufacturer.
""")

# create a plotly histogram with the split by parameter of choice
# create list of options
list_for_hist=['fuel', 'condition', 'transmission', 'manufacturer']

# create selectbox
choice_for_hist = st.selectbox('Price factors', list_for_hist)

# draw histogram
fig1 = px.histogram(df, x='price', color=choice_for_hist, range_x=[0, 100000])

# add title
fig1.update_layout(title="<b> Price depending on {}<b>".format(choice_for_hist))

# display the figure with streamlit
st.write(fig1)


st.header('Vehicle days listed between manufactures')
# get a list of car manufacturers
manufac_list = sorted(df['manufacturer'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                              label='Select first manufacturer',
                              options=manufac_list,
                              index=manufac_list.index('ford')
                              )
# second dropdown menu
manufacturer_2 = st.selectbox(
                              label='Select second manufacturer',
                              options=manufac_list,
                              index=manufac_list.index('chevrolet')
                              )

# filter the dataframe
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]

# checkbox if a user wants to normalize histogram
normalize = st.checkbox('Show in percentages', value=True, key='Days_listed in percent')
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram
fig = px.histogram(df_filtered,
                   x='days_listed',
                   nbins=30,
                   color='manufacturer',
                   histnorm=histnorm,
                   barmode='overlay')

# display the figure with the strimlit

st.write(fig)


# create age category of cars
df['age']=2022-df['model_year']

def age_cat(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>10: return '>10'

df['age_cat'] = df['age'].apply(age_cat)

# create scatter plot for price depending on cylinders, odometer, days listed
st.header('Price change depending on cylinders, odometer, days listed')

list_for_scatter = ['cylinders', 'odometer', 'days_listed']
choice_for_scatter = st.selectbox('Price factor', list_for_scatter)
fig2 = px.scatter(df, x='price', y=choice_for_scatter, hover_data=['age_cat'])

fig2.update_layout(title='<b> Price depending on {}'.format(choice_for_scatter))
st.write(fig2)