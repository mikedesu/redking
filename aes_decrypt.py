#!/usr/bin/env python3
import rsa
import sys
import base64
from cryptography.fernet import Fernet


def main():
    # key = sys.stdin.read().encode("utf-8")
    key = sys.argv[1].encode("utf-8")
    # read msg from stdin
    msg = sys.stdin.read().encode("utf-8")
    cipher = Fernet(key)
    # encrypted_msg = cipher.encrypt(msg).decode("utf-8")
    decrypted_msg = cipher.decrypt(msg).decode("utf-8")
    print(decrypted_msg)


if __name__ == "__main__":
    main()
