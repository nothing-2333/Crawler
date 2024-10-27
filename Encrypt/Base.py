# python 实现一些经典加密

import base64
import hashlib

def base64Encode(original_string):
    original_bytes = original_string.encode('utf-8')
    encoded_bytes = base64.b64encode(original_bytes)
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def base64Decode(encoded_string):
    encoded_bytes_again = encoded_string.encode('utf-8')
    decoded_bytes = base64.b64decode(encoded_bytes_again)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

def MD5(original_string):
    md5_hash = hashlib.md5()
    md5_hash.update(original_string.encode('utf-8'))
    md5_hash_digest = md5_hash.hexdigest()
    return md5_hash_digest

def SHA256(original_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(original_string.encode('utf-8'))
    sha256_hash_digest = sha256_hash.hexdigest()
    return sha256_hash_digest


if __name__ == "__main__":
    pass

