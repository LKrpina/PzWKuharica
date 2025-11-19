from app import create_app

app = create_app()

@app.before_request
def test_mongo_connection():
    try:
        from app.extensions import mongo
        mongo.db.command('ping')
        print("✅ MongoDB Atlas connection successful!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)