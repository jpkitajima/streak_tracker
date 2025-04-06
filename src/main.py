from data.sqlite3_database_manager import DatabaseManager
from rest_server.flask_server import FlaskServer


sqlite3_database_manager = DatabaseManager()
flask_server = FlaskServer(sqlite3_database_manager)
flask_server.run(debug=True, host='0.0.0.0')
