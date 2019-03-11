from app import app

if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'L3jqZCvayMe1njN4nFB9'

    app.run(debug=True)
