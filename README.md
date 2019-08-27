# dfuse_python_rest_api
Example of working with REST api of dfuse https://docs.dfuse.io

The dfuse API is available for multiple EOSIO networks. Example:      

EOS Mainnet    
Chain ID: aca376f2...    
REST	https://mainnet.eos.dfuse.io/

**AUTHENTICATION**   
There are two sorts of keys in the dfuse ecosystem:

A long-lived API key, which looks like ```server_abcdef123123123000000000000000000```, used to get short-lived JWT.

A short-lived JWT, used to do any call on the dfuse Platform, which looks like: ```eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NTYxMzI4MjAsImp0aSI6IjQwNWVmOTUxLTAwZTYtNGJmNC1hZWMxLTU0NTU1ZWMzMTUwMiIsImlhdCI6MTU1NjA0NjQyMCwiaXNzIjoiZGZ1c2UuaW8iLCJzdWIiOiJ1aWQ6MHdlbnU2NmUwNzU4OWRhODY4MWNlIiwiYWtpIjoiM2NhYWEzYzA3M2FlZjVkMmYxOGUwNjJmZDkzYzg3YzMzYWIxYzA1YzEzNjI3NjU2OTgzN2Y5NDc5NzZlMjM0YSIsInRpZXIiOiJmcmVlLXYxIiwic3RibGsiOi0zNjAwLCJ2IjoxfQ.000HeTujIuS_LRvvPN6ZRCmtoZqZyV6P1enNBviwK8v7Tf7BLHJIrEpQoEREKSIMdZWPrMQl_OE55yJP0MxUDA```


**Lifecycle of short-lived JWTs**   
The best way to handle each JWT’s lifecycle is, before doing calls to dfuse:   
* Get JWT + Expiration time from cache (localStorage, disk, etc..)
* If token is expired, is near expiration or is absent from cache, fetch a new token through /v1/auth/issue, and cache the response.
* Call dfuse with a JWT token.    

Each time you get a fresh JWT, you get the expiration and the token itself.  

Once a connection is established using a JWT, it will not be shutdown, even though the JWT expires during the session.
