from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib import const, aspects
from datetime import datetime, timezone

ASPECT_LABELS = {0: 'conjunction', 60: 'sextile', 90: 'square', 120: 'trine', 180: 'opposition'}
LIST_PLANETS = const.LIST_SEVEN_PLANETS + [const.URANUS, const.NEPTUNE, const.PLUTO, const.ASC]


class Person:
    """Wrapper for API query input, person and birth info"""

    def __init__(self, name, birthdate, birth_lat, birth_lon, birth_utc_offset):
        self.name = name
        self.birthdate = birthdate
        self.birth_lat = birth_lat
        self.birth_lon = birth_lon
        self.birth_utc_offset = birth_utc_offset

    def birth_date_str(self):
        return "{:%Y/%m/%d}".format(self.birthdate)

    def birth_time_str(self):
        return "{:%H:%M}".format(self.birthdate)

    def __repr__(self):
        return "<Person {} Born {:%y-%m-%d}>".format(self.name, self.birthdate)

    def __eq__(self, other):
        return self.name == other.name and self.birthdate == other.birthdate

    def __hash__(self):
        return hash("{}_{}".format(self.name, self.birthdate.timestamp()))


class NatalChart:
    """Calculator and wrapper for results of natal charts, per Person"""

    def __init__(self, person):
        self.planets = {}
        self.houses = {}
        self.person = person

        self.date = Datetime(person.birth_date_str(), person.birth_time_str(), person.birth_utc_offset)
        self.pos = GeoPos(person.birth_lat, person.birth_lon)
        self.chart = Chart(self.date, self.pos, IDs=const.LIST_OBJECTS, hsys=const.HOUSES_PLACIDUS)

        for body in LIST_PLANETS:
            self.planets[body] = NatalPlanet(self.chart, body)

        for house in const.LIST_HOUSES:
            self.houses[house] = NatalHouse(self.chart, house)


class NatalPlanet:
    """Positioning for planets"""

    def __init__(self, chart, body):
        self.planet = chart.get(body)
        self.house = chart.houses.getObjectHouse(self.planet).id
        self.aspects = []
        self.name = body if body != 'Asc' else 'Ascendant'

        for house_id in const.LIST_HOUSES:
            house = chart.get(house_id)
            if house.sign == self.planet.sign:
                self.house = house_id
            break

        for other_body in LIST_PLANETS:
            other_planet = chart.get(other_body)
            aspect = aspects.getAspect(self.planet, other_planet, const.MAJOR_ASPECTS)
            if aspect.type != -1:
                aspect_part = aspect.active if aspect.active.id != body else aspect.passive
            if aspect_part.id not in LIST_PLANETS:
                # don't care about Lilith and nodes
                continue
            if aspect.orb > 10:
                # maybe #TODO: use different values per type?
                continue
            self.aspects.append({
                'first': self.name, 'second': aspect_part.id,
                'type': aspect.type, 'type_name': ASPECT_LABELS[aspect.type],
                'orb': aspect.orb
            })

    def to_dict(self):
        obj = {
            'planet': self.planet.__dict__,
            'house': self.house,
        }
        if self.aspects:
            obj['aspects'] = [x for x in self.aspects]
        return obj

    def __repr__(self):
        return "<Natal Planet {} in {}>".format(self.planet, self.house)


class NatalHouse:
    """Whose who for the houses at moment of birth"""

    def __init__(self, chart, body):
        self.house = chart.get(body)

    def to_dict(self):
        return self.house.__dict__

    def __repr__(self):
        return "<Natal House {}>".format(self.house)


if __name__ == "__main__":
    birth_year = 2005
    birth_month = 3
    birth_day = 12
    birth_hour = 12
    birth_min = 0
    birthdate = datetime(birth_year, birth_month, birth_day, birth_hour, birth_min, 0, tzinfo=timezone.utc)

    birth_lat = 55.797440
    birth_lon = 37.580249
    birth_utc_offset = "+03:00"

    person = Person(
        name="Viktor",
        birthdate=birthdate,
        birth_lat=birth_lat,
        birth_lon=birth_lon,
        birth_utc_offset=birth_utc_offset
    )

    date = Datetime(person.birth_date_str(), person.birth_time_str(), person.birth_utc_offset)
    pos = GeoPos(person.birth_lat, person.birth_lon)
    chart = Chart(date, pos, IDs=const.LIST_OBJECTS, hsys=const.HOUSES_PLACIDUS)
    keys = chart.objects.content.keys()
    d = {}
    for key in keys:
        f = chart.objects.content[key].__dict__
        d[key] = [f["sign"], f["signlon"]]

    print(d)
