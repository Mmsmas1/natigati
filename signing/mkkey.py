import base64, datetime, sys
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import pkcs12

SCALAR_B64_FILE='/tmp/natigati-scalar.b64'
mode=sys.argv[1]
if mode=='generate':
    key=ec.generate_private_key(ec.SECP256R1())
    scalar=key.private_numbers().private_value.to_bytes(32,'big')
    open(SCALAR_B64_FILE,'w').write(base64.b64encode(scalar).decode()+'\n')
else:
    key=ec.derive_private_key(int.from_bytes(base64.b64decode(open(SCALAR_B64_FILE).read().strip()),'big'),ec.SECP256R1())

name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Mohamed Abu Soliman'),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME,'Natigati')])
nb=datetime.datetime(2026,11,24,tzinfo=datetime.timezone.utc)
cert=(x509.CertificateBuilder()
  .subject_name(name).issuer_name(name)
  .public_key(key.public_key())
  .serial_number(0x4E41544947415449)  # 'NATIGATI'
  .not_valid_before(nb)
  .not_valid_after(nb+datetime.timedelta(days=10000))
  .sign(key,hashes.SHA256()))
open('natigati-cert.pem','wb').write(cert.public_bytes(serialization.Encoding.PEM))
open('natigati-pubkey.pem','wb').write(key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
print('cert_sha256',cert.fingerprint(hashes.SHA256()).hex())
