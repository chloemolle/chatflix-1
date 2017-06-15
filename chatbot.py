# coding: utf-8

from recommendation import Recommendation


class Bot(object):

    def __init__(self):
        self.recommendation = Recommendation()

    def respond_to(self, sender, message):
        # Enregistre l'utilisateur s'il n'existe pas déjà
        user = self.recommendation.register_user(sender)

        # Donne le message pour que l'utilisateur l'utilise
        user.give_message(message)

        # Si le chatbot doit faire une recommandation ou pas
        if user.should_make_recommendation():
            return self.recommendation.make_recommendation(user)
        else:
            intro = ""
            print("bon,bad, neutre")
            print(user.good_ratings)
            print(user.bad_ratings)
            print(user.neutral_ratings)
            # Si l'utilisateur parle pour la première fois, affiche un message d'intro
            if not user.has_been_asked_a_question():
                intro = "Bonjour ! Je vais vous poser des questions puis vous faire une recommandation.\n"

            else:
                if (message == "oui"):
                    user.answer_yes()
                elif (message == "non"):
                    user.answer_no()
                else:
                    user.answer_neutral()
            message = self.recommendation.ask_question(user)
            return intro + message
