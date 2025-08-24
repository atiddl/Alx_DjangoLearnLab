# Social Media API

A Django REST Framework-based backend for a simple social media platform that includes user authentication, profiles, posts, and comments.


##  Setup Instructions

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
.venv\Scripts\activate       # On Windows
# Or
source .venv/bin/activate   # On macOS/Linux
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run the development server:

```bash
python manage.py runserver
```

---

## Authentication

All endpoints (except registration and login) require Token Authentication.

Set the header like this:

```
Authorization: Token your_token_here
```

---

##  API Endpoints

###  User Endpoints

| Endpoint         | Method  | Description                 |
| ---------------- | ------- | --------------------------- |
| `/api/register/` | POST    | Register user and get token |
| `/api/login/`    | POST    | Login and receive token     |
| `/api/profile/`  | GET/PUT | View or update user profile |

---

###  Post Endpoints

| Endpoint           | Method | Description                |
| ------------------ | ------ | -------------------------- |
| `/api/posts/`      | GET    | List all posts (paginated) |
| `/api/posts/`      | POST   | Create a new post          |
| `/api/posts/<id>/` | GET    | Retrieve a single post     |
| `/api/posts/<id>/` | PUT    | Update your own post       |
| `/api/posts/<id>/` | DELETE | Delete your own post       |

####  Optional Query Parameters

* `?search=keyword` – filter posts by title or content
* `?page=2&page_size=5` – pagination controls

---

###  Comment Endpoints

| Endpoint              | Method | Description                   |
| --------------------- | ------ | ----------------------------- |
| `/api/comments/`      | GET    | List all comments (paginated) |
| `/api/comments/`      | POST   | Create a comment on a post    |
| `/api/comments/<id>/` | PUT    | Update your own comment       |
| `/api/comments/<id>/` | DELETE | Delete your own comment       |

---

##  User Model Fields

* `username` *(inherited from AbstractUser)*
* `email` *(inherited from AbstractUser)*
* `bio`: `TextField`
* `profile_picture`: `ImageField`
* `followers`: `ManyToManyField` (self-referencing, `symmetrical=False`)

---

##  Project Structure (Simplified)

```
social_media_api/
├── accounts/
│   ├── models.py          # Custom user model
│   ├── serializers.py     # User, login, profile serializers
│   ├── views.py           # Auth and profile views
│   └── urls.py            # /api/register/, /login/, /profile/
│
├── posts/
│   ├── models.py          # Post and Comment models
│   ├── serializers.py     # Post and Comment serializers
│   ├── views.py           # ViewSets with permissions
│   ├── permissions.py     # IsAuthorOrReadOnly
│   └── urls.py            # /api/posts/, /comments/
│
├── social_media_api/
│   ├── settings.py
│   └── urls.py
```

---

##  Features

* Custom user model with extended fields
* Token-based authentication
* Post creation and management (CRUD)
* Comment system with permissions
* Pagination and search filtering for posts
* Self-documenting API structure using DRF routers

---

##  Example API Usage (Postman)

Register:

```http
POST /api/register/
{
  "username": "jane",
  "email": "jane@example.com",
  "password": "pass1234"
}
```

Login:

```http
POST /api/login/
{
  "username": "jane",
  "password": "pass1234"
}
```

Create Post:

```http
POST /api/posts/
Authorization: Token <token>
{
  "title": "Hello World",
  "content": "My first post."
}
```

Create Comment:

```http
POST /api/comments/
Authorization: Token <token>
{
  "post": 1,
  "content": "Great post!"
}
```

###  User Follow Endpoints

| Endpoint                   | Method | Description                         |
| -------------------------- | ------ | ----------------------------------- |
| `/api/follow/<user_id>/`   | POST   | Follow the user with the given ID   |
| `/api/unfollow/<user_id>/` | POST   | Unfollow the user with the given ID |

####  Requires Token Authentication

Example header:

```
Authorization: Token your_token_here
```

####  Example – Follow User

POST `/api/follow/3/`

```json
Response:
{
  "detail": "You are now following bob."
}
```

####  Example – Unfollow User

POST `/api/unfollow/3/`

```json
Response:
{
  "detail": "You have unfollowed bob."
}
```

---

###  Feed Endpoint

| Endpoint     | Method | Description                             |
| ------------ | ------ | --------------------------------------- |
| `/api/feed/` | GET    | Get a list of posts from followed users |

* Results are ordered by newest first (`created_at desc`)
* Supports pagination: `?page=1&page_size=10`

####  Example Request

GET `/api/feed/`
Header:

```
Authorization: Token your_token_here
```

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "author": "bob",
      "title": "Hello",
      "content": "My latest post",
      "created_at": "2025-08-23T15:30:00Z",
      ...
    }
  ]
}
```


## License

This project is licensed for educational or personal use. Please contact the author before using it commercially.

```