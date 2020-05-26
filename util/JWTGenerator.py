import jwt
import time
import hashlib


class JWTGenerator:

    def __init__(self, account_id, access_key, secret_key):
        self.account_id = account_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.expire = 360
        #self.canonical_path = canonical_path

    def generate_jwt(self,canonical_path):
        payload = {
            'sub': self.account_id,
            'qsh': hashlib.sha256(canonical_path.encode('utf-8')).hexdigest(),
            'iss': self.access_key,
            'exp': time.time()+self.expire,
            'iat': time.time()
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256').strip().decode('utf-8')
        return token

    def headers(self):
        headers = {
            'Authorization': 'JWT '+self.jwt(),
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }
        return headers