# SWE Crypto Cupcakes - Python

**See setup instructions on the `main` branch to install dependencies and start the Flask server.**

This branch refactors the basic auth flow to use tokens, which allows for a much
improved user experience.

## Coach notes

The big concept here is [tokens](https://mv-swe-docs.netlify.app/backend/tokens.html).
We're using JWTs to demonstrate this.

The framework the apprentice is working with might already have pushed them in
the direction of tokens when they were exploring basic auth last week. This is
fine! The implementation here is quite manual so we can really see what is going
on under the hood.

## Things to see and do


### Create a token secret

This could be anything, but 32 random bytes is a safe bet:

```bash
openssl rand -hex 32
```

produces something like

```bash
5325d132e0ddb67229a796ecaeaa5a17e44632304369d00be222170ec9006bcd
```

Create your own, or use this one, and save it as `TOKEN_SECRET` in the `.env`
file just as we did with the `ENCRYPTION_KEY` in the previous session.

### Create a user

In this new token based world, we create a user and then sign them in.

```bash
curl -L -v -XPOST \
-H "Content-type: application/json" \
-d '{ "email" : "test@user.com", "password" : "password123" }' \
'http://localhost:5000/users' | json_pp
```

creates the user, and

```bash
curl  -L -v -XGET \
-H "Authorization: Basic dGVzdEB1c2VyLmNvbTpwYXNzd29yZDEyMw==" \
"http://localhost:5000/users/login"
```

signs them in. The latter command should provide you with an accessToken in the
response. Something like:

```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdXNlci5jb20iLCJleHAiOjE3MDQzODA2MzV9.JMUvA3toHf8R0mNz65bQZwUdMTrDkzInHwJ0B7eRdMs
```

If you were to sign in again, you would get a different token each time.

### Access a resource

The GET `'/users'` endpoint has been protected by requiring a JWT. In order to access them,
you don't need to send your password again, but instead you send your token!

```bash
curl -L -v -XGET 'http://localhost:5000/users'
```

will fail, but

```bash
curl -L -v -XGET \
-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdXNlci5jb20iLCJleHAiOjE3MDQzODA2MzV9.JMUvA3toHf8R0mNz65bQZwUdMTrDkzInHwJ0B7eRdMs' \
'http://localhost:5000/users'
```

should succeed.

Try changing a single character in the token and see what happens. This prevents
hackers from spoofing tokens. Try also changing the `TOKEN_SECRET` and using the
correct access token - it should fail because the secret we use to check the
token must be the same secret we used to sign it.

If you split the token at the `'.'` characters, you can decode the parts from
Base 64 to utf-8 so that you can see what they contain.

### authMiddleware.py

This is the middleware which parses out the token, and then checks that it was
signed with the `TOKEN_SECRET`, verifying that it really came from our server.

Have a look at the lines. At what point to we check the token? What is the
difference between a `401` and a `403` error code?

## Next steps

As mentioned, the frameworks the apprentices are using might implement
token-based authentication in very different ways, and they might not need to do
much to handle the verification of tokens and handling of secrets. The
underlying protocol should be roughly the same, however, so encourage them to
lean into their framework's documentation and not be too worried if the
implementation of auth looks quite different.

Focus on the requirements in the spec.
