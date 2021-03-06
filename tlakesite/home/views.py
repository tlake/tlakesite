from __future__ import print_function

from django.views.generic import ListView
from .models import HomePageMessage, ResumeFolderID

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


class HomePageView(ListView):
    model = HomePageMessage
    template_name = 'home.html'

    def resume_link(self):
        try:
            _folder_id = ResumeFolderID.objects.first().folder_id
        except AttributeError:
            _folder_id = None

        def _get_credentials():
            """Gets valid user credentials from storage.

            If nothing has been stored, or if the stored credentials are
            invalid, the OAuth2 flow is completed to obtain the new
            credentials.

            Returns:
                Credentials, the obtained credential.
            """
            try:
                import argparse
                flags = tools.argparser.parse_args(args=[])
            except ImportError:
                flags = None

            # client_secret.json is not part of project; it must be created
            # on the machine itself.
            # See https://developers.google.com/drive/v2/web/quickstart/python
            # for details.

            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')

            SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
            CLIENT_SECRET_FILE = os.path.join(credential_dir, 'client_secret.json')
            APPLICATION_NAME = 'Drive API Python Quickstart'

            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir,
                                           'drive-python-quickstart.json')

            store = oauth2client.file.Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                flow = client.flow_from_clientsecrets(
                    CLIENT_SECRET_FILE, SCOPES)
                flow.user_agent = APPLICATION_NAME
                if flags:
                    credentials = tools.run_flow(flow, store, flags)
                else: # Needed only for compatibility with Python 2.6
                    credentials = tools.run(flow, store)
                print('Storing credentials to ' + credential_path)
            return credentials

        def _get_file_id(service, folder_id):
            """ Returns the ID of the first file found inside the
            folder designated by folder_id.
            """
            files = service.files().list(
                        q="'0B6D4ecmbxciiekhzYXRHQ2duelU' in parents"
                    ).execute()
            return files.get('files')[0]['id']


        credentials = _get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        file_id = _get_file_id(service, _folder_id)

        return "https://drive.google.com/file/d/" + file_id + "/view"
