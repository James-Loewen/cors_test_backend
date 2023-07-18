# Cross-Origin Resource Sharing & Session Cookie Web API

This project is a back-end web API written with Django and Django Rest Framework (DRF). I want to see if it's possible (or secure) to use session cookies to authenticate requests made across unrelated domains.

**Table of Contents**

- [Front-End Repository](#front-end-repository)
- [Installation](#installation)
- [API Documentation](#api-documentation)
    - [Base URL](#base-url)
    - [Authentication](#authentication)
    - **[CSRF Protection](#cross-site-request-forgery-csrf-protection)**
    - [Endpoints](#endpoints)
    - [Error Handling](#error-handling)
- [License](#license)

<a name="front-end-repository"></a>

## Front-End Repository

For the front-end aspect of this project, please refer to the [front-end repository](https://github.com/James-Loewen/cors_test_frontend).

<a name="installation"></a>

## Installation

***It is not necessary to host this project locally.*** The API is hosted publicly using a free [PythonAnywhere](https://www.pythonanywhere.com/) server. Server url is [https://pynoodler.pythonanywhere.com/](https://pynoodler.pythonanywhere.com/).

Clone the repository:

```bash
git clone https://github.com/James-Loewen/cors_test_backend.git
```

Install the project dependencies using either the `requirements.txt` or `Pipfile`:

```bash
# Using built-in venv
cd cors_test_backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

*or*

```bash
# Using pipenv
pip install pipenv # if not already installed
cd cors_test_backend
pipenv shell       # create & activate venv
pipenv install     # install dependencies from Pipfile
```

Run database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API should now be accessible at `http://localhost:8000/`.

<a name="api-documentation"></a>

## API Documentation

<a name="base-url"></a>

### Base URL

The base URL for accessing the API is `https://pynoodler.pythonanywhere.com/`

There currently is no homepage for the back-end so the base URL will display a `Page not found (404)` screen.

<a name="authentication"></a>

### Authentication

The API uses Django's built-in, cookie-based session authentication.

When a user authenticates successfully, a session cookie is created and stored in the client's browser under the domain `https://pynoodler.pythonanywhere.com/`. Subsequent requests from the client include this session cookie, allowing the API to identify and authenticate the user.

Requests made from the DRF browsable API pages on the same domain as the authenticating server have innate access to the session cookie.

Requests made from this project's front-end component use the JavaScript [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) with the option `credentials` set to `'include'`. The front-end for this project is explicitly whitelisted by the back-end via the django-cors-headers app and the `CORS_ALLOWED_ORIGINS` list in the `config.settings` module.

<a name="cross-site-request-forgery-csrf-protection"></a>

### Cross-Site Request Forgery (CSRF) Protection

*For some background, here's a good article from OWASP about [CSRF attacks and prevention methods](https://owasp.org/www-community/attacks/csrf). Their [cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) is also very informative.*

This is one of my primary learning goals for this project. The following are some questions I'm hoping to find answers to:

#### 1. When using this method of authentication (i.e., cross-domain session cookies), is it *necessary* to protect against CSRF/XSRF attacks? Is this setup vulnerable to that kind of attack?

**Hypothesis:**

- CSRF protection **is necessary**. Sites using this method of authentication are no less vulnerable than sites whose front-end is served from the same domain as the back-end.

#### 2. Assuming CSRF protection is necessary, *how* can I implement it?

Django comes with built-in CSRF protections, but they work best when the Django back-end is serving the HTML files that users interact with. Check out the Django [documentation](https://docs.djangoproject.com/en/stable/howto/csrf/), it's wonderful.

Django has two general methods for handling CSRF protection, both required a masked token along with the original cookie set by Django:

1. Each `POST`, `PUT`, and `DELETE` form (i.e., all "potentially destructive" requests) must include a hidden input element that contains a scrambled/masked version of the CSRF cookie value. Upon submission, this masked value is compared against the cookie value and if the check passes, the request is allowed, if not, a `403` status code is returned.

2. For AJAX requests (like the ones this project makes), the process is similar to the above, but the masked token is inserted into the header of each request. By default the header name is `X-CSRFToken`.

For this project, I have to use the second option. However, the question becomes *How does the client receive/retrieve the token?* For AJAX requests being made from the same domain, Django recommends using JavaScript to retrieve the token from the cookie itself, or if the cookie is httpOnly or otherwise unavailable, from the hidden input element. My front-end has access to neither so I need to come up with another option.

**Option 1:** Return the masked CSRF token as part of the initial login response.

This option *feels* safer, especially if the requests are only made over HTTPS, but it introduces the problem of where to store the token. I could use `localStorage`, but this introduces a Cross-Site Scripting (XSS) vulnerability. Even if we, as developers, trust ourselves to sanitize all inputs and write generally *safe* code, we cannot trust that each and every one of our projects' dependencies are safe and scrupulous.

That said, how dangerous is this? It certainly isn't as immediately dangerous as storing an authenticating JSON Web Token (JWT) in `local`/`sessionStorage`. If a malicious entity got its hands on something like that, a user's entire account would become immediately compromised. Whereas if the CSRF token were stolen, that would simply open up the possibility for CSRF attacks to work. Users would still need to encounter and be tricked into triggering them during the lifetime of their session.

**Option 2 [currently in use]:** Expose an API endpoint that returns the masked CSRF token.

This endpoint has to be public or users would never be able to log in. Truthfully, I don't understand CORS enough to know whether or not this is a problem. The following JavaScript can be used to grab and log a new CSRF token from the endpoint:

```javascript
(async () => {
    const res = await fetch("https://pynoodler.pythonanywhere.com/get_csrf/");
    const data = await res.json();
    console.log(data);
})();
```

As expected, because the front-end domain is whitelisted by the back-end, if you visit the front-end site, go into dev tools, and paste that JavaScript into the console, you will see an output like the following:

```javascript
Promise { <state>: "pending" }
Object { token: "E5poMUU2gWUYP52IKBwXvuqt7PAqQy5OgKvlYRuDVODQSpPaGed4yoxTtO80dI8M" }
```

However, if you go to a non-whitelisted domain—like `https://www.google.com`—and do the same thing, you'll see an error message that looks like the following:

```diff
- Cross-Origin Request Blocked: The Same Origin Policy disallows reading
- the remote resource at https://pynoodler.pythonanywhere.com/get_csrf/.
- (Reason: CORS header ‘Access-Control-Allow-Origin’ missing). Status code: 200.
```

The fact that it returns an error message makes sense. The `Status code: 200` part doesn't entirely make sense to me. I would have thought that the Django middleware function that handles CSRF token checking would raise an Exception and return an HTTP error code like `403`. Perhaps it isn't the middleware's decision to make and it assumes that because it has done its job of not setting the `Access-Control-Allow-Origin` header, the CORS error will be handled by the client's browser, *which seems to be the case*.

It does not seem like the data from the response is made available to JavaScript in the client's browser, which I *believe* would prevent CSRF vulnerabilities. However, on some browsers—like FireFox—the response data ***is*** viewable from the network tab of the dev tools. I understand that the *attacker* won't have access to this visual information, but I suppose it makes me nervous that the desired information was transferred at all.

From a data-persistance standpoint, I like this method better because I can request the CSRF token as soon as a user logs in and store it in-memory as a React state object and fetch new tokens on page refreshes and re-visits.

<a name="endpoints"></a>

### Endpoints

#### `GET /get_csrf/`

Endpoint that returns a new `csrf_token` object associated with the current session (if a user is logged in, otherwise its anonymous). 

##### Request

- **Method:** GET

##### Response

- **Status:** 200 OK
- **Body:**

```JSON
{
    "token": "E5poMUU2gWUYP52IKBwXvuqt7PAqQy5OgKvlYRuDVODQSpPaGed4yoxTtO80dI8M"
}
```

#### `GET /get_user/`

Endpoint that returns the `user` object associated with the current session. 

##### Request

- **Method:** GET

##### Response

- **Status:** 200 OK
- **Body:**

```JSON
{
    "id": "1",
    "first_name": "Suki",
    "last_name": "Cat",
    "username": "sandal_cat",
    "date_joined": "2023-07-11T12:40:10Z"
}
```

#### `POST /register/`

Endpoint for user registration.

##### Request

- **Method:** POST
- **Headers:**
    - Content-Type: application/json
    - X-CSRFToken: `csrf_token`
- **Body:**

```JSON
{
    "first_name": "Suki",
    "last_name": "Cat",
    "username": "sandal_cat",
    "password": "password1234"
}
```

##### Response

- **Status:** 201 Created
- **Body:**

```JSON
{
    "id": "1",
    "first_name": "Suki",
    "last_name": "Cat",
    "username": "sandal_cat",
    "date_joined": "2023-07-11T12:40:10Z"
}
```

#### `POST /my_login/`

Endpoint for user login and authentication.

##### Request

- **Method:** POST
- **Headers:**
    - Content-Type: application/json
    - X-CSRFToken: `csrf_token`
- **Body:**

```JSON
{
    "username": "sandal_cat",
    "password": "password1234"
}
```

##### Response

- **Status:** 200 OK
- **Body:**

```JSON
{
    "id": "1",
    "first_name": "Suki",
    "last_name": "Cat",
    "username": "sandal_cat",
    "date_joined": "2023-07-11T12:40:10Z"
}
```

#### `POST /my_logout/`

Endpoint for user logout and session flush.

##### Request

- **Method:** POST
- **Headers:**
    - Content-Type: application/json
    - X-CSRFToken: `csrf_token`
- **Body:**
    - `{}`

##### Response

- **Status:** 200 OK
- **Body:**

```JSON
{
    "message": "Successfully logged out!"
}
```

<a name="error-handling"></a>

### Error Handling

The API returns appropriate HTTP status codes and error messages in case of failures. E.g.:

- **Status:** 401 Unauthorized
- **Body:**

```JSON
{
    "message": "Invalid credentials"
}
```

<a name="license"></a>

## License

This project is licensed under the [MIT License](LICENSE).
