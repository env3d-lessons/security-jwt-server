# Introduction

This is the same application as the full-stack-example-1 from
a previous assignment.  You can read about it here:
https://github.com/env3d/full-stack-example-1

Start a codespaces.  Once completed, this will create a linux server that
is ready for node development and you can access the app using
the assignment URL from the "Ports" tab.

You may have to wait a little while for codepsaces to start and install
everything properly.  Once it's finished, run `npm run dev` in the terminal
and you'll have the option to open a browser to access the running
app.

# Task

HMAC signature is good for verification when the issuer is the same as the
verifier.  If you want to issue a token and have other parties verify it, we
will need to use the public/private key combination where the private key is
used to sign the token and the public key is used to verify it.

Modify the app so that all the endpoints are protected and can only be accessed
with a valid id_token from google in the Authorization Bearer header.  Below is
a sequence diagram of what happens when a valid token is sent to the backend:

![Auth sequence](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=dGl0bGUgQXBwIEF1dGggd2l0aCBKV1QKCkNsaWVudCBBcHAtPgAWBVByb3ZpZGVyOiAvbG9naW4gKHVzZXIgaWQvcGFzc3dvcmQpCgAcDS0-ADoKOiBUb2tlbgBJDQASDFN0b3JlABETQmFja2VuZCBBcGk6IC1IICdBdXRob3JpemF0aW9uOiBCZWFyZXIgJHsAWgV9JyAvQVBJX0NhbGwKADALADkPdmVyaWZ5KHRva2VuKQAaDkRhdGFiYXNlOiBTUUwKAAYIAHkPcmVzdWx0cwBUDgCBYAxIVFRQIDEuMS8yMDAgT0ssAIJRBgAwByBpbiBib2R5IAo&s=default)

To make things easier, I have provided a function in the file validateJwt.js called 
`verifyGoogleToken`.  This function comes from the google oauth library and return 
the token data if valid and returns null if token is invalid. 

Below is a simple example of how to use this function:

```javscript
const express = require('express');
const verifyGoogleToken = require('./validateJwt.js');

const app = express();
app.use(express.json());

app.post('/auth/google', async (req, res) => {
    const { token } = req.body;

    if (!token) {
        return res.status(400).json({ message: 'Token is required' });
    }

    const userData = await verifyGoogleToken(token);
    if (!userData) {
        return res.status(401).json({ message: 'Invalid Google token' });
    }

    res.json({ message: 'Token is valid', user: userData });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
```

HINT: the above example endpoint verifies a token provided in the request body.
When integrating in a webapp, you will expect the token in the "Authorization: Bearer"
header.  Here’s a relevant StackOverflow thread:
https://stackoverflow.com/questions/50284841/how-to-extract-token-string-from-bearer-token 

There’s no need to modify your frontend.  We will be testing your API via curl.

# Hand-in

Create a valid google JWT in the google oauth playground.  Put the JWT in a file
called `jwt.txt`.

Run `pytest` to make sure you have completed all the steps.  

When you are satisified, run the following commands to submit:

  - git add -A
  - git commit -a -m 'submit'
  - git push
