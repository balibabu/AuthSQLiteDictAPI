# AuthSQLiteDictAPI

## Description

A Django project that utilizes the `sqlitedict` library, incorporates user authorization, and offers API endpoints for performing operations on a SQLite-backed dictionary.

## Features

- **SQLite-backed Dictionary:** Utilizes the `sqlitedict` library to manage data persistence.
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

   - **Login:**
     - Description: If already a user then login and get a token for future HTTP requests
     - Method: POST
     - Path: http://localhost:8000/user/login/

   - **Register:**
     - Description: Register as a new user
     - Method: POST
     - Path: http://localhost:8000/user/register/

   - **Logout:**
     - Description: Logout and invalidate the authentication token
     - Method: POST
     - Path: http://localhost:8000/user/logout/

   - **Simple SQLite:**
     - Description: Perform simple operations on the SQLite-backed dictionary
     - Method: POST
     - Path: http://localhost:8000/sql/

   - **SQLiteDict:**
     - Description: Access and modify the SQLite-backed dictionary
     - Method: POST
     - Path: http://localhost:8000/sql/dict/

   - **Permission Control:**
     - Description: Manage user permissions for dictionary operations
     - Method: POST
     - Path: http://localhost:8000/sql/permit/
Your custom JSON format explanations look good for the most part, but I suggest making a few improvements for clarity and consistency:

## Custom Format For Endpoints SQLiteDict and Permission Control

*These are full format with all fields; for any operation, provide only the required fields.*

### SQLiteDict:

```json
{
  "prefix": "prefix can be null",
  "action": "override, get_table_names, get_keys, get_content_as_dict, deleteTable, read, has, delete",
  "data": {
    "key": "key",
    "value": "value",
    "table": "tablename"
  }
}
```

### Permission Control:

```json
{
  "prefix": "prefix can be null",
  "permission": "grant or revoke or check",
  "data": {
    "table": "tablename",
    "username or userid": "username or userid",
    "action": "insert, read, override, delete, __all__"
  }
}
```

## Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new pull request

## License

This project is licensed under the [MIT License](LICENSE).