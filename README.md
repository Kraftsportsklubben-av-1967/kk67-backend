# KK-67 Backend

In order to avoid leaking API_KEYS, the backend shall fetch all data from Facebook, Instagram etc.

The backend is a simple Python REST API developed with _Flask_

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

# Contribute

This server is maintained by Marius Arhaug.

To contribute to this project, follow the guidelines described in the [CONTRIBUTING.md](./CONTRIBUTING.md)

## Endpoints

Currently the REST API\* supports these endpoints:

```
/health     # Get server health (TODO get actual health)
/posts/fb   # Get facebook posts based on .env variables (we want kk67 posts)
/posts/ig   # Get instagram posts --||--

/posts/fb/<pagination_token>   # Get facebook posts based on pagination token
/posts/ig/<pagination_token>   # Get instagram posts --||--
```

> For more info about REST APIs check this [video](https://www.youtube.com/watch?v=-MTSQjw5DrM&t=377s&ab_channel=Fireship).
> Only the first 100 sec is about the concept of REST APIs..
