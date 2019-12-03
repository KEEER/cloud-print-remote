"""
Run this file seperately will give you the key.
"""

import rsa

public, private = rsa.newkeys(4096)

with open('remote_key.pem','wb') as fw:
    fw.write(private.save_pkcs1())
    fw.close()

with open('endpoint_key.pem','wb') as fw:
    fw.write(public.save_pkcs1())
    fw.close()

print('Done.')