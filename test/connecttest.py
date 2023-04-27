import pymysql
import decimal
import rsa
# -*- coding: utf-8

conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='11911707',
            database='50q'     
        )

cursor = conn.cursor()
# query = "select * from SCORE where degree between 60 and 80"
# query = "select * from SCORE where CNO='3-105';"
query = "select SNAME, SSEX from STUDENT where SNO= 101"
query = "select * from SCORE where SNO=101;"
cursor.execute(query)


result = cursor.fetchall()
cursor.close()
conn.close()

result = tuple(tuple(float(x) if isinstance(x, decimal.Decimal) else x for x in tpl) for tpl in result)
print(type(result))

print(result)

data = tuple(float(str(x))if isinstance(x,decimal.Decimal) else x for x in result)
print(data)
(pubkey, privkey) = rsa.newkeys(2048)
ciphertext = rsa.encrypt(str(data).encode('utf-8'),pubkey)

plaintext = rsa.decrypt(ciphertext,privkey)
result = eval(plaintext.decode('utf-8'))
print(result)