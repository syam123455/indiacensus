import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px 
import random
from PIL import Image
logo = Image.open('logo.png')
#pip install pandas numpy matplotlib seaborn streamlit
#to run streamlit :   streamlit run census.py 
st.set_page_config(page_title="INDIA CENSUS  EDA", page_icon=":bar_chart:", layout="wide")
st.image(logo)
# Define the list of names
names = ["21A21A6111-E Jeji Anil", "21A21A6158-Tusha Rahul B ", "21A21A6137-M S R Chandrika","21A21A6166-K Shyam chand","21A21A6101-A Leena","21A21A6140-N Upendra","21A21A6157-T Sumanth Raju","22A25A6105(L5)-T Naveen Babu"]
st.title("Exploratory Data Analysis on India Census Data Set")
# Add the names to the sidebar
st.sidebar.title("Project Team Members:")

for name in names:
    st.sidebar.write(name)
st.sidebar.title("Under The Guidance of :")
st.sidebar.write("Dr.Bomma.Ramakrishna")
# File upload
uploaded_file = st.file_uploader("Choose a India Census Dataset csv")
if uploaded_file is not None:
    data=pd.read_csv(uploaded_file)
    st.dataframe(data)
    
    st.title("India Census Data Analysis")

    if st.checkbox("checking weather the data is preprocessed or NOT ( Any NULL Values )"):
        st.write(data.isnull().sum())
    if st.checkbox("SOME COLUMN OPERATIONS"):
        option = st.radio("Select an operation:", 
                  ("View columns in the dataset", 
                   "Set a column as index", 
                   "Add suffix to column names", 
                   "Add prefix to column names"))
        if option == "View columns in the dataset":
            st.write(data.columns)
        elif option == "Set a column as index":
            st.write(data.set_index('District_code'))
        elif option == "Add suffix to column names":
            st.write(data.add_suffix('_rightone'))
        elif option == "Add prefix to column names":
            st.write(data.add_prefix('leftone_')) 
   
    if st.checkbox("SOME STATISTICAL OPERATIONS"):
        option = st.radio(
        'Select an operation',
        ('statistics of the dataset ?','Calculate state-wise total number of population and population with different religions',
        'How many Male Workers were there in Maharashtra state ?', 'Calculate the total population of India according to the 2011 Census ?',
        'Which state has the highest population ?','Calculate the correlation coefficient between two Attributes'))

        if option == 'statistics of the dataset ?':
            st.write(data.describe())

        if option == 'Calculate state-wise total number of population and population with different religions':
            st.write(data.groupby('State_name').agg({'Population': 'sum', 'Hindus': 'sum', 'Muslims': 'sum', 'Christians': 'sum', 'Sikhs': 'sum', 'Buddhists': 'sum', 'Jains': 'sum'}).sort_values(by='Population', ascending=False))

        if option == 'How many Male Workers were there in Maharashtra state ?':
            st.write(data[data.State_name == 'MAHARASHTRA']['Male_Workers'].sum())

        if option == 'Calculate the total population of India according to the 2011 Census ?':
            st.write("Total Population of India according to the 2011 Census is: ",data['Population'].sum())

        if option == 'Which state has the highest population ?':
            highest_population = data.groupby('State_name').agg({'Population': 'sum'}).sort_values(by='Population', ascending=False).head(1)
            st.write(f"{highest_population.index[0]} has the highest population of {highest_population['Population'][0]} it is beacause the no of districts in uttar pradesh is more") 

        if option == 'Calculate the correlation coefficient between two Attributes':
            corr = data['Male_Workers'].corr(data['Female_Workers'])
            st.write("Correlation coefficient:", corr)

     
    if st.header("\nData visualizations"):
        if st.checkbox("Show the percentages of Religions in India by a piechart"):
            st.write()
            fig = plt.figure(figsize=(50,25))
            ax1 = plt.subplot(312)
            explode = (0, 0.1, 0, 0)
            labels = ['Sikhs', 'Christians', 'Jains', 'Buddhists']
            val = [data.Sikhs.sum(),data.Christians.sum(),data.Jains.sum(),data.Buddhists.sum()]
            ax1.pie(val, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=270)
            plt.title('Pie Chart of Religions')
            st.pyplot(fig)
        if st.checkbox("Which state has the highest literacy rate?"):
            highest_literacy = data.groupby('State_name').agg({'Literate': 'mean'}).sort_values(by='Literate', ascending=False).head(1)
            fig = px.bar(data, x='State_name', y='Literate', title='Literacy rate by state', height=500)
            st.plotly_chart(fig)
        if st.checkbox("Which states have the highest number of male and female workers?"):
            workers = data.groupby('State_name').agg({'Male_Workers': 'sum', 'Female_Workers': 'sum'}).sort_values(by='Male_Workers', ascending=True).head(10)
            fig = px.bar(workers, x=workers.index, y=['Male_Workers', 'Female_Workers'], title='Number of Male and Female Workers by State', barmode='group', height=500)
            st.plotly_chart(fig)
        if st.checkbox("Population by state on a line chart"):
            pop_data = data.groupby('State_name').agg({'Population': 'sum'}).reset_index()
            fig = px.line(pop_data, x='State_name', y='Population', title='Line Chart Population by State')
            st.plotly_chart(fig)
        if st.checkbox("Histogram for showing the Age Groups"):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(data['Age_Group_0_29'], bins=10,label='Age 0-29',color='skyblue',edgecolor='black')
            ax.hist(data['Age_Group_30_49'], bins=10,label='Age 30-49',edgecolor='black')
            ax.hist(data['Age_Group_50'], bins=10,label='Age 50',color='royalblue',edgecolor='black')
            ax.set_title('Histogram of Age Group Population')
            ax.set_xlabel('Total Population')
            ax.set_ylabel('Frequency')
            plt.legend()
            st.pyplot(fig)
        if st.checkbox("Correlation heatmap between two similar columns"):
            corr_matrix = data.iloc[:,3:7].corr()
            fig,ax=plt.subplots()
            sns.heatmap(corr_matrix)
            plt.title("Correlation Heatmap :")
            st.pyplot(fig)

    if st.checkbox("Find the statewise population  of India "):
        state = st.selectbox('Select a state:', sorted(data['State_name'].unique()))
        state_data = data[data['State_name'] == state]
        district_populations = state_data.groupby('District_name')['Population'].sum()
        st.write('Total population by district in', state, ':')
        st.write(district_populations)
    

    def calc_pop_density(population, area):
        return population / area

    def indian_census():
        st.header("India Population Density Calculator")
        population = st.number_input("Enter India's population in 2011:")
        area = st.number_input("Enter India's land area in square kilometers:")

        if population and area:
            pop_density = calc_pop_density(population, area)
            st.write("The population density of India in 2011 was:", pop_density, "people per square kilometer")
    if __name__ == '__main__':
        indian_census()
   
        
    if st.header("Check the Details of Selected States and Districts"):
        state_options = data["State_name"].unique()
        district_options = {}
        for state in state_options:
           district_options[state] = data.loc[data["State_name"] == state, "District_name"].unique()
        selected_state = st.selectbox("Select a state",state_options)
        selected_districts = st.multiselect("Select districts", district_options[selected_state])
        if selected_districts:
            filtered_data = data.loc[(data["State_name"] == selected_state) & (data["District_name"].isin(selected_districts))]
        else:
            filtered_data = data.loc[data["State_name"] == selected_state]
        st.write(filtered_data)

    

