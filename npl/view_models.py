import datetime
from .models import Encounter
from . import utilities
from django.db import models

# These are just temporary view models that can be created purely for displaying data to user
# They are not persisted to the DB

NUM_WEEKS_TO_SHOW = 4

class EncounterPinViewModel:
    # todo: add laborer name here? helpful for team view?
    # laborer_name = ''
    response = ''
    name = ''
    full_address = ''
    date_time = ''
    actions = []
    lat = None
    lng = None

    def __init__(self, encounter: Encounter):
        # self.laborer_name = encounter.laborer.name
        self.response = encounter.response
        self.name = encounter.name
        self.full_address = utilities.smart_get_address_string(encounter)
        self.date_time = str(encounter.date_time)
        self.set_actions(encounter)
        self.lat = encounter.lat
        self.lng = encounter.lng

    def set_actions(self, encounter: Encounter):
        actions = []
        if encounter.action_prayer:
            actions.append('Prayer')
        if encounter.action_testimony:
            actions.append('Testimony')
        if encounter.action_gospel:
            actions.append('Gospel')

        self.actions = actions


class DashboardViewModel:
    num_encounters = 0

    num_encounters_by_week = [None] * NUM_WEEKS_TO_SHOW  # initialize a list with certain number of slots

    num_red_lights_by_week = [None] * NUM_WEEKS_TO_SHOW
    num_yellow_lights_by_week = [None] * NUM_WEEKS_TO_SHOW
    num_green_lights_by_week = [None] * NUM_WEEKS_TO_SHOW
    num_believer_wants_training_by_week = [None] * NUM_WEEKS_TO_SHOW
    num_believer_rejects_training_by_week = [None] * NUM_WEEKS_TO_SHOW

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

    def __init__(self, my_encounters: models.QuerySet, team_encounters=None):
        self.num_encounters = my_encounters.count()
        if self.num_encounters == 0:
            self.num_prayers = 0
            self.num_testimonies = 0
            self.num_gospel_shares = 0

            self.num_red_lights = 0
            self.num_yellow_lights = 0
            self.num_green_lights = 0
            self.num_believer_wants_training = 0
            self.num_believer_rejects_training = 0

            self.percentage_red_lights = 0
            self.percentage_yellow_lights = 0
            self.percentage_green_lights = 0
            self.percentage_believer_wants_training = 0
            self.percentage_believer_rejects_training = 0
            i = 0
            while i < NUM_WEEKS_TO_SHOW:
                self.num_encounters_by_week[i] = 0
                self.num_red_lights_by_week[i] = 0
        else:
            self.num_prayers = my_encounters.filter(action_prayer=True).count()
            self.num_testimonies = my_encounters.filter(action_testimony=True).count()
            self.num_gospel_shares = my_encounters.filter(action_gospel=True).count()

            self.num_red_lights = my_encounters.filter(response='RL').count()
            self.num_yellow_lights = my_encounters.filter(response='YL').count()
            self.num_green_lights = my_encounters.filter(response='GL').count()
            self.num_believer_wants_training = my_encounters.filter(response='WT').count()
            self.num_believer_rejects_training = my_encounters.filter(response='RT').count()

            self.percentage_red_lights = self.num_red_lights / self.num_encounters
            self.percentage_yellow_lights = self.num_yellow_lights / self.num_encounters
            self.percentage_green_lights = self.num_green_lights / self.num_encounters
            self.percentage_believer_wants_training = self.num_believer_wants_training / self.num_encounters
            self.percentage_believer_rejects_training = self.num_believer_rejects_training / self.num_encounters

            i = 0
            starting_week_number = datetime.datetime.now().isocalendar()[1] - NUM_WEEKS_TO_SHOW + 1
            while i < NUM_WEEKS_TO_SHOW:
                self.num_encounters_by_week[i] = my_encounters.filter(date_time__week=(starting_week_number+i)).count()
                self.num_red_lights_by_week[i] = my_encounters.filter(response='RL', date_time__week=(starting_week_number+i)).count()
                i += 1


    '''def get_percentage_of_red_lights()
    def get_percentage_of_yellow_lights()
    def get_percentage_of_green_lights()
    def get_percentage_of_believers_want_training()
    def get_percentage_of_believers_reject_training()'''
