# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import Flask, session, render_template, request, redirect, jsonify
#from functions import plustwo

from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "bachelorproef-2223",
  "private_key_id": "779aaa5392797f56f0043ef742f870470d876902",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCkAenYU0tpmkGr\nGlmFAk1ttcqq2UkjHOJkON7/unD2ejtPFkmOSs0L1cqlvZ5kVTGyjpbVjP2JS7Sw\ngvlBnCu65Od0GBWE5yIOf5aS41UUTqppyXu4yUp7ObRZeRJ2alQzrQJBJA2hIc/A\n50IBK9vn9Zcuec0AwR1RbfUwGVZtlD6BICxJ8AKSRagmvj2GGqHVurMP+mmNRtS9\nw+v4XHnPNqeMq0CfjwoYgPEzwQj3CXCgMph3aNp+TngvexWD9hiumhH/M7iiej9j\nfSFIx8S66qqPL/d15B0QH3QVVdwWbNFjHP9G2OoiF2ExES/Cf/XTChH/Gz0qVDrb\nsrw4wQ9ZAgMBAAECggEAULQkVu+95ywh7klcDahxY3AWV3XumFmpSXn2uc4Lsi25\nq5QjA+Lo/U7plh81pteJSf0CWfkz9XCMbGM2tkNb/W6QOj9zr19xEcNU29kDz6da\nEg40VFywyuw9Q93g6OYvovIabuWH02do7NqfTyY+4uilyRfked+NRrmd8lo1fluv\nmDgyLzwkcxn5Ee6ZtoqJRNIIRuE3C++Q+iV18tRxMVDKxNyVE0FgIUnmqmvLbBmT\nezs+dJ6JpordaS5d0AgnsRmyRPs6yU6n8z1dGs3nL9hp27kBdm/UlM1MtlZ39bVv\nivDR/sAUtfv7SuVoqBpzf8DZYPHjc8ID5tV63xlwhQKBgQDTZ4sfikdT5XPI3SSr\nhZu7SPbEHr3K2kupVh+fHRXI5J8rarKqkaaC0afw4zNqZ57bGnqQz/S8IQi1hlJ3\nOR9H7JUddO4UACwRkOtRE4BjAsw5/tUC0iDSDY0C6YcN8/xodwOzTnvT6Lykt4je\n0b878yGM5mLVYm5YIlpqQGeeOwKBgQDGmstiP3hC+aSFDexB+8M159CBupYLb5Kf\nratdT2jLJW4WGvmD8tHKT1FIGv+M07mOkeoHAReWpM7IVhQzhR0qj6HgD+JmtB+K\nM1eRWhSVxa46K4hsoWcjUFoNgGd0fJcnhCUR1X+RG3o1iKIkjcEaMgziRvNR3b+L\n89CiZUqLewKBgQDRuU8ToyLP4DnVc04Fuy6bxe7I8ZZnv9h/zajhOQF7oxMlB1zo\nSkZeUY/CMiO308SMqOAe+a9ZU4xISVFWZZzaxaHI70+hF+qgIpzQegBMOWJRxrWb\nbsqQmFDkKriI5xvopulM4PeHasR6xHlMU9jbqIAIQCacemHtnWcFMY+aMQKBgQCI\nqCTAYtn2g96fqzfhI0JsiikfyurJzaj/dLnQh/6cohHA5ijAkUmnwrI0QleLaHhq\n0J5O2YKIpriegxR9at/p1FFXYravYsu9BZ0AqBI4CIDdB+1kih703qpIVg1Zyw0b\nJMN5JQYVK+oIgg7Hxj6ULtJMtPNiZooR29+4jqgflwKBgQCbN5QrQNIVHh1V8JMQ\nF1kGc9xC0zt1UhkrTmCavb0aQBcLHfn2eFMef1aOe04by/JwYLZrZuiEfUZ/HFae\nZOVBzWIYUeLbjFJ8iQsCKFELyqXQZ8czIJzYii7LtNsJVgGXAoJJppf3XGMjgA6j\nNX2UgeEwwPxmVKV2/JU3zz+q3A==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-vsza3@bachelorproef-2223.iam.gserviceaccount.com",
  "client_id": "118238777985434336465",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vsza3%40bachelorproef-2223.iam.gserviceaccount.com"
})
default_app = initialize_app(cred)
db = firestore.client()
general_parameters = db.collection('general_parameters')


"""
put the below functions in another py file (functions.py) and connect them
"""


def get_rooms():
    rooms = []
    docs = None
    docs = db.collection(u'room').stream()
    if docs:
        for doc in docs:
            rooms.append(doc.to_dict())
        return render_template('home/rooms.html', segment='rooms', acc=rooms)
    else:
        return render_template('home/rooms.html', segment='rooms', acc="hey")
    
"""
end 
"""

@blueprint.route('/rooms')
@login_required
def index():
    rooms = []
    docs = None
    docs = db.collection(u'room').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            dict["id"] = doc.id
            rooms.append(dict)
        return render_template('home/rooms.html', segment='rooms', rooms=rooms)
    else:
        return render_template('home/rooms.html', segment='rooms', rooms="hey")


@blueprint.route('/room-detail/<room_id>')
@login_required
def room(room_id):
    doc_ref = db.collection(u'room').document(room_id)
    doc = doc_ref.get()
    if doc.exists:
        dict = doc.to_dict()
        dict["id"] = room_id
        schemes = []
        docs = db.collection(u'scheme').where(u'room_id', u'==', room_id).stream()
        if docs:
            days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            for doc in docs:
                schemes.append(doc.to_dict())
            return render_template('home/room-detail.html', segment='room-detail', room=dict, schemes=schemes, 
                                   days_of_week=days_of_week)
        else:
            return render_template('home/room-detail.html', segment='room-detail', room=dict, schemes=[], 
                                   days_of_week="")
    else:
        return render_template('home/room-detail.html', segment='room-detail', room="none")


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        """if template == "rooms.html":
            doc = general_parameters.document("parameters").get()
            if doc.exists:
                params = doc.to_dict()
                return render_template("home/" + template, segment=segment, accuracy="success")
            else:
                return render_template("home/" + template, segment=segment, accuracy="fail")
        else:
            return render_template("home/" + template, segment=segment, accuracy="not rooms")"""
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
