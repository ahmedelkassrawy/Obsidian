![[Pasted image 20250218033401.png]]
 it’s a standardized security token format
# **Why we need it?**

It allows for stateless authentication where the server doesn’t need to store session information.
Before JWT, session-based authentication was common. This required the server to maintain a session store to track authenticated users.

# **The components**
JSON Web Tokens (JWTs) are a standardized way to securely send data between two parties.

 we can see that it has 3 parts each containing some data, divided by a dot symbol:
 1. Header
```json
 {  
	“alg”: “HS256”,  
	“typ”: “JWT”  
}
```

It gives information about how we should read and validate the token’s data and signature.

2. Payload

```json
{  
	“sub”: “1234567890”,  
	“name”: “John Doe”,  
	“admin”: true  
}
```
The payload is the content of the token itself,
the JSON object that you are protecting and transmitting to another party
The data in the payload consists of what we call <span style="background:#40a9ff">claims</span>
claims ->  statements about an entity made by the token’s creator.

3 types  of claims:
1. [**Registered claims**](https://tools.ietf.org/html/rfc7519#section-4.1):
2. [**Public claims**](https://tools.ietf.org/html/rfc7519#section-4.2)
3. [**Private claims**](https://tools.ietf.org/html/rfc7519#section-4.3)

**Signature**
The signature part of a JWT is crucial for ensuring the integrity and authenticity of the token
It verifies that the token has not been tampered with and that it was indeed issued by a trusted source.

The signature is used to verify the message wasn’t changed along the way, and, in the case of tokens signed with a private key, it can also verify that the sender of the JWT is who it says it is.

#### Process
In authentication, when the user successfully logs in using their credentials, a JSON Web Token will be returned.
Whenever the user wants to access a protected route or resource, the user agent should send the JWT, typically in the `Authorization` header.
The server’s protected routes will check for a valid JWT in the `Authorization` header, and if it's present, the user will be allowed to access protected resources

### **How is the Signature Used?**
When a JWT is received by the server, it needs to validate the token.
- **Reconstruct the Signature** ->  Using the same algorithm and secret key
the server reconstructs the signature by signing the header and payload again.
- **Compare Signatures** : The server compares the reconstructed signature with the signature included in the received JWT. If they match, the token is considered valid and untampered.
- **Check Claims**:The server then checks the claims within the payload to ensure they meet the required conditions (e.g., not expired, correct audience, etc.).