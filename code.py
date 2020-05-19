# --------------
#Importing header files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Path of the file is stored in the variable path
path #path = 'Olympics_Cleaned.csv'

#Code starts here
# Data Loading 
data = pd.read_csv(path)

# In the dataframe, rename the column 'Total' to 'Total_Medals'
#data.rename(index = str, columns = {'Total' : 'Total_Medals'}, inplace = True)
data.rename(columns = {'Total' : 'Total_Medals'}, inplace = True)
#print(data.head(10))

# Summer or Winter
# Create a new column Better_Event that stores 'Summer','Winter' or 'Both' based on the comparision between the total medals won in Summer event and Winter event (i.e. comparision between the Total_Summer and Total_Winter columns) using "np.where()"function.
data['Better_Event'] = np.where(data['Total_Summer'] > data['Total_Winter'], 'Summer', np.where(data['Total_Summer'] == data['Total_Winter'], 'Both', 'Winter'))
#print(data.head())

# Find out which has been a better event with respect to all the performing countries by using 'value_counts()' function and store it in a new variable called 'better_event'.
better_event = data['Better_Event'].value_counts().idxmax()
#print(better_event)

# Top 10
# Create a new dataframe subset called 'top_countries' with the columns ['Country_Name','Total_Summer', 'Total_Winter','Total_Medals'] only
top_countries = data[['Country_Name', 'Total_Summer', 'Total_Winter', 'Total_Medals']]
#print(top_countries.tail())

# Drop the last row from 'top_countries'(The last row contains the sum of the medals)
top_countries.drop(top_countries.tail(1).index, inplace = True)
#print(top_countries.tail())

# Create a function called 'top_ten' that:
#    Takes the dataframe 'top_countries' and a column name as parameters.
#    Creates a new empty list called 'country_list'
#    Find the top 10 values for that particular column (for e.g. 'Total_Summer') using "nlargest()" function
#    From the dataframe returned by nlargest function, slices the Country_Name column and stores it in the 'country_list' list
#    Returns the 'country_list'
def top_ten(top_countries, column):
    country_list = []
    country_list = list(top_countries.nlargest(10, column)['Country_Name'])    
    return country_list

# Call the 'top_ten()' function for the three columns :Total_Summer,Total_Winter and Total_Medals and store their respective results in lists called 'top_10_summer', 'top_10_winter' and 'top_10'
top_10_summer = top_ten(top_countries, 'Total_Summer')
#print(top_10_summer)
top_10_winter = top_ten(top_countries, 'Total_Winter')
#print(top_10_winter)
top_10 = top_ten(top_countries, 'Total_Medals')
#print(top_10)

# Create a new list 'common' that stores the common elements between the three lists('top_10_summer', 'top_10_winter' and 'top_10')
common = []
for element in top_10:
    if(element in top_10_summer and element in top_10_winter):
        common.append(element)

#print(common)

# Plotting top 10
# Take the three previously created lists(top_10_summer, top_10_winter, top_10)
# Subset the dataframe 'data' based on the country names present in the list top_10_summer using "isin()" function on the column Country_Name. Store the new subsetted dataframes in 'summer_df'. Do the similar operation using top_10_winter and top_10 and store the subset dataframes in 'winter_df' & 'top_df' respectively.
summer_df = data[data['Country_Name'].isin(top_10_summer)]
winter_df = data[data['Country_Name'].isin(top_10_winter)]
top_df = data[data['Country_Name'].isin(top_10)]

# Take each subsetted dataframe and plot a bar graph between the country name and total medal count according to the event (For e.g. for 'summer_df' plot a bar graph between Country_Name and Total_Summer)
#summer_df.plot(x = 'Country_Name', y = 'Total_Medals', kind = 'bar', label = 'Summer')
#winter_df.plot(x = 'Country_Name', y = 'Total_Medals', kind = 'bar', label = 'Winter')
#top_df.plot(x = 'Country_Name', y = 'Total_Medals', kind = 'bar', label = 'Top')

# Top Performing Countries
# In the dataframe 'summer_df'(created in the previous function) , create a new column Golden_Ratio which is the quotient after dividing the two columns Gold_Summer and Total_Summer.
summer_df['Golden_Ratio'] = summer_df['Gold_Summer'] / summer_df['Total_Summer']
#print(summer_df)
# Find the max value of Golden_Ratio and the country associated with it and store them in summer_max_ratio and summer_country_gold respectively.
summer_max_ratio = summer_df['Golden_Ratio'].max()
#print(summer_max_ratio)
max_idx = summer_df['Golden_Ratio'].idxmax()
#rint(max_idx)
summer_country_gold = summer_df.at[max_idx, 'Country_Name']
#print(summer_country_gold)

# In the dataframe 'winter_df'(created in the previous function) , create a new column Golden_Ratio which is the quotient after dividing the two columns Gold_Winter and Total_Winter. Find the max value of Golden_Ratio and the country associated with it and store them in 'winter_max_ratio' and 'winter_country_gold' respectively.
winter_df['Golden_Ratio'] = winter_df['Gold_Winter']/winter_df['Total_Winter']
winter_max_ratio = winter_df['Golden_Ratio'].max()
winter_country_gold = winter_df.at[ winter_df['Golden_Ratio'].idxmax(), 'Country_Name']

# In the dataframe 'top_df' (created in the previous function), create a new column Golden_Ratio which is the quotient after dividing the two columns Gold_Total and Total_Medals.
top_df['Golden_Ratio'] = top_df['Gold_Total'] / top_df['Total_Medals']
# Find the max value of Golden_Ratio and the country associated with it and store them in top_max_ratio' and 'top_country_gold' respectively.
top_max_ratio = top_df['Golden_Ratio'].max()
top_country_gold = top_df.at[ top_df['Golden_Ratio'].idxmax(), 'Country_Name']

# Best in the world 
# Drop the last row from the dataframe(The last row contains the total of all the values calculated vertically) and save the result in 'data_1'
data_1 = data.copy()
data_1.drop(data_1.tail(1).index, inplace = True)
#print(data_1.head())

# Update the dataframe 'data_1' to include a new column called 'Total_Points' which is a weighted value where each gold medal counts for 3 points, silver medals for 2 points, and bronze medals for 1 point. (i.e. You need to take the weighted value of Gold_Total, Silver_Total and Bronze_Total)
data_1['Total_Points'] = (3 * data_1['Gold_Total']) + (2 * data_1['Silver_Total']) + (1 * data_1['Bronze_Total'])
#print(data_1.head())

# Find the max value of Total_Points in 'data_1' and the country associated with it and store it in variables 'most_points' and 'best_country' respectively.
most_points = data_1['Total_Points'].max()
#print(most_points)
best_country = data_1.at[ data_1['Total_Points'].idxmax(), 'Country_Name']
#print(best_country)

# Plotting the best
# Create a single row dataframe called 'best' from 'data' where the value of column 'Country_Name' is equal to 'best_country' (The variable you created in the previous task)
best = data[data['Country_Name'] == best_country]
#print(best)

# Subset 'best' even further by only including the columns: ['Gold_Total', 'Silver_Total', 'Bronze_Total']
best = best[['Gold_Total', 'Silver_Total', 'Bronze_Total']]
#print(best)

# Create a stacked bar plot of 'best' using "DataFrame.plot.bar()" function
# Name the x-axis as United States using "plt.xlabel()"
# Name the y-axis as Medals Tally using "plt.ylabel()"
# Rotate the labels of x-axis by 45o using "plt.xticks()"
best.plot.bar()
plt.xlabel('United States')
plt.ylabel('Medals Tally')
plt.xticks(rotation = 45)


