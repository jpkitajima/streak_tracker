from flask import Flask, request, jsonify, render_template
from data.database_manager import DatabaseManager

app = Flask(__name__)

# Sample data
data = []

db = DatabaseManager()

@app.route('/', methods=['GET'])
def get_data():
    streaks = db.get_activity_streaks()
    return render_template('ui.html', streaks=streaks)

@app.route('/', methods=['POST'])
def add_data():
    new_data = request.json
    print(new_data)
    new_activity= new_data.get('newActivity')
    if new_activity:
        db.add_streak(new_activity, False)
    checkboxes = new_data.get('checkboxes', {})
    for key, value in checkboxes.items():
        db.add_streak(key, value)
    data.append(new_data)
    return jsonify(new_data), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')