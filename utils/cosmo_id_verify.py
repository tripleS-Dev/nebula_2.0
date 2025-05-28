from bot_core import auto_complete
import db

def cosmo_id_verify(action, cosmo_id):
    verify = auto_complete.cosmo_id(action, cosmo_id, True)[0].value
    #print(verify)
    if '|' in verify:
        if verify.split('|')[0].lower() == cosmo_id.lower():
            return verify
        else:
            return 'The account does not exist.'
    else:
        return 'The account does not exist.'
