import redis
import rsa
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  



(pubkey1, privkey1) = rsa.newkeys(2048)
(pubkey2, privkey2) = rsa.newkeys(2048)
(pubkey3, privkey3) = rsa.newkeys(2048)


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






with open('pubkey1.pem') as f:
    pubkey1 = f.read().encode()
    
r.delete('pu1')
r.set('pu1', pubkey1)
st1 = r.get('pu1')
pubkey1 = rsa.PublicKey.load_pkcs1(st1)
print(pubkey1)
    
with open('pubkey2.pem') as f:
    pubkey2 = f.read().encode()
    
r.delete('pu2')
r.set('pu2', pubkey2)

with open('pubkey3.pem') as f:
    pubkey3 = f.read().encode()
    
r.delete('pu3')
r.set('pu3', pubkey3)
    
with open('privkey1.pem') as f:
    privkey1 = f.read().encode()
r.delete('pr1')
r.set('pr1', privkey1)
    
with open('privkey2.pem') as f:
    privkey2 = f.read().encode()
r.delete('pr2')
r.set('pr2', privkey2)

with open('privkey3.pem') as f:
    privkey3 = f.read().encode()
r.delete('pr3')
r.set('pr3', privkey3)