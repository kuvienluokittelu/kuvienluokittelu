# Documentation: https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html#list

import zipfile, io, os.path, json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from PIL import Image, ImageDraw
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from mimetypes import MimeTypes

SCOPE1 = "https://www.googleapis.com/auth/drive" 
SCOPE2 = "https://www.googleapis.com/auth/drive.file"
SCOPE3 = "https://www.googleapis.com/auth/drive.metadata"
scopes = [SCOPE1, SCOPE2, SCOPE3]

exampleCredentials = r'''{
    "type": "service_account",
    "project_id": "ravihevostunnistus",
    "private_key_id": "",
    "private_key": "",
    "client_email": "ravihevonen@ravihevostunnistus.iam.gserviceaccount.com",
    "client_id": "",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ravihevonen%40ravihevostunnistus.iam.gserviceaccount.com"
}'''

class GoogleDriver:
  def __init__(self, credentials):
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(credentials), scopes=scopes)
    self.service = build("drive", "v3", credentials=creds)

  def download_file(self, file_id, file_path="./model.pt", is_zip=False):
      path = file_path
      if is_zip:
        path = "./zip-file.zip"
      
      request = self.service.files().get_media(fileId=file_id)
      fh = io.FileIO(path, "wb")
      downloader = MediaIoBaseDownload(fh, request)
      done = False
      while done is False:
          status, done = downloader.next_chunk()
          print("Download %d%%." % int(status.progress() * 100))

      if is_zip:
        file = zipfile.ZipFile(path, 'r')
        file.extractall("./")

  def get_file_list(self, print_result=False):
    results = self.service.files().list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get("files", [])
    if not items:
      return []
    else:
      if print_result is True:
        print("Files and folders:")
        for item in items:
          print(u"{0}, {1}, {2}".format(item["id"], item["name"], item["mimeType"]))
      return items

  def upload_file(self,file_path, parent_id=None):
    mime = MimeTypes()
    file_name = file_path.split("/")[-1]
    file_metadata = {'name': file_name, 'yoyo': 'yoyo'}
    if parent_id:
      file_metadata['parents'] = [parent_id]
    print("Uploading to {0}/{1}...".format(parent_id, file_name))
    media = MediaFileUpload(file_path, mimetype=mime.guess_type(os.path.basename(file_path))[0], resumable=True)
    file = self.service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('Uploaded {0} successfully. File ID: {1}'.format(file_name, file.get('id')))
    return file.get('id')

  def get_folder_id(self, folder_name):
    files = self.get_file_list()
    name = list(filter(lambda file: file.get('name') == folder_name, files))
    if (len(name) == 0):
      return None
    else:
      return name[0].get("id")

  def get_newest_model_id(self):
    parent_id = self.get_folder_id("models")
    qsearch = "'{0}'".format(parent_id)
    results = self.service.files().list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)", q="{0} in parents".format(qsearch), orderBy="createdTime desc").execute()
    items = results.get("files", [])

    print(items)
    if not items:
      print("Models not found")
      return None

    print("Models found:")
    for item in items:
      print(u"{0}, {1}, {2}".format(item["id"], item["name"], item["mimeType"]))

    newest_model_id = items[0].get("id")
    return newest_model_id

if __name__ == "__main__":

  gdriver = GoogleDriver(exampleCredentials)
  newest_model_id = gdriver.get_newest_model_id()
  gdriver.download_file(newest_model_id)