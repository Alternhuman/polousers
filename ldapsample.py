import ldap
 
l = ldap.initialize("ldap://ldap1.cie.aulas.usal.es")
try:
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
 
    bind = l.simple_bind_s("", "")
 
    base = "dc=DIA"
    criteria = "(&(objectClass=*)(sAMAccountName=i0825993))"
    attributes = ['name']
    result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
    results = [entry for dn, entry in result if isinstance(entry, dict)]
    print(results)
finally:
    l.unbind()