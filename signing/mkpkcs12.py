import base64, sys, os
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import pkcs12

# reads scalar from /tmp/natigati-scalar.b64, cert from natigati-cert.pem
# writes natigati-release.p12 with password from env KSPASS
scalar=base64.b64decode(open('/tmp/natigati-scalar.b64').read().strip())
key=ec.derive_private_key(int.from_bytes(scalar,'big'),ec.SECP256R1())
cert=x509.load_pem_x509_certificate(open('natigati-cert.pem','rb').read())
# consistency: derived pubkey must equal cert pubkey
assert key.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)==cert.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo),'scalar does not match cert'
blob=pkcs12.serialize_key_and_certificates(b'natigati',key,cert,None,serialization.BestAvailableEncryption(os.environ['KSPASS'].encode()))
open('natigati-release.p12','wb').write(blob)
print('p12 written, cert sha256',cert.fingerprint(hashes.SHA256()).hex())
