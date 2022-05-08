# Contributing

## Get started

This project is written in Python 3.9 with the Flask

1. Install python3.9

Ubuntu

```sh
$ sudo apt install python3.9
```

2. Install dependecies

```sh
$ pip install -r requirments.txt
```

3. Setting up Flask environment

```sh
$ export FLASK_APP=src/app.py
```

```sh
$ export FLASK_ENV=development
```

4. Setup environment variables in a `.env` file (**not** to be pushed to the repo). Ask **Marius** for key(s)/id(s)

```sh
FB_USER_KEY=<key>
FB_PAGE_KEY=<key>
FB_USER_ID=<id>
FB_PAGE_ID=<id>
```

5. Run app

```sh
$ flask run
```

Runs the app locally in development mode with file reload

Open `localhost:5000` in your browser to request endpoints.

I personally recommend **Insomnia** for advanced endpoint requesting
