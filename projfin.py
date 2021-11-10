from __future__ import print_function
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import random
from decimal import Decimal

FIELD_SIZE = 10 ** 3

SCOPES = ['https://www.googleapis.com/auth/drive']


def drive_init():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service


def search_file(service):
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)",
                                   q="name='encrypted.txt'").execute()
    items = results.get('files', [])
    op = ""

    if not items:
        print('No files found.')
    else:
        print('The File has been found.')
        for item in items:
            # print(u'{0} ({1})'.format(item['name'], item['id']))
            print(f"File Name : {item['name']} File ID : {item['id']}")
            op = item['id']
    return op


def upload_file(service):
    # Uploading a File
    file_metadata = {'name': "encrypted.txt"}
    filePath = "encrypted.txt"
    media = MediaFileUpload(filePath, mimetype="text/plain")
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    fileID = file.get('id')
    print('File ID: ' + fileID)


def download_file(service, fileid):
    # Downloading A File
    print(f"The file is being downloaded. It will be stored in the downloads folder.")
    request = service.files().get_media(fileId=fileid)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open("Downloads/encrypted.txt", "wb") as f:
        fh.seek(0)
        f.write(fh.read())


def reconstruct_secret(shares):
    sums = 0
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi) / (xi - xj))
        prod *= yj
        sums += Decimal(prod)
    return int(round(Decimal(sums), 0))


def polynom(x, coeffs):
    point = 0
    for coefficient_index, coefficient_value in enumerate(coeffs[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def coeff(t, secret):
    coeffs = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeffs.append(secret)
    return coeffs


def create_shares(a, b, secret):
    coeffs = coeff(b, secret)
    shares = []
    for i in range(1, a + 1):
        x = i
        shares.append((x, polynom(x, coeffs)))
    return shares


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def encrypt():
    p = 17
    q = 19
    n = p * q
    totient = (p - 1) * (q - 1)
    e = d = -1
    ct = 0
    for i in range(2, totient):
        if ct == 1:
            break
        if gcd(i, totient) == 1:
            e = i
            ct += 1
    ed = 1
    while True:
        ed = ed + totient
        if ed % e == 0:
            d = int(ed / e)
            break

    num = int(input("Enter the total number of shares you wish to make : "))
    threshold = int(input("Enter the threshold number of shares required to reconstruct the key : "))
    shares = create_shares(num, threshold, d)
    print(f"\nThe shares are as follows : \n{shares}\nPlease store them securely.\n")

    with open("input.txt", "r", encoding='utf8') as fin:
        message = fin.read()
    print(f"The message in the file is :\n{message}")
    msg = [ord(i) for i in message]
    enc = [pow(i, e, n) for i in msg]
    print("\nThe encrypted message is :")
    with open("encrypted.txt", "w", encoding='utf8') as fout:
        for i in enc:
            fout.write(chr(i))
            print(chr(i), end="")


def decrypt():
    p = 17
    q = 19
    n = p * q

    t = int(input('Enter the number of shares you have :'))
    print()
    shares = []
    for i in range(t):
        ind = int(input("Enter the index number of the share : "))
        val = int(input("Enter the value of the share : "))
        print()
        shares.append((ind, val))
    # print(reconstruct_secret(shares))
    d = reconstruct_secret(shares)

    with open("Downloads/encrypted.txt", "r", encoding='utf8') as fin:
        encmsg = fin.read()
    print(f"\nThe encrypted message is :\n{encmsg}")
    enc = [ord(i) for i in encmsg]
    dec = [pow(i, d, n) for i in enc]
    print("\nThe decrypted message is :")
    with open("decrypted.txt", "w", encoding='utf8') as fout:
        for i in dec:
            fout.write(chr(i))
            print(chr(i), end="")
    print()


def main():
    service = drive_init()
    choice = int(input("MENU\n1.Encryption & File Upload\n2.File Retrieval & Decryption\n\nEnter your choice : "))
    if choice == 1:
        encrypt()
        upload_file(service)
    elif choice == 2:
        id = search_file(service)
        download_file(service, id)
        decrypt()


main()
