import json
import uuid


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def movie_with_title(_, info, title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == title:
                return movie


def all_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies['movies']


def add_movie(_, info, title, director, rating, actors):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)

        movie = {
            "id": str(uuid.uuid4()),
            "title": title,
            "director": director,
            "rating": rating,
            "actors": actors
        }
        movies['movies'].append(movie)

        # Lire la liste des acteurs et rajouter le film dans la liste des films de chaque acteur
        with open('{}/data/actors.json'.format("."), "r") as file:
            data = json.load(file)
            for actor in data['actors']:
                if actor['id'] in actors and movie['id'] not in actor['films']:
                    actor['films'].append(movie['id'])

        with open('{}/data/movies.json'.format("."), "w") as file:
            json.dump(movies, file)
        return movie


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        print(actors)
        return actors


def delete_movie(_, info, _id):
    try:
        with open('{}/data/movies.json'.format("."), "r") as movie_file:
            movies = json.load(movie_file)
            for movie in movies['movies']:
                if movie['id'] == _id:
                    movies['movies'].remove(movie)
                    break
            else:
                return False
            with open('{}/data/movies.json'.format("."), "w") as actors_file:
                json.dump(movies, actors_file)
            return True
    except OSError as e:
        print("Error: %s : %s" % ("data/movies.json", e.strerror))
        return False


def rate_of_movie(_, info, _id, rating):
    try:
        with open('{}/data/movies.json'.format("."), "r") as movie_file:
            movies = json.load(movie_file)
            for movie in movies['movies']:
                if movie['id'] == _id:
                    movie['rating'] = rating
                    break
            else:
                return False
            with open('{}/data/movies.json'.format("."), "w") as actors_file:
                json.dump(movies, actors_file)
            return True
    except OSError as e:
        print("Error: %s : %s" % ("data/movies.json", e.strerror))
        return False
