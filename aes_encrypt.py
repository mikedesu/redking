#!/usr/bin/env python3
import rsa
import sys
import base64
from cryptography.fernet import Fernet


def main():
    # read key from stdin
    key = sys.stdin.read().encode("utf-8")
    msg = sys.argv[1].encode("utf-8")
    cipher = Fernet(key)
    encrypted_msg = cipher.encrypt(msg).decode("utf-8")
    print(encrypted_msg)


if __name__ == "__main__":
    main()
