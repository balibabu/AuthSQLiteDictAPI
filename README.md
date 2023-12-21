# AuthSQLiteDictAPI


## Description

A Django project that utilizes the sqlitedict library, incorporates user authorization, and offers API endpoints for performing operations on a SQLite-backed dictionary.

## Features

- **SQLite-backed Dictionary:** Utilizes the sqlitedict library to manage data persistence.
- **User Authentication:** Implements user authentication for secure access to the API.
- **API Endpoints:** Provides endpoints for performing various operations on the SQLite-backed dictionary.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/balibabu/AuthSQLiteDictAPI.git
   cd AuthSQLiteDictAPI
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the Django admin interface at `http://localhost:8000/admin/` and log in with the superuser credentials.

2. Use the provided API endpoints for dictionary operations:

   - Endpoint 1
   - Endpoint 2
   - ...

## API Documentation

- **Endpoint 1:**
  - Description: 
  - Method: 
  - Path: 

- **Endpoint 2:**
  - Description: 
  - Method: 
  - Path: 

...

## Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new pull request

## License

This project is licensed under the [MIT License](LICENSE).
