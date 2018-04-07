import geocoder
from .models import Encounter


def smart_get_address_string(encounter: Encounter):
    address_dict = dict()

    def _clean_component(param_name):
        val = getattr(encounter, param_name)
        if val is None:
            return ''
        else:
            return str(val).strip()

    def _get_parameters(input_parameters, joiner, address_so_far=None):
        values = [_clean_component(param) for param in input_parameters if _clean_component(param)]

        if address_so_far is None or address_so_far.strip() == '':
            return joiner.join(values)
        else:
            values.insert(0, address_so_far)
            return joiner.join(values)

    address_dict["address"] = _get_parameters(["street_address_number", "street_address_name", "apt_or_unit"], " ")
    address_dict["address_city_state"] = _get_parameters(["city", "state"], ", ",
                                                         address_so_far=address_dict["address"])

    return _get_parameters(["zip"], " ", address_so_far=address_dict["address_city_state"])


def get_lat_lng_from_address(encounter: Encounter) -> (float, float):
    if encounter.city is not None and encounter.state is not None:
        g = geocoder.google(smart_get_address_string(encounter))
        return g.lat, g.lng
    else:
        return None, None


# todo: keep this in sync somehow with the Encounter Model
def get_response_description(abbrev):
    MINISTRY_RESPONSES = {'RL': 'Red Light',
                          'YL': 'Yellow Light', 'GL': 'Green Light',
                          'WT': 'Believer Wants Training',
                          'RT': 'Believer Rejects Training'}
    return MINISTRY_RESPONSES.get(abbrev)

