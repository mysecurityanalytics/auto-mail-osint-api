# **Auto Mail OSINT - API**

![Logo](./logo.png)

This is an open source project that developed by [Alp Keskin](https://github.com/alpkeskin) and [Davut Kulaksız](https://github.com/davutkulaksiz) within the scope of <b>My Security Analytics 2021 Summer Internship Program</b> which supervised by [Çalgan Aygün](https://github.com/calganaygun).

<i>This repository is the API part of this project.</i>

To learn more about the front-end part, check out the [WEB Repository](https://github.com/mysecurityanalytics/auto-mail-osint-web).

## Functionality

- [x]  Login/Register endpoints with JWT 
- [x]  Email format check
- [x]  Mailbox server check
- [x]  SMTP check
- [x]  Scan social platforms (Instagram, Twitter, Snapchat and Tumblr)
- [x]  Scan mailbox providers (yaani, gmail and protonmail)

### Tech Stack

<img src="https://www.vectorlogo.zone/logos/python/python-ar21.svg" alt="python" width="100"/> <img src="https://www.vectorlogo.zone/logos/mongodb/mongodb-ar21.svg" alt="mongodb" width="100"/>

- For building the APIs, [FastAPI](https://fastapi.tiangolo.com/) is used.

- Server-side is made by using **Python**.

- [MongoDB](https://www.mongodb.com/) used to save users login data and save their searching logs.


## Installation

Clone API repo and install dependencies.

```
  git clone https://github.com/mysecurityanalytics/auto-mail-osint-api.git
  cd auto-mail-osint-api
  pip install -r requirements.txt
```

Set environment variables.

```
  export MONGO_URI=''
  export DB_NAME=''
  export JWT_SECRET=''
```

## Run

```
  uvicorn main:app --reload
```

`--reload`: make the server restart after code changes. Only do this for development!



# API Reference

### Authorization Endpoint Documentation

`http://localhost:8000/auth/docs`
or `http://localhost:8000/auth/redoc`

### Email Verification Endpoint Documentation

`http://localhost:8000/verify/docs`
or `http://localhost:8000/verify/redoc`

### Email Scan Endpoint Documentation

`http://localhost:8000/scan/docs`
or `http://localhost:8000/scan/redoc`


## Status Codes


| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 401 | `UNAUTHORIZED` |
| 403 | `FORBIDDEN` |
| 404 | `NOT FOUND` |
| 409 | `EMAIL ALREADY TAKEN` |
| 500 | `INTERNAL SERVER ERROR` |




Special thanks to [Çalgan Aygün](https://github.com/calganaygun) for his contribution to the project.
