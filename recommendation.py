# coding: utf-8

from User import User
from random import randint

import numpy as np
from sklearn.cluster import KMeans
import operator

from movielens import load_movies, load_simplified_ratings


class Recommendation:

    def __init__(self):

        # Importe la liste des films
        # Dans la variable 'movies' se trouve la correspondance entre l'identifiant d'un film et le film
        # Dans la variables 'movies_list' se trouve les films populaires qui sont vus par les utilisateurs
        self.movies = load_movies()
        self.movies_list = []

        # Importe la liste des notations
        # Dans le tableau 'ratings' se trouve un objet avec un attribut 'movie' contenant l'identifiant du film, un
        # attribut 'user' avec l'identifiant de l'utilisateur et un attribut 'is_appreciated' pour savoir si oui ou non
        # l'utilisateur aime le film
        self.ratings = load_simplified_ratings()

        # Les utilisateurs du fichier 'ratings-popular-simplified.csv' sont stockés dans 'test_users'
        self.test_users = {}
        # Les utilisateurs du chatbot facebook seront stockés dans 'users'
        self.users = {}

        # Lance le traitement des notations
        self.process_ratings_to_users()

    # Traite les notations
    # Crée un utilisateur de test pour chaque utilisateur dans le fichier
    # Puis lui attribue ses films aimés et détestés
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            if rating.is_appreciated is not None:
                if rating.is_appreciated:
                    user.good_ratings.append(rating.movie)
                else:
                    user.bad_ratings.append(rating.movie)
            elif rating.score is not None:
                user.ratings.append(rating)
            self.movies_list.append(rating.movie)

    # Enregistre un utilisateur de test s'il n'existe pas déjà et le retourne
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Enregistre un utilisateur s'il n'existe pas déjà et le retourne
    def register_user(self, sender):
        if sender not in self.users.keys():
            self.users[sender] = User(sender)
        return self.users[sender]

    # Retourne les films aimés par un utilisateur
    def get_movies_from_user(self, user):
        movies_list = []
        good_movies = user.good_ratings
        for movie_number in good_movies:
            movies_list.append(self.movies[movie_number].title)
        return movies_list


    # Calcule la similarité entre un utilisateur et tous les utilisateurs de tests
    def compute_all_similarities(self, user):
        user_similarities = {}
        for us, value in self.users.items():
            if value is not user:
                user_similarities[us] = self.get_similarity(user,value)
        return user_similarities


    # Affiche la recommandation pour l'utilisateur
    def make_recommendation(self, user):
        tab_recup = self.compute_all_similarities(user)
        tab_trie = sorted(tab_recup.items(),key = operator.itemgetter(1))
        print(tab_trie)
        return "Vous n'avez pas de recommandation pour le moment."

    # Pose une question à l'utilisateur
    def ask_question(self, user):
        i = randint(0,len(self.movies_list)-1)
        user.set_question(self.movies[i].id)
        return("As tu aimé " + self.movies[i].title)

    # Calcule la similarité entre 2 utilisateurs
    #c'est user_a qui calcule sa similarité avec user_b
    @staticmethod
    def get_similarity(user_a, user_b):
        s = set(user_a.good_ratings + user_a.bad_ratings + user_a.neutral_ratings + user_b.good_ratings + user_b.bad_ratings + user_b.neutral_ratings)
        ratings = 0
        for elmt in set:
            scoreA = get_score(user_a,elmt)
            scoreB = get_score(user_b,elmt)
            ratings += scoreA* scoreB
        return ratings/user_a.get_norm()

    def get_score(user,elmt):
        if elmt in user.good_ratings:
            return(1)
        elif elmt in user.bad_ratings:
            return(-1)
        else:
            return(0)
