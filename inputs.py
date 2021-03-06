from cStringIO import StringIO
from globals import *

from debug import *

import libtcodpy as tcod
import graphics as gfx

import scripting
import menus

import sys

def reset_input():
	for key in INPUT:
		INPUT[key] = False

def get_input():
	tcod.sys_check_for_event(tcod.EVENT_ANY, KEY, MOUSE)
	reset_input()
	get_keyboard_input()
	get_mouse_input()

def get_keyboard_input():
	global KEYBOARD_STRING
	
	if not KEY.vk:
		return False

	if KEY.c:
		_key = chr(KEY.c)
	else:
		if KEY.pressed:
			if KEY.vk == tcod.KEY_RIGHT:
				INPUT['right'] = True
			elif KEY.vk == tcod.KEY_LEFT:
				INPUT['left'] = True
			elif KEY.vk == tcod.KEY_DOWN:
				INPUT['down'] = True
			elif KEY.vk == tcod.KEY_UP:
				INPUT['up'] = True
		
		return True
	
	if SETTINGS['draw console']:
		if KEY.vk == tcod.KEY_ENTER and len(KEYBOARD_STRING[0]):
			#Taken from: http://stackoverflow.com/a/3906309
			old_stdout = sys.stdout
			redirected_output = sys.stdout = StringIO()
			exec(scripting.parse_console(KEYBOARD_STRING[0].rstrip()))
			sys.stdout = old_stdout
			
			gfx.log('>'+KEYBOARD_STRING[0].rstrip())
			gfx.log(' '+redirected_output.getvalue())
			
			KEYBOARD_STRING[0] = ''
			
		elif KEY.vk == tcod.KEY_BACKSPACE:
			KEYBOARD_STRING[0] = KEYBOARD_STRING[0][:len(KEYBOARD_STRING[0])-1]
	
	if not ACTIVE_MENU['menu'] == -1:
		_item = menus.is_getting_input(ACTIVE_MENU['menu'])
		if _item and KEY.pressed:
			_item['values'][0] += _key
	
	if not INPUT.has_key(_key):
		INPUT[_key] = False
	
	if not INPUT[_key] and KEY.pressed:
		if SETTINGS['draw console']:
			KEYBOARD_STRING[0] += _key
		
		INPUT[_key] = True
	else:
		#if INPUT[_key]:
		#	#TODO: A 'true' release...?
		#	pass
		
		INPUT[_key] = False

def set_mouse_click_callback(button, function):
	if button == 1:
		MOUSE_CALLBACKS['m1_click'] = function
	else:
		MOUSE_CALLBACKS['m2_click'] = function

def set_mouse_move_callback(function):
	MOUSE_CALLBACKS['move'] = function
	
def get_mouse_location():
	return CAMERA_POS[0]+MOUSE_POS[0], CAMERA_POS[1]+MOUSE_POS[1]

def get_mouse_input():
	#TODO: I can't get mouse input to work properly...
	_mouse = tcod.mouse_get_status()
	_old_x, _old_y = MOUSE_POS
	
	MOUSE_POS[0] = _mouse.cx
	MOUSE_POS[1] = _mouse.cy
	
	if not [_old_x, _old_y] == MOUSE_POS:
		if MOUSE_CALLBACKS['move']:
			MOUSE_CALLBACKS['move']()
	
	if not INPUT['m1'] and _mouse.lbutton_pressed:
		if MOUSE_CALLBACKS['m1_click']:
			MOUSE_CALLBACKS['m1_click']()
		
		INPUT['m1'] = True
	else:
		INPUT['m1'] = False
	
	if not INPUT['m2'] and _mouse.rbutton_pressed:
		if MOUSE_CALLBACKS['m2_click']:
			MOUSE_CALLBACKS['m2_click']()
		
		INPUT['m2'] = True
	else:
		INPUT['m2'] = False