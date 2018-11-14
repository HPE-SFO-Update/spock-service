from flask_socketio import Namespace, send, emit
from flask import request
import cryptography

"""
Authentication using SSH key pairs begins after the symmetric encryption has been established as described in the last 
section. The procedure happens like this:

1. The client begins by sending an ID for the key pair it would like to authenticate with to the server.

2. The server check's the authorized_keys file of the account that the client is attempting to log into for the key ID.

3. If a public key with matching ID is found in the file, the server generates a random number and uses the public key
 to encrypt the number.
 
4. The server sends the client this encrypted message.

5. If the client actually has the associated private key, it will be able to decrypt the message using that key, 
revealing the original number.

6. The client combines the decrypted number with the shared session key that is being used to encrypt the communication, 
and calculates the MD5 hash of this value.

7. The client then sends this MD5 hash back to the server as an answer to the encrypted number message.

8. The server uses the same shared session key and the original number that it sent to the client to calculate the MD5 
value on its own. It compares its own calculation to the one that the client sent back. If these two values match, it 
proves that the client was in possession of the private key and the client is authenticated.
"""
# https://flask-socketio.readthedocs.io/en/latest/
# https://hub.packtpub.com/making-simple-web-based-ssh-client-using-nodejs-and-socketio/
class Login(Namespace):
    def __init__(self,namespace=None):
        super(Namespace, self).__init__(namespace)
        self.user = []

    def on_connect(self):
        print("Connected ")

    def on_disconnect(self, msg):
        pass

    def on_message(self, msg):
        print('Message: ' + msg)
        send(msg, broadcast=False)

    def on_error(self):
        pass
