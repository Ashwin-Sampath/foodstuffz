# zothacks-backend

## Basic overview

Skeleton Flask backend that has CRUD (Create, Read, Update, Delete) endpoints for a User that is stored in a Mongo Database

## Instructions

1. Create and activate your Python Virtual Environment
    ```
    $ python3 -m venv env
    $ source env/bin/activate
    ```
2. Install the project dependencies
    ```
    $ pip3 install -r requirements.txt
    ```
3. Run the project without a debugger
    ```
    $ python3 app.py
    ```

## Endpoints

**GET /user**

Gets users based on params

```
PARAMS:
"_id"                       : String, returned from POST /user
"email"                     : String
"firstName"                 : String
"lastName"                  : String

RETURNS:
"_id"                       : User ID
"email"                     : User's email
"firstName"                 : User's first name
"lastName"                  : User's last name
```

**POST /user**

Creates user based on values in request body

```
BODY:
"email"                     : String, required
"firstName"                 : String, required
"lastName"                  : String, required

RETURNS:
"_id"                       : User ID
"email"                     : User's email
"firstName"                 : User's first name
"lastName"                  : User's last name
```

**PUT /user**

Updates user based on values in request body

```
PARAMS:
"_id"                       : String, required

BODY:
"email"                     : String, required
"firstName"                 : String, required
"lastName"                  : String, required

RETURNS:
"_id"                       : User ID
"email"                     : Updated User's email
"firstName"                 : Updated User's first name
"lastName"                  : Updated User's last name
```

**DELETE /user**

Deletes user based on _id

```
PARAMS:
"_id"                       : String, returned from POST /user

RETURNS:
"message"                   : deleted or error
```
