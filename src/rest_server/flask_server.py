from flask import Flask, request, jsonify, render_template
from interfaces.databse_manager import DatabaseManagerInterface


class FlaskServer:
    def __init__(self, db_manager: DatabaseManagerInterface):
        self.app = Flask(__name__)
        self.db = db_manager

        self._setup_routes()

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def _setup_routes(self):
        @self.app.route('/', methods=['GET'])
        def get_data():
            streaks = self.db.get_activity_streaks()
            return render_template('ui.html', streaks=streaks)

        @self.app.route('/', methods=['POST'])
        def add_data():
            new_data = request.json

            new_activity = new_data.get('newActivity')
            checkboxes = new_data.get('checkboxes', {})

            if new_activity:
                self.db.add_streak(new_activity, False)

            for key, value in checkboxes.items():
                self.db.add_streak(key, value)

            return jsonify(new_data), 201
