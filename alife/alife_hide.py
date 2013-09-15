#This is intended to be an example of how the new ALife
#system works.
from globals import *

import life as lfe

import judgement
import movement
import brain

import logging

STATE = 'hiding'
TIER = TIER_COMBAT-.2

def conditions(life, alife_seen, alife_not_seen, targets_seen, targets_not_seen, source_map):
	RETURN_VALUE = STATE_UNCHANGED
	
	if judgement.is_safe(life):
		return False
	
	if not judgement.get_visible_threats(life):
		if life['state'] == STATE:
			lfe.clear_actions(life)
			
		return False
	
	if not life['state'] == STATE:
		RETURN_VALUE = STATE_CHANGE
	
	return RETURN_VALUE

def tick(life, alife_seen, alife_not_seen, targets_seen, targets_not_seen, source_map):
	_threat = judgement.get_nearest_threat(life)
	_knows = brain.knows_alife_by_id(life, _threat)
	movement.escape(life, _knows['life']['id'])
