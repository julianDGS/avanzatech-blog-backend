# Blog Avanzatech

This is a REST API application, developed with Django Rest Framework, to emulate the interactions in a blog, including user authentication, CRUD operations on all post, with likes and comments, based on permissions related to the post and user.

# Table of Contents
1. [Setup using Docker](#Setup-using-Docker)
2. [Manual Setup](#manual-setup)
3. [Endpoints](#Endpoints)
4. [Login](#Login-POST)
5. [Register](#Register-POST)
6. [Logout](#Logout-GET)
7. [Create Post](#Create-Post-POST)
8. [Edit Post](#Edit-Post-PUT)
9. [Retrieve Post](#Retrieve-Post-GET)
10. [List Posts](#List-Posts-GET)
11. [Delete Post](#Delete-Post-DELETE)
12. [Create Like](#Create-Like-POST)
13. [List Likes](#List-Likes-GET)
14. [Delete Like](#Delete-Like-DELETE)
15. [Create Comment](#Create-Comment-POST)
16. [List Comments](#List-Comments-GET)
17. [Delete Comment](#Delete-Comment-DELETE)
18. [List Permissions](#List-Permissions-GET)
19. [List Categories](#List-Categories-GET)

# Setup

## Setup using Docker

Clone the repository [`https://github.com/julianDGS/avanzatech_blog`](https://github.com/julianDGS/avanzatech_blog) from git hub.

1. Install docker, docker-compose.
2. Create a file in the root of the project and name it `.env` . In this file, the following variables should be defined, as in the following example:
    
    ```python
    SECRET_KEY=get_secure_secret_key
    POSTGRES_DB=some_db_name
    POSTGRES_USER=some_db_user
    POSTGRES_PASSWORD=some_db_password
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    ```
    
3. In the root of the project (where the file docker-compose.yaml is) using a command shell execute:

    - `sudo docker-compose build`
    
    - `sudo docker-compose up`   
    
    First command will install all required dependencies and services, and second one run the server in http://localhost:8000/
    

## Manual Setup

Clone the repository [`https://github.com/julianDGS/avanzatech_blog`](https://github.com/julianDGS/avanzatech_blog) from git hub.

Using Python 3.11.9:

1. Create a virtual environment (cannot be named .env) using the following command:
    
     `python3 -m venv .venv`
    
2. Activate the virtual environment and then install all the required libraries executing:
    
    `pip install -r requirements.txt`
    
3. Create a file in the root of the project and name it `.env` . In this file, the following variables should be defined, as in the following example:
    
    ```python
    SECRET_KEY=get_secure_secret_key
    POSTGRES_DB=some_db_name
    POSTGRES_USER=some_db_user
    POSTGRES_PASSWORD=some_db_password
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    ```
    
4. Create a database using Postgres with the same name used in .env file variable POSTGRES_DB.
5. Using a command shell execute the migrations to create the tables in database.
    
    `python manage.py migrate`
    
6. Using a command shell create a super user to access to the admin site.
`python manage.py createsuperuser`
7. Run Django server.
    
    `python manage.py runserver` 
    
8. Login to the admin site `http://localhost:8000/admin/` and create the four categories shown in the select options. Also create the three permissions shown y the select options. 

The authentication system is session based. Then, you need the csrf token given in the response of login to perform actions.

# Endpoints

## Login `POST`

Give you access to the authenticated required actions based on session id

URL: 

`http://localhost:8000/user/login/` 

Request body structure example:

```jsx
{
    "username":"some@mail.com",
    "password":"1234"
}
```

Expected response body example: `HTTP 200`

```jsx
{
    "message": "Successful Login",
    "user": {
        "id": 4,
        "name": "some",
        "last_name": "user",
        "email": "some@mail.com",
        "nickname": "some"
    }
}
```

## Register `POST`

Create a new blogger user

URL: 

`http://localhost:8000/user/register/` 

Request body structure example:

```jsx
{
    "email":"some@mail.com",
    "password":"1234",
    "confirm_password":"1234",
    "name":"some",
    "last_name":"user"
}
```

Expected response body example: `HTTP 201`

```jsx
{
    "id": 1,
    "email": "some@mail.com",
    "name": "some",
    "last_name": "user"
}
```

## Logout `GET`

Close the active session for a user. `Authentication Required`

URL: 

`http://localhost:8000/user/logout/`

Expected response body example: `HTTP 200`

```jsx
{
    "message": "Successful Logout"
}
```

## Create Post `POST`

Create a new post. `Authentication Required`

URL: 

`http://localhost:8000/post/` 

Request body structure example:

```jsx
{
    "title": "Post Title.", 
    "content": "Some content for some post.",
    "permissions": [
        {"category_id":1, "permission_id":1},
        {"category_id":2, "permission_id":2},
        {"category_id":3, "permission_id":3},
        {"category_id":4, "permission_id":1}
    ]
}
```

Expected response body example: `HTTP 201`

```jsx
{
    "id": 1,
    "title": "Post Title.",
    "content": "Some content for some post.",
    "author": 1
}
```

## Edit Post `PUT`

Update an existing post based on its permissions per category. Only for categories with edit permission a user can perform an update, depending on which category that user belongs to.

URL: 

`http://localhost:8000/post/{post_id}/`

Path variable: id of post to be updated 

Request body structure example:

```jsx
{
    "title": "Post Title Updated.", 
    "content": "Some edit content for some post created.",
    "permissions": [
        {"category_id":1, "permission_id":3},
        {"category_id":2, "permission_id":2},
        {"category_id":3, "permission_id":1},
        {"category_id":4, "permission_id":2}
    ]
}
```

Expected response body example: `HTTP 200`

```jsx
{
    "id": 1,
    "title": "Post Title Updated.",
    "content": "Some edit content for some post created.",
    "author": 1
}
```

## Retrieve Post `GET`

Get an existing post based on its permissions per category. Only for categories whit read permission a user can see the post, depending on which category that user belongs to.

URL: 

`http://localhost:8000/post/{post_id}/`

Path variable: id of post to be retrieved 

Expected response body example: `HTTP 200`

```jsx
{
    "id": 1,
    "title": "Post Title Updated.",
    "content": "Some edit content for some post created.",
    "excerpt": "Some edit content for some post created.",
    "author": {
        "id": 1,
        "nickname": "some",
        "email": "user",
        "team": {
            "id": 1,
            "name": "Rookie"
        }
    },
    "permissions": {
        "public": "none",
        "auth": "edit",
        "team": "read",
        "author": "edit"
    },
    "likes": 0,
    "comments": 0,
    "post_liked": true
}
```

## List Posts `GET`

List all existing post based on its permissions per category. Only for categories whit read permission a user can see the list, depending on which category that user belongs to.
The result is an object representing a pagination with ten posts per page.

URL: 

`http://localhost:8000/post/?page={number}` 

Query param: page={number} the page which will be shown

Expected response body example: `HTTP 200`

```jsx
{
    "next": "http://localhost:8000/post/?page=2",
    "previous": null,
    "total_count": 11,
    "current_page": 1,
    "total_pages": 2,
    "results": [
        {
            "id": 1,
            "title": "Post Title Updated.",
            "content": "Some edit content for some post created.",
            "excerpt": "Some edit content for some post created.",
            "author": {
                "id": 1,
                "nickname": "some",
                "email": "user",
                "team": {
                    "id": 1,
                    "name": "Rookie"
                }
            },
            "permissions": {
                "public": "none",
                "auth": "edit",
                "team": "read",
                "author": "edit"
            },
            "likes": 0,
            "comments": 0,
            "post_liked": true
	    },
				
        "..."
        
        ,{
            "id": 10,
            "title": "Post Title 10.",
            "content": "Some content for some post created 10.",
            "excerpt": "Some edit content for some post created 10",
            "author": {
                "id": 1,
                "nickname": "some",
                "email": "user",
                "team": {
                    "id": 1,
                    "name": "Rookie"
                }
            },
            "permissions": {
                "public": "none",
                "auth": "edit",
                "team": "read",
                "author": "edit"
            },
            "likes": 0,
            "comments": 0,
            "post_liked": true
        }
    ]
}
```

## Delete Post `DELETE`

Delete an existing post based on its permissions per category. Only for categories whit edit permission a user can delete the post, depending on which category that user belongs to.

URL: 

`http://localhost:8000/post/{post_id}/`

Path variable: id of post to be deleted 

No response body: `HTTP 204`


## Create Like `POST`

Create a new like for an existing post. An user can like a post just once and only if he has read access. `Authentication Required`

URL: 

`http://localhost:8000/like/` 

Request body structure example:

```jsx
{
    "post_id": 1
}
```

Expected response body example: `HTTP 201`

```jsx
{
    "id": 1,
    "post": {
        "id": 1,
        "title": "Post Title."
    },
    "user": {
        "id": 1,
        "nickname": "some",
        "email": "some@mail.com"
    }
}
```

## List Likes `GET`

List all existing likes based on its permissions per category. Only for categories whit read permission a user can see the list, depending on which category that user belongs to.
The result is an object representing a pagination with twenty likes per page. It is possible to filter results by post, user or both

URL: 

`http://localhost:8000/like/?page={number}&post={number}&user={number}` 

Query params: 

- page={number} the page which will be shown
- post={number} id of post to be filtered
- user={user} id of user to be filtered

Expected response body example: `HTTP 200`

```jsx
{
    "next": "http://localhost:8000/like/?page=2",
    "previous": null,
    "total_count": 21,
    "current_page": 1,
    "total_pages": 2,
    "results": [
        {
	    "id": 1,
	    "post": {
		"id": 1,
		"title": "Post Title."
	    },
	    "user": {
		"id": 1,
		"nickname": "some",
		"email": "some@mail.com"
	    }
	},
        
        "..."
        
        ,{
	    "id": 20,
	    "post": {
		"id": 1,
		"title": "Post Title."
	    },
	    "user": {
		"id": 20,
		"nickname": "some20",
		"email": "some20@mail.com"
	    }
	}
   ]
}
```

## Delete Like `DELETE`

Delete an existing like based on its permissions per category. Only for categories whit edit permission a user can delete the like, depending on which category that user belongs to. A user just can delete his own like. `Authentication Required`

URL: 

`http://localhost:8000/like/{like_id}/`

Path variable: id of like to be deleted

No response body: `HTTP 204`


## Create Comment `POST`

Create a new comment for an existing post. An user can comment only if he has read access. `Authentication Required`

URL: 

`http://localhost:8000/comment/` 

Request body structure example:

```jsx
{
    "post_id": 1,
    "comment": "some comment from user"
}
```

Expected response body example: `HTTP 201`

```jsx
{
    "id": 1,
    "comment": "some comment from user",
    "post": {
        "id": 1,
        "title": "Post Title."
    },
    "user": {
        "id": 1,
        "nickname": "some",
        "email": "some@mail.com"
    }
}
```

## List Comments `GET`

List all existing comments based on its permissions per category. Only for categories whit read permission a user can see the list, depending on which category that user belongs to.
The result is an object representing a pagination with ten comments per page. It is possible to filter results by post, user or both

URL: 

`http://localhost:8000/comment/?page={number}&post={number}&user={number}` 

Query params: 

- page={number} the page which will be shown
- post={number} id of post to be filtered
- user={user} id of user to be filtered

Expected response body example: `HTTP 200`

```jsx
{
    "next": "http://localhost:8000/comment/?page=2",
    "previous": null,
    "total_count": 21,
    "current_page": 1,
    "total_pages": 2,
    "results": [
        {
	    "id": 1
	    "comment": "some comment from user",
	    "post": {
		"id": 1,
		"title": "Post Title."
	    },
	    "user": {
		"id": 1,
		"nickname": "some",
		"email": "some@mail.com"
	    }
	},
				
        "..."
        
        ,{
	    "id": 10,
	    "comment": "some ten comments from user",
	    "post": {
		"id": 1,
		"title": "Post Title."
	    },
	    "user": {
		"id": 20,
		"nickname": "some20",
		"email": "some20@mail.com"
	    }
	}
   ]
}
```

## Delete Comment `DELETE`

Delete an existing comment based on its permissions per category. Only for categories whit edit permission a user can delete the comment, depending on which category that user belongs to. A user just can delete only his own comments. `Authentication Required`

URL: 

`http://localhost:8000/comment/{comment_id}/`

Path variable: id of comment to be deleted

No response body: `HTTP 204`


## List Permissions `GET`

List all existing permissions. `Authentication Required`

URL: 

`http://localhost:8000/permission/` 

Expected response body example: `HTTP 200`

```jsx
[
    {
        "id": 1,
        "name": "read"
    },
    {
        "id": 2,
        "name": "edit"
    },
    {
        "id": 3,
        "name": "none"
    }
]
```

## List Categories `GET`

List all existing permission categories. `Authentication Required`

URL: 

`http://localhost:8000/permission/category/` 

Expected response body example: `HTTP 200`

```jsx
[
    {
        "id": 1,
        "name": "public"
    },
    {
        "id": 2,
        "name": "auth"
    },
    {
        "id": 3,
        "name": "team"
    },
    {
        "id": 4,
        "name": "author"
    }
]
```