from apps import app


@app.route('/')
def index():
    return 'A RESTful API to support CRUD operations to manage a shopping list.'


if __name__ == '__main__':
    app.run()
