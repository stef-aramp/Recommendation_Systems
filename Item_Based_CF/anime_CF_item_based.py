#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 10:14:50 2017

@author: stephanosarampatzes
"""

# Import Libraries
import pandas as pd
import numpy as np

# data
rates = pd.read_csv('rating.csv')
anime = pd.read_csv('anime.csv')

###################################

# Replace -1 values with NaN. -1 = Did not watch or did not rate movie

rates = rates.replace({-1 : np.nan}, regex = True)

# minimize the size of dataframe for computation reasons
mini_rates = rates[rates.user_id <= 2000]

# create pivot table

user_ratings = mini_rates.pivot_table(index=['user_id'],columns=['anime_id'],
                                 values='rating')

# We'll use the min_periods argument to throw out results where fewer than 
# 100 users rated a given movie pair

corr_matrix = user_ratings.corr(method = 'pearson', min_periods = 100)
corr_matrix.head()

# select a random user

user1 = user_ratings.loc[1].dropna()

# empty series to add recommendations

recoms = pd.Series()

# find most correlated movies to user1's rates

for i in range(0,len(user1.index)):
        print('Adding similars for ', user1.index[i], '...')
        # Retrieve similar movies to this one that I rated
        sims = corr_matrix[user1.index[i]].dropna()
        # Now scale its similarity by how well I rated this movie
        sims = sims.map(lambda x: x * user1.iloc[i])
        # Add the score to the list of similarity candidates
        recoms = recoms.append(sims)
        
# sorting highest reccomendations
recoms.sort_values(inplace = True, ascending = False)

# group by anime. 
# Some recommendations may be the same for several user1's ratings

recoms = recoms.groupby(recoms.index).sum()
recoms.sort_values(inplace = True, ascending = False)
print(recoms.head(10))

# drop user1's ratings. We don't want duplicates
filter_sims = recoms.drop(user1.index)

# final recommendations
print('\nrecommendations for user1\n')
for r in filter_sims.index[:5]:
    print('title: ',anime.loc[anime['anime_id']==r]['name'].iloc[0],',  ',
          'rating:',anime.loc[anime['anime_id']==r]['rating'].iloc[0])
