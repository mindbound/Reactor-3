#This tool was rushed together over the course of an hour or so. Be gentle.

from flask import Flask, render_template, request

import threading
import socket
import json

app = Flask(__name__)

def request(request, value=None):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(5)
	sock.connect(('', 3333))
	sock.sendall(json.dumps({'type': 'get', 'what': request, 'value': value}))
	data = json.loads(sock.recv(9048))
	sock.close()
	
	return data

@app.route('/life/<life_id>')
def life(life_id):
	life = request('life', value=int(life_id))
	life['know'] = life['know'].values()
	
	return render_template('life.html', life=life)

@app.route('/group/<group_id>')
def group(group_id):
	groups = request('groups')
	group = groups[group_id]
	
	return render_template('group.html', group_id=group_id, group=group)

@app.route('/')
def index():
	groups = request('groups')
	groups = groups.keys()
	groups.sort()
	
	return render_template('index.html', groups=groups)

if __name__ == '__main__':
	app.run(debug=True, port=3336)