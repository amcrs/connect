# amcrs-connect draft

The goal is, to create an API for common software e.g. Houdini, Max, Maya, PS that is not bound to a specific programming language and therefore easy to use for every pipeline team. At first it should cover basic operations that every software supports (e.g. open, save).

## Architecture

To install the API some files must be copied to software specific folders e.g. nuke path, max startup. On application startup, the web server starts and searches for an open port within a specific port range (e.g. 30000 - 30010). It will use the first open port. External scripts just have to create ("get_application_info") requests against these ports on localhost to find running applications.

## Protocol

HTTP seems to be the best choice for a protocol, as it is supported natively by many programming languages. Even if e.g. grpc has libs for all common languages, it might cause problems to install the libs for third party software like photoshop.

## Security

I suggest not to use HTTPS at first, to avoid “self signed certificate” problems. Also using cors should be skipped at first. To authenticate requests against the API, we could use a shared secret in the authorization header. Every unauthenticated request must cause a 401 status code.

Response (401):

```js
// Body
{
  "error": true,
  "code": "unauthorized"
}
```

## Install / Uninstall

Execute src/install.py or src/uninstall.py

## Server API

### get_application_info

Request:

```js
// Headers
{
  "Authorization": "secret"
}
// Body
{
  "command": "get_application_info"
}
```

Response (200):

```js
// Body
{
  "application": "nuke",
  "version": "10.v4",
  "startedAt": "2019-01-01T00:00:00.000Z"
}
```

### get_current_filename

Request:

```js
// Headers
{
  "Authorization": "secret"
}
// Body
{
  "command": "get_current_filename"
}
```

Response (200):

```js
// Body
{
  "error": false,
  "filename": "...path-to-file"
}
```

### open_file

Request:

```js
// Headers
{
  "Authorization": "secret"
}
// Body
{
  "filename": "...path-to-file"
}
```

Response (200):

```js
// Body
{
  "error": false,
  "code": "success"
}
```

Response (400):

```js
// Body
{
  "error": true,
  "code": "invalid_filename"
}
```

### save_file

Request:

```js
// Headers
{
  "Authorization": "secret"
}
// Body
{
  "filename": "...path-to-file"
}
```

Response (200):

```js
// Body
{
  "error": false,
  "code": "success"
}
```

Response (400):

```js
// Body
{
  "error": true,
  "code": "invalid_filename"
}
```
