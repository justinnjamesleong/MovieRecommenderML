import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle

data = pd.read_csv("imdb10000data.csv")
data.rename(columns={'Unnamed: 0': 'movie_id'}, inplace=True)

columns = ['Cast', 'Director', 'Genre', 'Movie Name', 'Description']
data[columns] = data[columns].fillna('')

def get_features(data):
    imptfeatures=[]
    for i in range (0, data.shape[0]):
        mname = str(data['Movie Name'][i])
        d = str(data['Director'][i])
        g = str(data['Genre'][i])
        desc = str(data['Description'][i])
        c = str(data['Cast'][i])

        imptfeatures.append(mname + ' ' + d + ' ' + g + ' ' + desc + ' ' + c)
    return imptfeatures

data['imptfeatures'] = get_features(data)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['imptfeatures'])
tfidf_matrix.shape

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(data.index, index=data['Movie Name']).drop_duplicates()

def recommend(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    movie_ids = data['movie_id'].iloc[movie_indices]
    movie_names = data['Movie Name'].iloc[movie_indices]
    results = [{'title': movie_names.iloc[i], 'similarity': cosine_sim[idx, movie_indices[i]], 'id': str(movie_ids.iloc[i])} for i in range(len(movie_indices))]
    return results


# Save the cosine similarity matrix using pickle
with open('cosine_sim.pickle', 'wb') as f:
    pickle.dump(cosine_sim, f)



