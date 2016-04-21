from flask import Flask
from sqlalchemy import Enum

class DaysEnum(Enum):
	monday = "Monday"
	tuesday = "Tuesday"
	wednesday = "Wednesday"
	thursday = "Thursday"
	friday = "Friday"
	saturday = "Saturday"
	sunday = "Sunday"

class InterestsEnum(Enum):
	youth = "youth"
	seniors = "seniors"
	education ="education"
	environment = "environment"
	health = "health"
	arts = "arts"
	financialemp = "financialemp"
	veterans = "veterans"
	immigration = "immigration"
	animals = "animals"
	mentoring = "mentoring"
	homeless = "homeless"
	lgbt = "lgbt"
	domestic = "domestic"
	hunger = "hunger"
	disabilities = "disabilities"


class SkillsEnum(Enum):
	public = "public"
	teaching = "teaching"
	it = "it"
	administrative = "administrative"
	legal = "legal"
	coaching ="coaching"
	handiwork = "handiwork"
	arts = "arts"
	tefl = "tefl"
	writing = "writing"
	language = "language"
	event = "event"
	management = "management"
	sports = "sports"

class NeighborhoodsEnum(Enum):
	allston ="allston"
	backbay = "backbay"
	bayvillage = "bayvillage"
	beacon = "beaconhill"
	brighton = "brighton"
	charlestown = "charlestown"
	chinatown = "chinatown"
	dorchester = "dorchester"
	downtown = "downtown"
	eastboston = "eastboston"
	fenwaykenmore = "fenwaykenmore"
	hyde = "hyde"
	jamaica = "jamaica"
	mattapan = "mattapan"
	middorchester = "middorchester"
	missionshill = "missionhill"
	northend = "northend"
	roslindale = "roslindale"
	roxbury = "roxbury"
	southboston = "southboston"
	southend = "southend"
	westend = "westend"
	westroxbury = "westroxbury"
	greater = "greater"

class EducationEnum(Enum):
	lesshigh = "lesshigh"
	highschool = "highschool"
	somecoll = "somecoll"
	postsec = "postsec"
	associate = "associate"
	bachelor = "bachelor"
	master = "master"
	doctoral = "doctoral"


