# Introduction

This is the same application as the full-stack-example-1 from
a previous assignment.  You can read about it here:
https://github.com/env3d/full-stack-example-1

Start a codespace.  Once completed, this will create a linux server that
is ready for node development and you can access the app using
the assignment URL from the "Ports" tab.

# Task

HMAC signature is good for verification when the issuer is the same as the
verifier.  If you want to issue a token and have other parties verify it, we
will need to use the public/private key combination where the private key is
used to sign the token and the public key is used to verify it.

Modify the app so that all the endpoints are protected and can only be accessed
with a valid id_token from google in the Authorization Bearer header.  Below is
a sequence diagram of what happens when a valid token is sent to the backend:

![Auth sequence](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=dGl0bGUgQXBwIEF1dGggd2l0aCBKV1QKCkNsaWVudCBBcHAtPgAWBVByb3ZpZGVyOiAvbG9naW4gKHVzZXIgaWQvcGFzc3dvcmQpCgAcDS0-ADoKOiBUb2tlbgBJDQASDFN0b3JlABETQmFja2VuZCBBcGk6IC1IICdBdXRob3JpemF0aW9uOiBCZWFyZXIgJHsAWgV9JyAvQVBJX0NhbGwKADALADkPdmVyaWZ5KHRva2VuKQAaDkRhdGFiYXNlOiBTUUwKAAYIAHkPcmVzdWx0cwBUDgCBYAxIVFRQIDEuMS8yMDAgT0ssAIJRBgAwByBpbiBib2R5IAo&s=default)

To make things easier, I have provided an example node app for you as a reference:
https://github.com/env3d/jwt-node-example.  The validateJwt.js file provides the
function for you to use.  This is also a good time to look up "middleware" in NodeJs.  

HINT: the above example endpoint verifies a token provided in the query parameter.
When integrating in a webapp, you will expect the token in the "Authorization: Bearer"
header.  Here’s a relevant StackOverflow thread:
https://stackoverflow.com/questions/50284841/how-to-extract-token-string-from-bearer-token 

There’s no need to modify your frontend.  We will be testing your API via curl.
