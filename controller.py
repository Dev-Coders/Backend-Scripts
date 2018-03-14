from flask import Flask

app = Flask(__name__)

@app.route('/')
def working():
	return 'Welcome to Devcoder\'s Scripts.\nScript is Working..!'

if __name__ == '__main__':
	app.run(port=5000,use_reloader=True)