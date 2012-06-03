import rsa
import hashlib


def verify_message(ciphertext, signature, pub_key):
    """Checks the signature on the given message."""
    try:
        rsa.verify(ciphertext, signature, pub_key)
        return True
    except rsa.pkcs1.VerificationError:
        return False


def str_to_public_key(pk_str):
    """Converts the given string to a PublicKey object."""
    return rsa.PublicKey.load_pkcs1(pk_str, 'PEM')


def key_to_fingerprint(key):
    """Converts the given key (as a base64 encoded string) into a
    fingerprint."""
    return hashlib.md5(key).hexdigest()
