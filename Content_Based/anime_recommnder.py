υρ#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:37:15 2017

@author: stephanosarampatzes
"""

# anime recommendation system based only on user viewing history.

import pandas as pd
import numpy as np


anime = pd.read_csv('anime.csv')

# unknown episodes 

print('Anime with unknown episodes :',anime.loc[anime['episodes']=='Unknown']['episodes'].count())
print(anime.loc[anime['episodes']=='Unknown']['type'].value_counts())
anime.loc[anime['episodes']=='Unknown'][:10]

# fill known as 1-episode anime

anime.loc[(anime['type'] == 'Special') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'
anime.loc[(anime['type'] == 'Movie') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'

anime.loc[(anime['genre'] == 'Hentai') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'

# Episodes from string to nuneric

anime['episodes'] = anime['episodes'].apply(pd.to_numeric, errors='ignore')
anime = anime.replace({'episodes' : { 'Unknown': np.nan}})

# drop some NaNs

print('Missing Values : \n', anime.isnull().sum())

nan_percentiles = round(anime.isnull().sum().sort_values(ascending=False)/len(anime)*100,2)

for i in range(len(nan_percentiles)):
    if nan_percentiles[i] > 0:
        print(nan_percentiles.index[i], nan_percentiles[i],'%')

anime = anime.dropna()

anime.isnull().sum()

# anime type encoding
# replace 'type' with int
 
anime = anime.replace({'type' : { 'TV': 1, 'OVA': 2, 'Movie' :3, 'Special' :4,
                                 'ONA' :5, 'Music' :6}})

# MESS WITH DUMMIES

genre_dummies = anime['genre'].str.get_dummies(sep=', ')

genre_dummies.columns

# Final DataFrame

final_df = pd.concat([anime, genre_dummies], axis=1)
final_df.head(2)

# Select Features
    
features = final_df.drop(['anime_id','name','genre'], axis=1)

# scale features

from sklearn.preprocessing import MaxAbsScaler

scaler = MaxAbsScaler()
scaled_feats = scaler.fit_transform(features)

# build the model

from sklearn.neighbors import  NearestNeighbors

nbrs = NearestNeighbors(n_neighbors = 6, algorithm = 'ball_tree').fit(scaled_feats)
distances, indices = nbrs.kneighbors(scaled_feats)

# this is a 'searching' function

def find_movies(movie):
    distances[movie]
    indices[movie]
    print('If you liked ', anime.iloc[movie][1],', we also recommend :')
    for m in indices[movie][1:]:
        print(anime.iloc[m][1],'\nCategory: ', anime.iloc[m][2],
          '\nRating',anime.iloc[m][5])
        if anime.iloc[m][3]==1:
            print('TV')
        elif anime.iloc[m][3]==2:
            print('OVA')
        elif anime.iloc[m][3]==3:
            print('Movie')
        elif anime.iloc[m][3]==4:
            print('Special')
        elif anime.iloc[m][3]==5:
            print('ONA')
        else:
            print('Music')
        
        print('# # #')
    return(movie)

# find your recommendations
find_movies(367)
    
