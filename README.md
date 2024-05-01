# Movie Recommendation: A Genetic Algorithm Approach

## Overview 
This project implements a movie recommendation system using a genetic algorithm. The system recommends movies based on various criteria, such as actor, genre, IMDb score, and social media popularity. It utilizes a genetic algorithm to optimize the recommendation process and provide personalized suggestions to users.

## Features
- **Recommendation by Genre:** Users can receive movie recommendations based on their preferred genre.
- **Recommendation by Actor:** Users can get movie suggestions based on their favorite actors.
- **Recommendation by Popularity:** Movies are recommended based on IMDb score and social media popularity.
- **Customizable Optimization:** The genetic algorithm allows for the customization of weights for different recommendation factors.

## How it Works
1. *Data Preprocessing:* The system preprocesses a dataset containing information about movies, including genre, actors, IMDb score, and social media metrics.
2. *Genetic Algorithm Optimization:* The genetic algorithm optimizes the recommendation process by adjusting weights assigned to different recommendation factors.
3. *Recommendation Generation:* Based on user input (genre, actor, etc.) and the optimized weights, the system generates personalized movie recommendations.

## Installation
1. Clone the repository:
```
git clone https://github.com/yourusername/Genetic-Algorithm-Movie-Recommendation.git
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
5. Run the main script:
```
python movie_recommendation.py
```

## Usage
- Choose a recommendation method (genre, actor, or popularity) when prompted.
- Provide additional information such as genre name, actor name, or preference for IMDb score vs. social media popularity.
- Receive personalized movie recommendations based on your input.

## Credits
This project was developed by Sherin R Varghese. Special thanks to [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/data?select=movies_metadata.csv) for providing the movie dataset (movie_metadata.csv)


