#!/usr/bin/env python3
import rsa
import sys
import base64


def main():
    # read msg from stdin
    msg = sys.stdin.read().encode("utf-8")
    private_key_bytes = b"-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAI1Ve4/DE8omJP58g4l1tmlIox6i866I3rwKTH71UwYzdR+wO//n\nndxypAFk/8z4KA3JN0JdeBZ4zXluS0u+yB0CAwEAAQJAPAKm42TuWzAVFyVhaJVd\nrZiVAmYoV9xvzqIE1wdtRzbFKVPIXlAfJIoOFb5u+QQ8k96zAC6xbuc9Tl54lLhX\nwQIjAJkluAmy4dW75s63d/rS1hMZ0UI5zXVmHU3pmmBCc83K2fECHwDsQLVSJa7h\nZBcplVu+ld4H2QRS2WJajpfJ667/RO0CIwCUlDGOx0uurtPoLbtrTu1+LogEdkvM\n4DsCAedSCGaNe4YhAh8A1dOrSPJ6Wd1xaV2Zb+HM12WAGExQTI4Kq+L4vGnxAiJ+\n/05NOZ9gfWGFrOHfKI8GIlYPjeDlxud/ZkijKAuO9SjX\n-----END RSA PRIVATE KEY-----"
    # pub = rsa.PublicKey.load_pkcs1(pubkey)
    priv = rsa.PrivateKey.load_pkcs1(private_key_bytes)
    if priv:
        msg = base64.b64decode(msg)
        decrypted_msg = rsa.decrypt(msg, priv).decode("utf-8")
        print(decrypted_msg)
        # signed_msg = rsa.encrypt(msg, pub)
        # print(signed_msg)
        # base64_signed_msg = base64.b64encode(signed_msg).decode("utf-8")
        # base64_signed_msg = base64.b64encode(signed_msg).decode("utf-8")
        # print(base64_signed_msg)


if __name__ == "__main__":
    main()
