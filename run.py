from app import create_app

# Create app by calling the application factory
app = create_app()

@app.route('/')
def home():
    return "Home page"


# Run the app
if __name__ == "__main__":
    app.run(debug=True)