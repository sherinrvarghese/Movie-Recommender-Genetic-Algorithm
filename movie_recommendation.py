# -*- coding: utf-8 -*-
"""Copy of GA_MovieRecommendation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1N3du0zk0hFhoUB_CH7c5H8tQRaYZI8JS
"""

# Supress Warnings
import warnings
warnings.filterwarnings('ignore')

"""#Importing the Libraries"""

# lets import the basic Libraries
import numpy as np
import pandas as pd

# for data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# for jupyter notebook widgets
#import ipywidgets as widgets
#from ipywidgets import interact
#from ipywidgets import interact_manual

# for Interactive Shells
from IPython.display import display

# setting up the chart size and background
plt.rcParams['figure.figsize'] = (16, 8)
plt.style.use('fivethirtyeight')

"""#Loading the Data Set"""

# lets read the dataset
data = pd.read_csv('movie_metadata.csv')

"""#Shape of the Data"""

# lets check the shape
print(data.shape)

"""#Information about the Data Set"""

# lets check the column wise info

data.info()

# lets remove unnecassary columns from the dataset

# Use the 'drop()' function to drop the unnecessary columns

data = data.drop(['color',
                      'director_facebook_likes',
                      'actor_3_facebook_likes',
                      'actor_1_facebook_likes',
                      'cast_total_facebook_likes',
                      'actor_2_facebook_likes',
                      'facenumber_in_poster',
                      'content_rating',
                      'country',
                      'movie_imdb_link',
                      'aspect_ratio',
                      'plot_keywords',
                      ],
                       axis = 1)
data.columns

"""#Missing Values Imputation"""

# lets check the rows having high percentage of missing values in the dataset

round(100*(data.isnull().sum()/len(data.index)), 2)

# Since 'gross' and 'budget' columns have large number of NaN values, drop all the rows with NaNs at this column using the
# 'isnan' function of NumPy alongwith a negation '~'

data = data[~np.isnan(data['gross'])]
data = data[~np.isnan(data['budget'])]

# Now lets again check the Missing Values column wise
data.isnull().sum()

# The rows for which the sum of Null is less than two are retained

data = data[data.isnull().sum(axis=1) <= 2]
data.isnull().sum()

# lets impute the missing values

# using mean for numerical columns
data['num_critic_for_reviews'].fillna(data['num_critic_for_reviews'].mean(), inplace = True)
data['duration'].fillna(data['duration'].mean(), inplace = True)

# using mode for categorical column
data['language'].fillna(data['language'].mode()[0], inplace = True)

# As we know that We cannot use statistical values for imputing the missing values of actor names, so we will replace the
# actor names with "Unknown Actor"

data['actor_2_name'].fillna('Unknown Actor', inplace = True)
data['actor_3_name'].fillna('Unknown Actor', inplace = True)

# as we imputed all the missing values lets check the no. of total missing values in the dataset
data.isnull().sum().sum()

"""# Feature Modification"""

# Lets convert the gross and budget from $ to Million $ to make our analysis easier

data['gross'] = data['gross']/1000000
data['budget'] = data['budget']/1000000

# lets create a Profit column using the Budget and Gross

data['Profit'] = data['gross'] - data['budget']

# lets also check the name of Top 10 Profitable Movies
data[['Profit','movie_title']].sort_values(by = 'Profit', ascending  = False).head(10)

# By looking at the above result we can easily analyze that there are some duplicate

# lets print the no. of rows before removing Duplicates
print("No. of Rows Before Removing Duplicates: ",data.shape[0])

# so lets remove all the duplicates from the data
data.drop_duplicates(subset = None, keep = 'first', inplace = True)

# lets print the no. of rows after removing Duplicates
print("No. of Rows After Removing Duplicates: ",data.shape[0])

"""#Top 10 Movies with Highest profit"""

# Lets check the Top 10 Profitable Movies Again
data[['movie_title','Profit']].sort_values(by = 'Profit', ascending  = False).head(10)

"""#Manupulating the Duration and Language Collumn"""

# lets check the values in the language column
data['language'].value_counts()

# Looking at the above output we can easily observe that out of 3,500 movies only 150 movies are of other languages

# so it is better to keep only two languages that is English and Foreign
def language(x):
    if x == 'English':
        return 'English'
    else:
        return 'Foreign'

# lets apply the function on the language column
data['language'] = data['language'].apply(language)

# lets check the values again
data['language'].value_counts()

# The Duration of Movies is not varying a lot but we know that most of the users either like watching long movies or short
# duration movies. we can categorize the movies in two part i.e., short and long.
# lets define a function for categorizing Duration of Movies
def duration(x):
    if x <= 120:
        return 'Short'
    else:
        return 'Long'

# lets apply this function on the duration column
data['duration'] = data['duration'].apply(duration)

# lets check the values of Duration column
data['duration'].value_counts()

# lets also check the values in the Genres Column

data['genres'].value_counts()

data['genres'].str.split('|')[0]

# we can see from the above output that most of the movies are having a lot of genres
# also, a movie can have so many genres so lets keep four genres

data['Moviegenres'] = data['genres'].str.split('|')
data['Genre1'] = data['Moviegenres'].apply(lambda x: x[0])

# Some of the movies have only one genre. In such cases, assign the same genre to 'genre_2' as well
data['Genre2'] = data['Moviegenres'].apply(lambda x: x[1] if len(x) > 1 else x[0])
data['Genre3'] = data['Moviegenres'].apply(lambda x: x[2] if len(x) > 2 else x[0])
data['Genre4'] = data['Moviegenres'].apply(lambda x: x[3] if len(x) > 3 else x[0])

# lets check the head of the  data
data[['genres','Genre1','Genre2','Genre3','Genre4']].head(5)

"""#Data Visualisation"""

# lets also calculate the Social Media Popularity of a Movie

# to calculate popularity of a movie, we can aggregate No. of voted users, No. of Users for Reviews, and Facebook Likes.
data['Social_Media_Popularity'] = (data['num_user_for_reviews']/
                                   data['num_voted_users'])*data['movie_facebook_likes']

# lets also check the Top 10 Most Popular Movies on Social Media
x = data[['movie_title','Social_Media_Popularity']].sort_values(by = 'Social_Media_Popularity',
                                                                ascending = False).head(10).reset_index()
print(x)

sns.barplot(x=x['movie_title'], y=x['Social_Media_Popularity'],data=data, palette = 'magma')
plt.title('Top 10 Most Popular Movies on Social Media', fontsize = 20)
plt.xticks(rotation = 90, fontsize = 14)
plt.xlabel(' ')
plt.show()

# Lets compare the Gross with Genres

# first group the genres and get max, min, and avg gross of the movies of that genre.)
display(data[['Genre1','gross',]].groupby(['Genre1']).agg(['max','mean','min']).style.background_gradient(cmap = 'Wistia'))

# lets plot these values using lineplot
data[['Genre1','gross',]].groupby(['Genre1']).agg(['max','mean','min']).plot(kind = 'line', color = ['red','black','blue'])
plt.title('Which Genre is Most Bankable?', fontsize = 20)
plt.xticks(np.arange(17), ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
       'Documentary', 'Drama', 'Family', 'Fantasy', 'Horror', 'Musical',
       'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'Western'], rotation = 90, fontsize = 15)
plt.ylabel('Gross', fontsize = 15)
plt.xlabel(' ',)
plt.show()

print('The Most Profitable Movie from each Genre')
display(data.loc[data.groupby(data['Genre1'])['Profit'].idxmax()][['Genre1',
                                    'movie_title','gross']].style.background_gradient(cmap = 'copper'))

# lets convert year into integer
data['title_year'] = data['title_year'].astype('int')

print('Most Profitable Years in Box Office')
display(data[['title_year','language','Profit']].groupby(['language',
                                    'title_year']).agg('sum').sort_values(by = 'Profit',
                                     ascending = False).head(10).style.background_gradient(cmap = 'Greens'))

# lets plot them
sns.lineplot(x=data['title_year'], y=data['Profit'], data=data,hue = data['language'])
plt.title('Time Series for Box Office Profit for English vs Foreign Movies', fontsize = 20)
plt.xticks(fontsize = 18)
plt.xlabel(' ')
plt.show()

print("Movies that Made Huge Losses")
display(data[data['Profit'] < -2000][['movie_title',
                        'language','Profit']].style.background_gradient(cmap = 'Reds'))

display(data[data['duration'] == 'Long'][['movie_title', 'duration', 'gross',
                    'Profit']].sort_values(by = 'Profit',ascending = False).head(5).style.background_gradient(cmap = 'spring'))

display(data[data['duration'] == 'Short'][['movie_title', 'duration', 'gross',
                    'Profit']].sort_values(by = 'Profit',ascending = False).head(5).style.background_gradient(cmap = 'spring'))

sns.barplot(x=data['duration'], y=data['gross'], data=data,hue = data['language'], palette = 'spring')
plt.title('Gross Comparison')

print("Average IMDB Score for Long Duration Movies is {0:.2f}".format(data[data['duration'] == 'Long']['imdb_score'].mean()))
print("Average IMDB Score for Short Duration Movies is {0:.2f}".format(data[data['duration'] == 'Short']['imdb_score'].mean()))

print("\nHighest Rated Long Duration Movie\n",
    data[data['duration'] == 'Long'][['movie_title','imdb_score']].sort_values(by = 'imdb_score', ascending = False).head(1))
print("\nHighest Rated Short Duration Movie\n",
    data[data['duration'] == 'Short'][['movie_title','imdb_score']].sort_values(by = 'imdb_score', ascending = False).head(1))

sns.boxplot(x=data['imdb_score'], y=data['duration'], data=data,palette = 'copper')
plt.title('IMDB Ratings vs Gross', fontsize = 20)
plt.xticks(rotation = 90)
plt.show()

def query_actors(x):
    a = data[data['actor_1_name'] == x]
    b = data[data['actor_2_name'] == x]
    c = data[data['actor_3_name'] == x]
    y = pd.concat([a, b, c])


    y = y[['movie_title',
       'budget',
       'gross',
       'title_year',
       'genres',
       'language',
       'imdb_score',
        ]]
    return y

query_actors('Matthew Perry')

def actors_report(x):
    a = data[data['actor_1_name'] == x]
    b = data[data['actor_2_name'] == x]
    c = data[data['actor_3_name'] == x]
    y = pd.concat([a, b, c])

    print("Time:",y['title_year'].min(), y['title_year'].max())
    print("Max Gross : {0:.2f} Millions".format(y['gross'].max()))
    print("Avg Gross : {0:.2f} Millions".format(y['gross'].mean()))
    print("Min Gross : {0:.2f} Millions".format(y['gross'].min()))
    print("Number of 100 Million Movies :", y[y['gross'] > 100].shape[0])
    print("Avg IMDB Score : {0:.2f}".format(y['imdb_score'].mean()))
    print("Most Common Genres:\n",y['Genre1'].value_counts().head())

actors_report('Meryl Streep')

# Lets compare Brad Pitt, Leonardo Caprio and Tom Cruise

def critically_acclaimed_actors(m):
    a = data[data['actor_1_name'] == m]
    b = data[data['actor_2_name'] == m]
    c = data[data['actor_3_name'] == m]
    y = pd.concat([a, b, c])

    return y['num_critic_for_reviews'].sum().astype('int')


print("Number of Critics Reviews for Brad Pitt")
display(critically_acclaimed_actors('Brad Pitt'))

print("Number of Critics Reviews for Leonardo DiCaprio")
display(critically_acclaimed_actors('Leonardo DiCaprio'))

print("Number of Critics Reviews for Tom Cruise")
display(critically_acclaimed_actors('Tom Cruise'))

!pip install ipywidgets

from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

pd.set_option('display.max_rows', 3000)

@interact
def show_movies_more_than(column='imdb_score', score=9.0):
    x = data.loc[data[column] > score][[ 'title_year','movie_title',
                                       'director_name',
                                       'actor_1_name',
                                       'actor_2_name',
                                       'actor_3_name',
                                       'Profit',
                                       'imdb_score',
                                    ]]
    x = x.sort_values(by = 'imdb_score', ascending = False)
    x = x.drop_duplicates(keep = 'first')
    return x

pd.set_option('display.max_rows', 30000)

@interact
def show_articles_more_than(column=['budget','gross'], x=1000):
    return data.loc[data[column] > x][['movie_title','duration','gross','Profit','imdb_score']]

"""#Recommending Movies based on Languages"""

def recommend_lang(x):
    y = data[['language','movie_title','imdb_score']][data['language'] == x]
    y = y.sort_values(by = 'imdb_score', ascending = False)
    return y.head(15)

recommend_lang('Foreign')

"""#Recommending Movies Based on Actors"""

def recommend_movies_on_actors(x):
    a = data[['movie_title','imdb_score']][data['actor_1_name'] == x]
    b = data[['movie_title','imdb_score']][data['actor_2_name'] == x]
    c = data[['movie_title','imdb_score']][data['actor_3_name'] == x]
    a = pd.concat([a, b, c])

    a = a.sort_values(by = 'imdb_score', ascending = False)
    return a.head(15)

recommend_movies_on_actors('Leonardo DiCaprio')

"""#Recommending similar Genres"""

from mlxtend.preprocessing import TransactionEncoder

x = data['genres'].str.split('|')
te = TransactionEncoder()
x = te.fit_transform(x)
x = pd.DataFrame(x, columns = te.columns_)

# lets check the head of x
x.head()

# lets convert this data into boolean so that we can perform calculations
genres = x.astype('int')

genres.head()

# now, lets insert the movie titles in the first column, so that we can better understand the data
genres.insert(0, 'movie_title', data['movie_title'])

genres.head()

# lets set these movie titles as index of the data
genres = genres.set_index('movie_title')
genres.head()

# making a recommendation engine for getting similar genres

def recommendation_genres(gen):
    gen = genres[gen]
    similar_genres = genres.corrwith(gen)
    similar_genres = similar_genres.sort_values(ascending=False)
    similar_genres = similar_genres.iloc[1:]
    return similar_genres.head(3)

recommendation_genres('Documentary')

"""#Recommending similar Movies"""

# lets make a sparse matrix to recommend the movies

x = genres.transpose()
x

x.shape

# making a recommendation engine for getting similar movies

def recommendation_movie(movie):
    movie = x[movie+'\xa0']
    similar_movies = x.corrwith(movie)
    similar_movies = similar_movies.sort_values(ascending=False)
    similar_movies = similar_movies.iloc[1:]
    return similar_movies.head(20)

genres=x.copy()
genres

genres = genres.transpose()
genres.head()

# lets test on some results
recommendation_movie('John Carter')

"""#**GENETIC ALGORITHM**

## Based on Movies
"""

import numpy as np
import random

def fitness_function(weights, genres):
    genre_weights = np.array(weights)

    # Calculate recommendations based on genre similarity and weights.
    recommendations = np.dot(genres.values, genre_weights)

    return recommendations

def recommend_movies_by_genre(movie_name, genres, num_recommendations=10, population_size=25, mutation_rate=0.1, generations=50):

    # Ensure the movie_name exists in the dataset
    e=movie_name + '\xa0'
    if e not in genres.iloc[:, 0]:
        return "Movie not found in the dataset."

    population = np.random.uniform(0, 1, genres.shape[1])
   # print(population)
    for generation in range(generations):
        # Evaluate the fitness of each individual in the population.
        fitness_scores = fitness_function(population, genres)

        # Apply mutation to the best-performing individual
        max_fitness_index = np.argmax(fitness_scores)
        best_individual=0
        if max_fitness_index < len(population):
            best_individual = population[max_fitness_index]
        else:
            # Handle the case where the index is out of bounds
            pass
            #print("Error: Index out of bounds")

        mutation_values = np.random.uniform(-0.1, 0.1, genres.shape[1])
        new_individual = best_individual + mutation_values

        population = new_individual

    recommendations = fitness_function(population, genres)

    # Sort movies based on recommendations.
    top_movie_indices = np.argsort(recommendations)[::-1]

    # Exclude the input movie itself and get the top recommendations
    top_recommendations = genres.index[top_movie_indices[1:num_recommendations + 1]]

    return top_recommendations

# Example usage:
movie_name = 'Avatar'
recommended_movies = recommend_movies_by_genre(movie_name, genres)
print(f"Top 10 Movie Recommendations for '{movie_name}':")
print(recommended_movies)

def precision(actual, recommended):
    true_positives = len(set(actual) & set(recommended))
    if len(recommended) == 0:
        return 0
    return true_positives / len(recommended)

def recall(actual, recommended):
    true_positives = len(set(actual) & set(recommended))
    if len(actual) == 0:
        return 0
    return true_positives / len(actual)

def f1_score(actual, recommended):
    precision_val = precision(actual, recommended)
    recall_val = recall(actual, recommended)
    if precision_val + recall_val == 0:
        return 0
    return 2 * (precision_val * recall_val) / (precision_val + recall_val)

"""## Based on Popularity"""

import numpy as np
import random

# Define your fitness function for the recommendation system.
def fitness_function(weights):
    imdb_weight, social_media_weight = weights

    # Combine 'imdb_score' and 'Social_Media_Popularity' using the weights.
    recommendations = data['imdb_score'] * imdb_weight + data['Social_Media_Popularity'] * social_media_weight

    # Sort movies based on the recommendations.
    top_recommendations = data[['movie_title', 'imdb_score', 'Social_Media_Popularity']].copy()
    top_recommendations['Recommendation Score'] = recommendations

    # Sort by the recommendation score in descending order.
    top_recommendations = top_recommendations.sort_values(by='Recommendation Score', ascending=False)

    # Calculate the quality of recommendations (e.g., precision, recall, F1-score).
    # You can use any relevant metric for your task.

    # For simplicity, let's calculate the mean recommendation score.
    mean_recommendation_score = top_recommendations['Recommendation Score'].mean()

    # Return the mean recommendation score to maximize in the genetic algorithm.
    return mean_recommendation_score

# Define the genetic algorithm parameters.
population_size = 50
mutation_rate = 0.1
generations = 100

# Initialize the population with random weights.
population = [(np.random.uniform(0, 1), np.random.uniform(0, 1)) for _ in range(population_size)]

# Main loop for genetic algorithm.
for generation in range(generations):
    # Evaluate the fitness of each individual in the population.
    fitness_scores = [fitness_function(weights) for weights in population]

    # Select the top-performing individuals to become parents
    parents = np.argsort(fitness_scores)[-population_size // 2:]

    # Create a new population through crossover and mutation
    new_population = []

    for _ in range(population_size // 2):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        # Perform crossover to create a new individual (combine weights)
        crossover_point = random.randint(0, 1)
        new_individual = (population[parent1][0] if crossover_point == 0 else population[parent2][0],
                          population[parent1][1] if crossover_point == 1 else population[parent2][1])

        # Apply mutation with a certain probability (change weights)
        if random.random() < mutation_rate:
            mutation_value = (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))
            new_individual = (new_individual[0] + mutation_value[0], new_individual[1] + mutation_value[1])

        new_population.append(new_individual)

    population = new_population

# Find the best solution after optimization
best_weights = population[np.argmax(fitness_scores)]

print("Optimal weights for 'imdb_score' and 'Social_Media_Popularity':", best_weights)

# Generate movie recommendations based on the optimal weights
imdb_weight, social_media_weight = best_weights
recommendations = data['imdb_score'] * imdb_weight + data['Social_Media_Popularity'] * social_media_weight

# Sort movies based on recommendations
top_recommendations = data[['movie_title', 'imdb_score', 'Social_Media_Popularity']].copy()
top_recommendations['Recommendation Score'] = recommendations

# Sort by the recommendation score in descending order
top_recommendations = top_recommendations.sort_values(by='Recommendation Score', ascending=False)

# Display the top recommended movies
top_10_recommendations = top_recommendations[['movie_title', 'Recommendation Score']].head(10)
print("Top 10 Movie Recommendations:")
print(top_10_recommendations)

"""## Based on Actor Name"""

import numpy as np
import random

# Ask the user for the specific actor they are interested in.
user_actor = input("Enter the actor's name for recommendations: ")

# Define your fitness function for the recommendation system.
def fitness_function(weights):
    imdb_weight, social_media_weight = weights

    # Filter movies that involve the user-specified actor.
    actor_filter = data['actor_1_name'] == user_actor

    # Combine 'imdb_score' and 'Social_Media_Popularity' using the weights.
    recommendations = data[actor_filter]['imdb_score'] * imdb_weight + data[actor_filter]['Social_Media_Popularity'] * social_media_weight

    # Sort movies based on the recommendations.
    top_recommendations = data[actor_filter][['movie_title', 'imdb_score', 'Social_Media_Popularity']].copy()
    top_recommendations['Recommendation Score'] = recommendations

    # Sort by the recommendation score in descending order.
    top_recommendations = top_recommendations.sort_values(by='Recommendation Score', ascending=False)

    # Calculate the quality of recommendations (e.g., precision, recall, F1-score).
    # You can use any relevant metric for your task.

    # For simplicity, let's calculate the mean recommendation score.
    mean_recommendation_score = top_recommendations['Recommendation Score'].mean()

    # Return the mean recommendation score to maximize in the genetic algorithm.
    return mean_recommendation_score

# Define the genetic algorithm parameters.
population_size = 50
mutation_rate = 0.1
generations = 100

# Initialize the population with random weights.
population = [(np.random.uniform(0, 1), np.random.uniform(0, 1)) for _ in range(population_size)]

# Main loop for genetic algorithm.
for generation in range(generations):
    # Evaluate the fitness of each individual in the population.
    fitness_scores = [fitness_function(weights) for weights in population]

    # Select the top-performing individuals to become parents
    parents = np.argsort(fitness_scores)[-population_size // 2:]

    # Create a new population through crossover and mutation
    new_population = []

    for _ in range(population_size // 2):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        # Perform crossover to create a new individual (combine weights)
        crossover_point = random.randint(0, 1)
        new_individual = (population[parent1][0] if crossover_point == 0 else population[parent2][0],
                          population[parent1][1] if crossover_point == 1 else population[parent2][1])

        # Apply mutation with a certain probability (change weights)
        if random.random() < mutation_rate:
            mutation_value = (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))
            new_individual = (new_individual[0] + mutation_value[0], new_individual[1] + mutation_value[1])

        new_population.append(new_individual)

    population = new_population

# Find the best solution after optimization
best_weights = population[np.argmax(fitness_scores)]

print("Optimal weights for 'imdb_score' and 'Social_Media_Popularity' based on the genetic algorithm:", best_weights)

# Generate movie recommendations based on the optimal weights
imdb_weight, social_media_weight = best_weights
recommendations = data['imdb_score'] * imdb_weight + data['Social_Media_Popularity'] * social_media_weight

# Filter movies that involve the user-specified actor
actor_filter = data['actor_1_name'] == user_actor
top_recommendations = data[actor_filter][['movie_title', 'imdb_score', 'Social_Media_Popularity']].copy()
top_recommendations['Recommendation Score'] = recommendations

# Sort by the recommendation score in descending order
top_recommendations = top_recommendations.sort_values(by='Recommendation Score', ascending=False)

# Display the top recommended movies
top_recommendations = top_recommendations[['movie_title', 'Recommendation Score']].head(10)
print("Top Movie Recommendations for", user_actor)
print(top_recommendations)

"""## Based on Genre"""

import numpy as np
import random

# Ask the user for the specific genre they are interested in.
user_genre = input("Enter the genre for recommendations: ")

# Define your fitness function for the recommendation system.
def fitness_function(weights):
    imdb_weight, social_media_weight = weights

    # Filter movies that belong to the user-specified genre.
    genre_filter = data['Genre1'] == user_genre

    # Combine 'imdb_score' and 'Social_Media_Popularity' using the weights.
    recommendations = data[genre_filter]['imdb_score'] * imdb_weight + data[genre_filter]['Social_Media_Popularity'] * social_media_weight

    # Sort movies based on the recommendations.
    top_recommendations = data[genre_filter][['movie_title', 'imdb_score', 'Social_Media_Popularity']].copy()
    top_recommendations['Recommendation Score'] = recommendations

    # Sort by the recommendation score in descending order.
    top_recommendations = top_recommendations.sort_values(by='Recommendation Score', ascending=False)

    # Calculate the quality of recommendations (e.g., precision, recall, F1-score).
    # You can use any relevant metric for your task.

    # For simplicity, let's calculate the mean recommendation score.
    mean_recommendation_score = top_recommendations['Recommendation Score'].mean()

    # Return the mean recommendation score to maximize in the genetic algorithm.
    return mean_recommendation_score

# Define the genetic algorithm parameters.
population_size = 50
mutation_rate = 0.1
generations = 100

# Initialize the population with random weights.
population = [(np.random.uniform(0, 1), np.random.uniform(0, 1)) for _ in range(population_size)]

# Main loop for genetic algorithm.
for generation in range(generations):
    # Evaluate the fitness of each individual in the population.
    fitness_scores = [fitness_function(weights) for weights in population]

    # Select the top-performing individuals to become parents.
    parents = np.argsort(fitness_scores)[-population_size // 2:]

    # Create a new population through crossover and mutation.
    new_population = []

    for _ in range(population_size // 2):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        # Perform crossover to create a new individual (combine weights).
        crossover_point = random.randint(0, 1)
        new_individual = (population[parent1][0] if crossover_point == 0 else population[parent2][0],
                          population[parent1][1] if crossover_point == 1 else population[parent2][1])

        # Apply mutation with a certain probability (change weights).
        if random.random() < mutation_rate:
            mutation_value = (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))
            new_individual = (new_individual[0] + mutation_value[0], new_individual[1] + mutation_value[1])

        new_population.append(new_individual)

    population = new_population

# Find the best solution after optimization.
best_weights = population[np.argmax(fitness_scores)]

print(f"Optimal weights for 'imdb_score' and 'Social_Media_Popularity' based on the genetic algorithm for genre '{user_genre}': {best_weights}")

# Generate movie recommendations based on the optimal weights.
imdb_weight, social_media_weight = best_weights
recommendations = data['imdb_score'] * imdb_weight + data['Social_Media_Popularity'] * social_media_weight

# Filter movies that belong to the user-specified genre.
genre_filter = data['Genre1'] == user_genre
top_recommendations = data[genre_filter][['movie_title', 'imdb_score', 'Social_Media_Popularity']].copy()
top_recommendations['Recommendation Score'] = recommendations

# Sort by the recommendation score in descending order.
top_recommendations = top_recommendations.sort_values(by='Recommendation Score', ascending=False)

# Display the top recommended movies.
top_10_recommendations = top_recommendations[['movie_title', 'Recommendation Score']].head(10)
print(f"Top 10 Movie Recommendations for genre '{user_genre}':")
print(top_10_recommendations)