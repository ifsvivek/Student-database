# Student Database

A simple Flask application to manage a student database.

## Setup and Installation

1. Clone the repository:

```sh
git clone https://github.com/ifsvivek/Student-database.git
```

2. Navigate to the project directory:

```sh
cd Student-database
```

3. Create a virtual environment:

```sh
python -m venv env
```

4. Activate the virtual environment:

```sh
env\Scripts\activate
```

5. Install the required dependencies:

```sh
pip install -r requirements.txt
```

6. Create a `.env` file in the project root directory with the following content:

```sh
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=student_db
```

7. Run the application:

```sh
python app.py
```

The application will be accessible at [`http://localhost:8000`](http://localhost:8000).

## File Structure

-   `app.py`: This is the main application file where the Flask application is defined and routes are set up.
-   `functions.py`: This file contains functions for interacting with the MySQL database.
-   `templates/index.html`: This is the HTML template for the form and table.
-   `requirements.txt`: This file lists the Python dependencies of the project.
-   `.gitignore`: This file specifies the files and directories that should be ignored by Git.

## Dependencies

-   Flask: A lightweight web application framework for Python.
-   mysql-connector-python: A driver for communicating with MySQL servers from Python.
-   python-dotenv: A module that allows you to specify environment variables in a .env file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](/LICENSE)
