import rsa
import sys
import base64
import gzip


def main():
    msg = sys.argv[1].encode("utf-8")
    pubkey = b"-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCNVXuPwxPKJiT+fIOJdbZpSKMeovOuiN68Ckx+9VMGM3UfsDv/553ccqQB\nZP/M+CgNyTdCXXgWeM15bktLvsgdAgMBAAE=\n-----END RSA PUBLIC KEY-----"
    pub = rsa.PublicKey.load_pkcs1(pubkey)
    if pub:
        signed_msg = rsa.encrypt(msg, pub)
        # print(signed_msg)
        # base64_signed_msg = base64.b64encode(signed_msg).decode("utf-8")
        base64_signed_msg = base64.b64encode(signed_msg).decode("utf-8")
        print(base64_signed_msg)


if __name__ == "__main__":
    main()
