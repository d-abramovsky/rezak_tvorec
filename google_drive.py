from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

direct_creds = 'credentials_module.json'

def login_googledrive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(direct_creds)
    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(direct_creds)
    else:
        gauth.Authorize()
    return GoogleDrive(gauth)

def backup_googledrive(file_id):
    creds = login_googledrive()
    file = creds.CreateFile({'title': f'{file_id}', 'parents':[{'kind': 'drive#fileLink', 'id': '1mNgNf6hmvHsS_bQPlgjMe1O_sNfpwKPB'}]})
    file.SetContentFile(f'{file_id}')
    file.Upload()
