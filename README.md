# Bookshelf-API
This project is a virtual bookshelf for Udacity students. Students are able to add their books to the bookshelf, give them a rating, update the rating and search through their book lists.
The codes are written using [PEP 8 style guide](https://peps.python.org/pep-0008/). 

## Getting Started
### Local Development 
The instructions below are meant for the local setup only. The classroom workspace is already set for your to start practicing. 

#### Pre-requisites
* Developers using this project should already have Python3, pip and node installed on their local machines.


* **Start your virtual environment** 
From the backend folder run
```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

* **Install dependencies**<br>
From the backend folder run 
```bash
# All required packages are included in the requirements file. 
pip3 install -r requirements.txt
# In addition, you will need to UNINSTALL the following:
pip3 uninstall flask-socketio -y
```

### Step 1 - Create and Populate the database
1. **Verify the database username**<br>
Verify that the database user in the `/backend/books.psql`, `/backend/models.py`, and `/backend/test_flaskr.py` files must be either the `student` or `postgres` (default username). FYI, the classroom workspace uses the `student`/`student` user credentials, whereas, the local implementation can use the dafault `postgres` user without a password as well. (See the `/backend/setup.sql` for more details!)

2. **Create the database and a user**<br>
In your terminal, navigate to the directory, and run the following:
```bash
cd */backend
# Connect to the PostgreSQL
psql postgres
#View all databases
\l
# Create the database, create a user - `student`, grant all privileges to the student
\i setup.sql
# Exit the PostgreSQL prompt
\q
```


3. **Create tables**<br>
Once your database is created, you can create tables (`bookshelf`) and apply contraints
```bash
# Mac and windows users
psql -f books.psql -U student -d bookshelf
# Linux users
su - postgres bash -c "psql bookshelf < /path/to/exercise/backend/books.psql"

```
**You can even drop the database and repopulate it, if needed, using the commands above.** 


### Step 2: Start the backend server
Navigate to the `/backend/flaskr/__init__.py` file, and finish all the `@TODO` thereby building out the necessary routes and logic to get the backend of your app up and running.

Once you've written your code, start your (backend) Flask server by running the command below from the `/backend/` directory.
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application will run on `http://127.0.0.1:5000/` by default and is set as a proxy in the frontend configuration. Also, the current version of the application does not require authentication or API keys. 



### Step 3: Start the frontend
(You can start the frontend even before the backend is up!)
From the `frontend` folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```
By default, the frontend will run on `localhost:3000`. Close the terminal if you wish to stop the frontend server. 

---

## Additional information
#### Running Tests
If any exercise needs testing, navigate to the `/backend` folder and run the following commands: 
```bash
psql postgres
dropdb bookshelf_test
createdb bookshelf_test
\q
psql bookshelf_test < books.psql
python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Cannot process request
- 405: Method not allowed
- 500: Server Error

### Endpoints 
#### GET /books
- General:
    - Returns a list of book objects, success value, and total number of books
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/books`

``` {
  "books": [
    {
      "author": "Stephen King",
      "id": 1,
      "rating": 5,
      "title": "The Outsider: A Novel"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 5,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 5,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 5,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    }
  ],
"success": true,
"total_books": 18
}
```

#### POST /books
- General:
    - Creates a new book using the submitted title, author and rating. Returns the id of the created book, success value, total books, and book list based on current page number to update the frontend. 
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`
```
{
  "books": [
    {
      "author": "Neil Gaiman",
      "id": 24,
      "rating": 5,
      "title": "Neverwhere"
    }
  ],
  "created": 24,
  "success": true,
  "total_books": 17
}
```

#### SEARCH /books/search
- General:
    - Searches for books that meeet the search criteria passed with the body of the request. 
- ` curl -X POST http://127.0.0.1:5000/books/search -H "Content-type: application/json" -d '{"search": "A"}'`

```
{
  "books": [
    {
      "author": "Sunny",
      "id": 27,
      "rating": 1,
      "title": "Dev FirmusTemplateMods"
    },
    {
      "author": "Sunny",
      "id": 25,
      "rating": 5,
      "title": "Increase space for message characters in order to allow formatting"
    },
    {
      "author": "Sunny",
      "id": 23,
      "rating": 5,
      "title": "Dev ApprovalApi"
    },
    {
      "author": "Gregory Blake Smith",
      "id": 16,
      "rating": 2,
      "title": "The Maze at Windermere"
    },
    {
      "author": "Rachel Kushner",
      "id": 15,
      "rating": 4,
      "title": "The Mars Room"
    },
    {
      "author": "Emily Giffin",
      "id": 13,
      "rating": 2,
      "title": "All We Ever Wanted"
    },
    {
      "author": "Kiese Laymon",
      "id": 12,
      "rating": 4,
      "title": "Heavy: An American Memoir"
    },
    {
      "author": "Jordan B. Peterson",
      "id": 11,
      "rating": 5,
      "title": "12 Rules for Life: An Antidote to Chaos"
    }
  ],
  "success": true,
  "total_books": 12
}
```

#### DELETE /books/{book_id}
- General:
    - Deletes the book of the given ID if it exists. Returns the id of the deleted book, success value, total books, and book list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/books/16?page=2`
```
{
  "books": [
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    },
    {
      "author": "Jordan B. Peterson",
      "id": 11,
      "rating": 5,
      "title": "12 Rules for Life: An Antidote to Chaos"
    },
    {
      "author": "Kiese Laymon",
      "id": 12,
      "rating": 1,
      "title": "Heavy: An American Memoir"
    },
    {
      "author": "Emily Giffin",
      "id": 13,
      "rating": 4,
      "title": "All We Ever Wanted"
    },
    {
      "author": "Jose Andres",
      "id": 14,
      "rating": 4,
      "title": "We Fed an Island"
    },
    {
      "author": "Rachel Kushner",
      "id": 15,
      "rating": 1,
      "title": "The Mars Room"
    }
  ],
  "deleted": 16,
  "success": true,
  "total_books": 15
}
```
#### PATCH /books/{book_id}
- General:
    - If provided, updates the rating of the specified book. Returns the success value and id of the modified book. 
- `curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
```
{
  "id": 15,
  "success": true
}
```

👤 **Cyril Iyadi**

- GitHub: [@see-why](https://github.com/see-why)
- LinkedIn: [C.Iyadi](https://www.linkedin.com/in/cyril-iyadi/)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).

## Show your support

Give a ⭐️ if you like this project!

## Acknowledgments
- Caryn McCarthy [@cmccarthy15](https://github.com/cmccarthy15), for a great course content
## 📝 License
- This project is [MIT](./LICENSE) licensed.