from flask import Flask
from app.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

with app.app_context():
    print("🔥 Registered Routes in Flask:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint} --> {rule.methods} --> {rule.rule}")

if __name__ == "__main__":
    print("🚀 Flask app is running on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
