from .models import Encounter

# These are just temporary view models that can be created purely for displaying data to user
# They are not persisted to the DB


class DashboardViewModel:
    num_encounters = 0

    num_prayers = 0
    num_testimonies = 0
    num_gospel_shares = 0

    num_red_lights = 0
    num_yellow_lights = 0
    num_green_lights = 0
    num_believer_wants_training = 0
    num_believer_rejects_training = 0

    percentage_red_lights = 0
    percentage_yellow_lights = 0
    percentage_green_lights = 0
    percentage_believer_wants_training = 0
    percentage_believer_rejects_training = 0


    def __init__(self, encounter: Encounter):
        print('do stuff here!')

    '''def get_percentage_of_red_lights()
    def get_percentage_of_yellow_lights()
    def get_percentage_of_green_lights()
    def get_percentage_of_believers_want_training()
    def get_percentage_of_believers_reject_training()'''
