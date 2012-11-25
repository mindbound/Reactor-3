from globals import *
import graphics as gfx
import logging
import json

def load_item(item):
	with open(os.path.join(ITEM_DIR,item+'.json'),'r') as e:
		return json.loads(''.join(e.readlines()))

def initiate_item(name):
	if name in ITEM_TYPES:
		logging.warning('Item type \'%s\' is already loaded. Reloading...' % name)
	
	item = load_item(name)
	
	if not 'icon' in item:
		logging.warning('No icon set for item type \'%s\'. Using default (%s).' % (name,DEFAULT_ITEM_ICON))
		item['tile'] = DEFAULT_ITEM_ICON
	
	if not 'flags' in item:
		logging.error('No flags set for item type \'%s\'. Errors may occur.' % name)
	
	if 'attaches_to' in item:
		item['attaches_to'] = item['attaches_to'].split('|')
	
	#Unicode isn't handled all that well on Windows for some reason...
	for key in item:
		if isinstance(item[key],unicode):
			item[key] = str(item[key])
	
	ITEM_TYPES[item['name']] = item
	
	return item

def create_item(name,position=[0,0,0]):
	item = ITEM_TYPES[name].copy()
	
	item['pos'] = list(position)
	
	ITEMS.append(item)
	
	return item

def get_items_at(position):
	_items = []
	
	for item in ITEMS:
		if item.has_key('id'):
			continue
		
		if item['pos'] == position:
			_items.append(item)
	
	return _items

def draw_items():
	for item in ITEMS:
		if item.has_key('id'):
			continue
		
		if not item['pos'][2] <= CAMERA_POS[2]:
			continue
		
		if item['pos'][0] >= CAMERA_POS[0] and item['pos'][0] < CAMERA_POS[0]+MAP_WINDOW_SIZE[0] and\
			item['pos'][1] >= CAMERA_POS[1] and item['pos'][1] < CAMERA_POS[1]+MAP_WINDOW_SIZE[1]:
			_x = item['pos'][0] - CAMERA_POS[0]
			_y = item['pos'][1] - CAMERA_POS[1]
			gfx.blit_char(_x,_y,item['icon'],white,None)