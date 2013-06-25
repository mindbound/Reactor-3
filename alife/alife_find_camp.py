from globals import *

import life as lfe

import references
import judgement
import brain
import camps
import stats
import maps

import logging
import random

STATE = 'finding camp'

def conditions(life, alife_seen, alife_not_seen, targets_seen, targets_not_seen, source_map):
	RETURN_VALUE = STATE_UNCHANGED
	
	if not 'INTELLIGENT' in life['life_flags']:
		return False
	
	if not judgement.is_safe(life):
		return False
	
	if not life['state'] == STATE:
		RETURN_VALUE = STATE_CHANGE
	
	if stats.desires_to_create_camp(life):
		_unfounded_camp = camps.find_best_unfounded_camp(life)
		
		if _unfounded_camp['score'] >= stats.get_minimum_camp_score(life):
			#brain.store_in_memory(life, 'explore_camp', _unfounded_camp['camp'])
			print 'YO!!!! LETS CAMP, DUDE!'
			return RETURN_VALUE
		elif _unfounded_camp['camp']:
			brain.store_in_memory(life, 'explore_camp', _unfounded_camp['camp'])
			print 'only interested'
			return RETURN_VALUE
	
	return False

def tick(life, alife_seen, alife_not_seen, targets_seen, targets_not_seen, source_map):
	_to_explore = brain.retrieve_from_memory(life, 'explore_camp')
	if _to_explore:
		print 'LOOKING AT CAMP'
		_closest_key =  references.find_nearest_key_in_reference(life, _to_explore, ignore_current=True)
		_chunk = maps.get_chunk(_closest_key)
		
		lfe.clear_actions(life)
		lfe.add_action(life,{'action': 'move',
	     	'to': random.choice(_chunk['ground'])}, 200)
		return True
	
	_best_camp = camps.find_best_unfounded_camp(life)['camp']
	print 'lets camp ;)'
	
	if not _best_camp:
		return False
	
	camps.found_camp(life, _best_camp, announce=True)
