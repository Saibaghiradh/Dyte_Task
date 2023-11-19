from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        query_params = request.form.to_dict()
        filters = {key: query_params[key] for key in query_params if query_params[key]}

        # Sample Queries
        if 'query' in query_params:
            if query_params['query'] == 'error_logs':
                filters['level'] = 'error'
            elif query_params['query'] == 'connect_failure_logs':
                filters['message'] = 'Failed to connect'
            elif query_params['query'] == 'resource_logs':
                filters['resourceId'] = 'server-1234'
            elif query_params['query'] == 'timestamp_range_logs':
                start_time = datetime.strptime('2023-09-10T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
                end_time = datetime.strptime('2023-09-15T23:59:59Z', '%Y-%m-%dT%H:%M:%SZ')
                filters['timestamp'] = (start_time, end_time)

        # Build the query based on filters
        query = Log.query.filter_by(**filters)

        # Execute the query and retrieve results
        results = query.all()

        return render_template('results.html', results=results)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)
