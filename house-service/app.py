from server import create_app, db


app = create_app("prod")
with app.app_context():
    db.create_all()
    db.session.commit()
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082)