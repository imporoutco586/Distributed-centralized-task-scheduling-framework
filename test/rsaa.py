import rsa

(pubkey1, privkey1) = rsa.newkeys(512)
(pubkey2, privkey2) = rsa.newkeys(512)
(pubkey3, privkey3) = rsa.newkeys(512)

with open('pubkey1.pem', 'w+') as f:
    f.write(pubkey1.save_pkcs1().decode())

with open('privkey1.pem', 'w+') as f:
    f.write(privkey1.save_pkcs1().decode())

with open('pubkey2.pem', 'w+') as f:
    f.write(pubkey2.save_pkcs1().decode())

with open('privkey2.pem', 'w+') as f:
    f.write(privkey2.save_pkcs1().decode())

with open('pubkey3.pem', 'w+') as f:
    f.write(pubkey3.save_pkcs1().decode())

with open('privkey3.pem', 'w+') as f:
    f.write(privkey3.save_pkcs1().decode())
