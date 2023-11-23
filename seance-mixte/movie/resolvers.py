import json
import uuid

# Lecture des données
with open('{}/data/movies.json'.format("."), "r") as file:
    movies = json.load(file)['movies']

with open('{}/data/actors.json'.format("."), "r") as file:
    actors = json.load(file)['actors']


def save_movies():
    """
    Save movies in json file

    :return: None
    """
    with open('{}/data/movies.json'.format("."), "w") as movies_file:
        json.dump({"movies": movies}, movies_file)


def save_actors():
    """
    Save actors in json file

    :return:  None
    """
    with open('{}/data/actors.json'.format("."), "w") as actors_file:
        json.dump({"actors": actors}, actors_file)


#################### Fonctions de résolution ####################
def movie_with_id(_, info, _id):
    """
    Retrieve a movie by its id

    Parameters
    ----------
    :param _: unused
    :param info: unused
    :param _id: id of the movie to retrieve

    :return: the movie with the given id
    """
    for movie in movies:
        if movie['id'] == _id:
            return movie


def movie_with_title(_, info, title):
    """
    Retrieve a movie by its title

    Parameters
    ----------
    :param _: unused
    :param info: unused
    :param title: title of the movie to retrieve

    :return: the movie with the given title
    """
    for movie in movies:
        if movie['title'] == title:
            return movie


def all_movies(_, info) -> list:
    """
    Retrieve all movies in the database

    Parameters
    ----------
    :param _: unused
    :param info: unused
    :return:
    """
    return movies


def add_movie(_, info, title, director, rating):
    """
    Add a movie to the database

    Parameters
    ----------
    :param _:
    :param info:
    :param title:
    :param director:
    :param rating:
    :return:
    """
    # check if all fields are filled
    if not title or not director or not rating:
        return False

    # check if movie already exists
    if movie_with_title(_, info, title):
        return False

    movie = {
        "id": str(uuid.uuid4()),
        "title": title,
        "director": director,
        "rating": rating
    }

    movies.append(movie)

    save_movies()

    return movie


def add_actor(_, info, firstname, lastname, birthday):
    """
    Add an actor to the database

    Parameters
    ----------
    :param _:
    :param info:
    :param firstname:
    :param lastname:
    :param birthday:
    :return:
    """
    if not firstname or not lastname or not birthday:
        return False

    actors.append({
        "id": str(uuid.uuid4()),
        "firstname": firstname,
        "lastname": lastname,
        "birthday": birthday,
        "films": []
    })

    save_actors()

    return True


def add_movie_to_actor(_, info, actor_id, movie_id):
    """
    Add a movie to an actor's filmography

    Parameters
    ----------
    :param _:
    :param info:
    :param actor_id:
    :param movie_id:
    :return:
    """
    for actor in actors:
        if actor['id'] == actor_id:
            # check if movie is already in list
            if movie_id not in actor['films']:
                actor['films'].append(movie_id)
                save_actors()
                return True
    return False


def remove_movie_from_actor(_, info, actor_id, movie_id):
    """
    Remove a movie from an actor's filmography

    Parameters
    ----------
    :param _:
    :param info:
    :param actor_id:
    :param movie_id:
    :return:
    """
    for actor in actors:
        if actor['id'] == actor_id:
            # check if movie is already in list
            if movie_id in actor['films']:
                actor['films'].remove(movie_id)
                save_actors()
                return True
    return False


def resolve_actors_in_movie(movie, info):
    """
    Retrieve all actors playing in a movie

    Parameters
    ----------
    :param movie:
    :param info:
    :return:
    """
    actors_in_movie = []
    for actor in actors:
        if movie['id'] in actor['films']:
            actors_in_movie.append(actor)
    return actors_in_movie


def delete_actor(_, info, _id):
    """
    Delete an actor from the database

    Parameters
    ----------
    :param _:
    :param info:
    :param _id:
    :return:
    """
    for actor in actors:
        if actor["id"] == _id:
            actors.remove(actor)

            save_actors()

            return True

    return False


def delete_movie(_, info, _id):
    """
    Delete a movie from the database

    Parameters
    ----------
    :param _:
    :param info:
    :param _id:
    :return:
    """
    for movie in movies:
        if movie["id"] == _id:
            movies.remove(movie)

            for actor in actors:
                if _id in actor['films']:
                    actor['films'].remove(_id)

            save_actors()

            save_movies()

            return True

    return False


def update_movie(_, info, _id, title, director, rating):
    """
    Update a movie in the database

    Parameters
    ----------
    :param _:
    :param info:
    :param _id:
    :param title:
    :param director:
    :param rating:
    :return:
    """
    for movie in movies:
        if movie["id"] == _id:
            movie["title"] = title if title else movie["title"]
            movie["director"] = director if director else movie["director"]
            movie["rating"] = rating if rating else movie["rating"]

            save_movies()

            return movie

    return False
