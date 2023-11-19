from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(50))
    message = db.Column(db.String(255))
    resourceId = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    traceId = db.Column(db.String(50))
    spanId = db.Column(db.String(50))
    commit = db.Column(db.String(50))
    parentResourceId = db.Column(db.String(50))

    def __init__(self, **kwargs):
        kwargs['timestamp'] = datetime.strptime(kwargs['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        super().__init__(**kwargs)

@app.route('/ingest', methods=['POST'])
def ingest():
    try:
        data = request.get_json()
        # Process and save the log data to the database
        new_log = Log(**data)
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(port=3000)
