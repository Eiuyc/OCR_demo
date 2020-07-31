from flask import Flask, render_template, request
import os
import json
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		f = request.files['file']
		if not os.path.exists('static/tmp'): os.mkdir('static/tmp')
		img_path = f'static/tmp/{f.filename}'
		f.save(img_path)
		os.system(f'python cmd_test.py {img_path}')
		with open('static/tmp/result.txt','r', encoding='utf-8') as f:
			result = json.loads(f.read())
		return render_template('result.html', rst=result, f=img_path, head='OCR demo')
	return render_template('index.html', head='OCR demo')
app.run(host='127.0.0.1', port='80')
