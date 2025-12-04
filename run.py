from app import create_app
import os

# Create app by calling the application factory
app = create_app()

@app.route('/')
def home():
    return "Home page"


#Debug mode
debug_mode = os.environ.get('DEBUG_MODE', 'True') == 'True'

# Run the app
if __name__ == "__main__":
    app.run(debug=debug_mode)