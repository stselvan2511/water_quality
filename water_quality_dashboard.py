import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
df = pd.read_excel(r'data/Water_Quality_dataset2.xlsx')
df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)

# Check if the required columns are present
if 'ph' in df.columns and 'Solids' in df.columns and 'Potability' in df.columns:
    # Calculate drinkable and non-drinkable based on updated conditions
    df['Drinkable'] = ((df['ph'].between(6.5, 8.5)) &
                       (df['Solids'] > 50) &
                       (df['Solids'] < 300) &
                       (df['Potability'] == 1)).astype(int)
    
    # Calculate drinkable and non-drinkable counts
    drinkable_count = df['Drinkable'].sum()
    non_drinkable_count = df['Drinkable'].size - drinkable_count
    
    # Prepare data for pie chart
    drinkable_counts = pd.Series([non_drinkable_count, drinkable_count], index=['Non-Drinkable', 'Drinkable'])
    
    # Visualize the data using Streamlit
    st.title('Water Quality Dashboard')

    # Show the first few rows of the dataframe
    st.subheader('Dataset Preview')
    st.write(df.head())

    # Create a two-column layout
    col1, col2 = st.columns([3, 1])  # Adjust the width ratios as needed

    with col1:
        # Pie chart for drinkable vs non-drinkable water
        st.subheader('Drinkable vs Non-Drinkable Water')
        fig, ax = plt.subplots()
        if drinkable_counts.sum() > 0:
            ax.pie(drinkable_counts, labels=drinkable_counts.index, autopct='%1.1f%%', startangle=90, colors=['red', 'green'])
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        else:
            ax.text(0.5, 0.5, 'No Data Available', horizontalalignment='center', verticalalignment='center')
        st.pyplot(fig)
    
    with col2:
        # Display counts for drinkable and non-drinkable water
        st.subheader('Counts of Drinkable and Non-Drinkable Water')
        st.write(f"**Total drinkable water entries:** {drinkable_count}")
        st.write(f"**Total non-drinkable water entries:** {non_drinkable_count}")

    # pH Distribution Plot with Conditions
    st.subheader('pH Distribution with Drinkability Conditions')
    fig, ax = plt.subplots()
    # Plot pH data with counts on y-axis
    sns.histplot(df['ph'], bins=30, kde=False, ax=ax,)
    # Highlight pH values outside the range 6.5 - 8.5
    ax.hist(df[~df['ph'].between(6.5, 8.5)]['ph'], bins=30, color='red', alpha=0.7, label='pH < 6.5 or pH > 8.5')
    # Highlight pH values within the range 6.5 - 8.5
    ax.hist(df[df['ph'].between(6.5, 8.5)]['ph'], bins=30, color='cyan', alpha=0.7, label='pH 6.5 - 8.5')
    ax.set_title('pH Value Distribution')
    ax.set_xlabel('pH')
    ax.set_ylabel('Count')
    ax.legend()
    st.pyplot(fig)

    # Solids Distribution Plot with Conditions
    st.subheader('Solids Distribution with Drinkability Conditions')
    fig, ax = plt.subplots()
    # Plot Solids data with counts on y-axis
    sns.histplot(df['Solids'], bins=30, kde=False, ax=ax)
    # Highlight Solids values outside the range 50 - 300 ppm
    ax.hist(df[~((df['Solids'] > 50) & (df['Solids'] < 300))]['Solids'], bins=30, color='orange', alpha=0.7, label='Solids ≤ 50 or Solids ≥ 300 ppm')
    # Highlight Solids values within the range 50 - 300 ppm
    ax.hist(df[(df['Solids'] > 50) & (df['Solids'] < 300)]['Solids'], bins=30, color='cyan', alpha=0.7, label='50 < Solids < 300 ppm')
    ax.set_title('Solids Value Distribution')
    ax.set_xlabel('Solids (ppm)')
    ax.set_ylabel('Count')
    ax.legend()
    st.pyplot(fig)

    # Potability Pie Chart
    st.subheader('Potability Distribution')
    fig, ax = plt.subplots()
    potability_counts = df['Potability'].value_counts()
    ax.pie(potability_counts, labels=potability_counts.index.map({1: 'Potable', 0: 'Non-Potable'}),
           autopct='%1.1f%%', startangle=90, colors=['blue', 'green'])
    ax.axis('equal')
    st.pyplot(fig)

    # Display conditions for drinkable water
    st.subheader('Conditions for Drinkability')
    st.write("""
    The water is considered drinkable if the following conditions are met:
    - **pH** is between **6.5 and 8.5**
    - **Solids** concentration is between **50 and 300 ppm**
    - **Potability** is **1** (indicating drinkable)
    """)
else:
    st.write("Required columns are not present in the dataset.")
