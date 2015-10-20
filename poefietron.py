
# http://stackoverflow.com/questions/12232304/how-to-implement-server-push-in-flask-framework

import flask
from anypubsub import create_pubsub

app = flask.Flask(__name__)
pubsub = create_pubsub('memory')
messages = []

@app.route('/')
def root():
    return flask.render_template('index.html', messages=messages)

@app.route('/static/<path:path>')
def statics(path):
    return flask.render_static_file(path)

def event_stream():
    sub = pubsub.subscribe('chat')
    for message in sub:
        yield 'data: {}\n\n'.format(message)

@app.route('/stream')
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route('/post', methods=['POST'])
def post():
    message = flask.request.form['message']
    pubsub.publish('chat', message)
    messages.insert(0, message)
    return "OK"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)

