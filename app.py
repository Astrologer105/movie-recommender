import pandas as pd
import streamlit as slt
import pickle
import pandas
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f3aeefbaf85be6ab830905671af10d09&language=en-US'.format(movie_id))
    data=response.json()
    return 'https://image.tmdb.org/t/p/w500'+data['poster_path']

def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id = df.iloc[i[0]].id
        recommended_movies.append(df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

slt.title('Movie Recommender System')

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity= pickle.load(open('similarity.pkl','rb'))
df = pd.DataFrame(movies_dict)

movie_selected= slt.selectbox(
    'Please Select Movie:-',
    (df['title'].values))

if slt.button('Recommend'):
    names,posters = recommend(movie_selected)
    col1, col2, col3, col4, col5= slt.columns(5)
    col=[col1,col2,col3,col4,col5]
    for i in range(5):
        with col[i]:
            slt.text(names[i])
            slt.image(posters[i])



