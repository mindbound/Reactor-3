from globals import *

import life as lfe

import judgement
import movement
import groups
import speech
import action
import brain
import stats
import jobs

TIER = TIER_PASSIVE

def conditions(life, alife_seen, alife_not_seen, targets_seen, targets_not_seen, source_map):
	RETURN_VALUE = STATE_UNCHANGED
	
	return RETURN_SKIP

def tick(life, alife_seen, alife_not_seen, targets_seen, targets_not_seen, source_map):
	if not life['group']:
		if not stats.desires_to_create_group(life):
			return False
		
		_group_id = groups.create_group(life)
		_group = groups.get_group(_group_id)
		_pos = lfe.get_current_chunk(life)['pos']
		
		_j = jobs.create_job(life, 'Gather for group %s.' % _group_id,
	                         gist='create_group',
	                         description='Group %s: Looking for new members.' % _group_id,
	                         group=life['group'])
	
		jobs.add_task(_j, '0', 'find_target',
	                  action.make_small_script(function='find_target',
	                                           kwargs={'target': life['id'],
	                                                   'distance': 5}),
	                  player_action=action.make_small_script(function='can_see_target',
	                                           kwargs={'target_id': life['id']}),
	                  description='Find %s.' % ' '.join(life['name']),
	                  delete_on_finish=False)
		jobs.add_task(_j, '1', 'talk',
	                  action.make_small_script(function='start_dialog',
	                                           kwargs={'target': life['id'], 'gist': 'form_group'}),
	                  player_action=action.make_small_script(function='always'),
	                  description='Talk to %s.' % (' '.join(life['name'])),
	                  requires=['0'],
	                  delete_on_finish=False)
		
		groups.flag(_group_id, 'job_gather', _j)
		
		groups.announce(life, _group_id, 'job', 'New group gathering.', consider_motive=True, job_id=_j)
	
	if groups.is_leader(life['group'], life['id']):
		if stats.wants_to_abandon_group(life, life['group']):
			print 'ABANDONING ON THESE TERMS' * 10
			return False
		
		if life['state'] == 'idle' or lfe.is_in_shelter(life):
			groups.process_events(life['group'])
			#TODO: Re-announce group from time to time LOGICALLY
			if groups.get_group(life['group'])['claimed_motive'] == 'survival' and lfe.ticker(life, 'announce_group', 200):
				_job_id = groups.get_flag(life['group'], 'job_gather')
				groups.announce(life, life['group'], 'job', 'New group gathering.', consider_motive=True, job_id=_job_id)
			
			for member in groups.get_unwanted_members_with_perspective(life, life['group']):
				_j = jobs.create_job(life, 'Remove %s from group %s.' % (' '.join(LIFE[member]['name']), life['group']),
					                 gist='remove_member_from_group',
					                 description='Remove %s from group %s.' % (' '.join(LIFE[member]['name']), life['group']),
					                 group=life['group'],
					                 target=member)
				
				if _j:
					jobs.join_job(_j, life['id'])
			
			if len(groups.get_group(life['group'])['members'])<=3:
				_j = jobs.create_job(life, 'Meet with group %s.' % life['group'],
					                 gist='stay_with_group',
					                 description='Stay nearby group.',
					                 group=life['group'])
				
				if _j:
					groups.flag(life['group'], 'meet_with_group', _j)
					
					jobs.add_task(_j, '0', 'meet_with_group',
						          action.make_small_script(function='find_target',
						                                   kwargs={'target': life['id'],
						                                           'distance': 5,
						                                           'follow': False}),
					              player_action=action.make_small_script(function='can_see_target',
	                                           kwargs={'target_id': life['id']}),
						          description='Meet with group',
					              delete_on_finish=False)
					
					jobs.add_task(_j, '2', 'wait_for_number_of_group_members_in_chunk',
			              action.make_small_script(function='number_of_alife_in_chunk_matching',
			                                       kwargs={'amount': 3,
			                                               'chunk_key': lfe.get_current_chunk_id(life),
			                                               'matching': {'group': life['group']}}),
					      player_action=action.make_small_script(function='number_of_alife_in_chunk_matching',
			                                       kwargs={'amount': 3,
			                                               'chunk_key': lfe.get_current_chunk_id(life),
			                                               'matching': {'group': life['group']}}),
			              description='Wait until everyone arrives.')
				
				if lfe.ticker(life, 'meet_with_group', 30):
					_job_id = groups.get_flag(life['group'], 'meet_with_group')
					groups.announce(life, life['group'],
					                'job',
					                'We need everyone here.',
					                job_id=_job_id,
					                filter_if=[action.make_small_script(function='has_completed_job',
					                                                   kwargs={'job_id': _job_id})])
			else:
				print 'READY FOR MORE COMMANDS',len(groups.get_group(life['group'])['members'])
	