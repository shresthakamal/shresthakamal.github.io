def parse_certificate(certificate, **kwargs):
    """
    Contains the entire certificate in JSON
    """


def get_key_from_store(name_of_CA):
    """
    Returns Public key based on the name of Certificate Authority
    """


def parse_key(key):
    """
    Parses p,q,n,e,d based on the values of key
    """


def query_CRL(URL, SN):
    """
    Returns the revocation status by looking at the CRL list
    """


def query_OCSP(URL, SN):
    """
    Returns the revocation status by querying the OCSP Server
    """


def myCertChecker(digital_certificate, today, domain_name):
    """
    Function to check the validity of the digital certificate

    1. Integrity Check: Verification of the Signature
    2. Validity of the Certificate
    3. Revocation Status Check
    4. Verification of Common Name and Subject's Alternative Name
    """

    """Generate message digest using tbs"""

    # Get the tbsCertificate from the digital_certificate
    tbsCertificate = parse_certificate(digital_certificate, tbs=True)

    # Get the Signature Hash and Signing Algorithm
    hash, encryption = parse_certificate(digital_certificate, sign_algorithm=True)

    # Use the information of hash and tbs to get the message digest
    message_digest_from_tbs = hash(tbsCertificate)

    """Generate Message Digest from Signature Value"""

    # Get Signature Value from digital_certificate
    sign_value = parse_certificate(digital_certificate, sign=True)

    # Get the public key of the Certificate Authority from root stores
    pub_key = get_key_from_store(parse_certificate(digital_certificate, name_CA=True))

    # Parse the values of (n,e) from public key
    n, e = parse_key(pub_key)

    # Generate the message digest using the signatue value from certificate
    message_digest_from_sign = (sign_value**e) % n

    """ Verify the integrity of the certificate: No Certificate Tampering"""
    if message_digest_from_tbs == message_digest_from_sign:

        valid_from, valid_to = parse_certificate(digital_certificate, validity=True)

        """ Checking the Validity of the certificate"""
        if valid_from < today and valid_to >= today:

            serial_no = parse_certificate(digital_certificate, sn=True)

            # Querying CRL Distribution Points to check the revocation status
            crl_path = parse_certificate(digital_certificate, crl_path=True)
            CRL_revocation_status = query_CRL(crl_path, serial_no)

            # Querying OCSP Server to check the revocation status
            ocsp_server = parse_certificate(digital_certificate, ocsp_server=True)
            OCSP_revocation_status = query_OCSP(ocsp_server, serial_no)

            """ Checking the Revocation Status"""
            if CRL_revocation_status and OCSP_revocation_status:
                cn, sans = parse_certificate(digital_certificate, cn_sans=True)

                """Verification of Common Name and Subject's ALternative Name"""
                if domain_name == cn or domain_name in sans:

                    # Certificate is VAID
                    return True
            else:
                # Certificate has been revoked.
                return False
        else:
            # Certificate has expired.
            return False
    else:
        # Certificate has been compromised.
        return False


# MAIN FUNCTION

myCertChecker(_.wikipedia.org, "2022-01-30 06:42:55.581381", "en.wikipedia.org")
