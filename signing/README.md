# Signing / التوقيع

The release APK is signed with a P-256 (EC, secp256r1) key.

- `natigati-cert.pem` — the signing certificate (public, also embedded in every APK). SHA-256: `ff2dbfde2b3f88c2c708cdd5780fe128bd79d2453500f01faeb466bf6ee8a4a8`
- The private key is a 32-byte scalar stored as base64 (44 chars) in the owner vault entry "Natigati Android release signing key". Never commit it.

Rebuild the signing store (needs Python `cryptography`):

```bash
# 1) write the base64 scalar from the vault to /tmp/natigati-scalar.b64
# 2) run:
KSPASS=<new-random-pass> python3 mkpkcs12.py
# 3) point android/keystore.properties at signing/natigati-release.p12 with that password
```

`mkpkcs12.py` verifies the scalar matches this certificate before writing the store.
