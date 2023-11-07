import geopandas as gdp
import json
import matplotlib.pyplot as plt
import pandas as pd
from cartoframes.viz import Map, Layer, popup_element
import folium
import seaborn as sns
import os


# Reading the table with all the companies filtered 
#df = pd.read_csv('data/filter_companies.csv')

# Defining a function to change the colocar when has the Category Code of company 'Gam' to include the game and gaming industry
def marker_color_for_gam(row):
    if 'gam' in row['category_code'].lower():
        marker_color = 'red'
        marker_size = 'large'
    else:
        marker_color = 'blue'
        marker_size = 'small'
    return marker_color, marker_size

def ploting_map(df, lat, lon, zoom):
    my_map = folium.Map(location=[lat, lon], zoom_start=zoom)
    for index, row in df.iterrows():
        color, size = marker_color_for_gam(row)
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['name'],
            icon=folium.Icon(color=color, icon_size=size)
        ).add_to(my_map)
    return my_map

# Defining a function to get a df and plot a barplot with the Score per Neighborhood
def barplot_score_per_neighborhood(df):
    df = df.sort_values(by='final_score', ascending=False)
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='Neighborhood', y='final_score', data=df, color='skyblue')
    plt.xlabel('Neighborhood')
    plt.ylabel('Score')
    plt.title('Score per Neighborhood')
    plt.xticks(rotation=50)

    # Add value labels to the bars
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), 
                    textcoords='offset points')

    plt.tight_layout()

    # Save and display the plot
    plt.savefig('../images/score_per_neighborhood.png')
    os.system('open images/score_per_neighborhood.png')