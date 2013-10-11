from globals import *

import situations
import zones
import alife
import items
import life

def suicide():
	life.kill(LIFE[SETTINGS['controlling']], 'suicide')

def kill(life_id):
	life.kill(LIFE[life_id], 'suicide')

def make_hungry(life_id):
	LIFE[life_id]['hunger'] = 500
	
def world_hunger():
	for l in LIFE.values():
		l['hunger'] = 500

def make_thirsty(life_id):
	LIFE[life_id]['thirst'] = 500

def simple_lights():
	SETTINGS['draw light'] = False

def love_me():
	for target in LIFE[SETTINGS['controlling']]['know']:
		alife.brain.add_impression(LIFE[target], LIFE[SETTINGS['controlling']]['id'], 'follow', {'influence': 100})

def time(time):
	WORLD_INFO['real_time_of_day'] = time

def timescale(scale):
	WORLD_INFO['time_scale'] = scale

def warp(x, y):
	LIFE[SETTINGS['controlling']]['pos'][0] = x
	LIFE[SETTINGS['controlling']]['pos'][1] = y

def camps():
	alife.camps.debug_camps()

def food():
	items.create_item('corn', position=LIFE[SETTINGS['controlling']]['pos'])

def drink():
	items.create_item('soda', position=LIFE[SETTINGS['controlling']]['pos'])

def give(item):
	items.create_item(item, position=LIFE[SETTINGS['controlling']]['pos'])

def drop():
	situations.drop_cache(['soda', 'corn'])

def toss():
	life.push(LIFE[SETTINGS['controlling']], 0, 2)