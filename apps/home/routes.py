# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
import tempfile
from apps.home import blueprint
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import Flask, session, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
#from firestoreFunctions import plustwo
from firebase_admin import credentials, firestore, initialize_app, storage


# configuration for realtime database
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
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vsza3%40bachelorproef-2223.iam.gserviceaccount.com",
})
default_app = initialize_app(cred, {
    'storageBucket': 'bachelorproef-2223.appspot.com'})
db = firestore.client()
bucket = storage.bucket()
general_parameters = db.collection('general_parameters')
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

"""
put the below functions in another py file (functions.py) and connect them
"""

# All room functions
def getRooms():
    rooms = []
    docs = None
    docs = db.collection(u'room').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            dict["id"] = doc.id
            rooms.append(dict)
        return rooms
    else:
        return docs


def getRoomById(room_id):
    doc_ref = db.collection(u'room').document(room_id)
    doc = doc_ref.get()
    schemes = []
    if doc.exists:
        dict = doc.to_dict()
        dict["id"] = room_id
        docs = db.collection(u'scheme').where(u'room_id', u'==', room_id).stream()
        if docs:
            for doc in docs:
                dict_scheme = doc.to_dict()
                dict_scheme["id"] = doc.id
                schemes.append(dict_scheme)
        return schemes, dict
    else:
        return schemes, []


def addRoom(name, location):
    data = {
        u'roomname': name,
        u'location': location,
    }
    db.collection(u'room').add(data)


def editRoom(req, room_id):
    dict = {}
    if req['name']:
        name = req['name']
        dict['roomname'] = name
    if req['location']:
        location = req['location']
        dict['location'] = location

    room_ref = db.collection(u'room').document(room_id)
    room_ref.update(dict)


def deleteRoom(room_id):
    # first delete the schemes associated with this room
    doc_ref = db.collection(u'scheme').where(u'room_id', u'==', room_id).get()

    if doc_ref:
        batch = db.batch()
        for doc in doc_ref:
            batch.delete(doc.reference)
        batch.commit()

    # delete the room itself
    db.collection(u'room').document(room_id).delete()


# All users functions
def getUserById(user_id):
    doc_ref = db.collection(u'user').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        user = doc.to_dict()
        return user
    else:
        return None


def getUsersByGroup(group_id):
    users = []
    doc = db.collection(u'user').stream()
    if doc:
        for user in doc:
            dict = user.to_dict()
            for group in dict["group_id"]:
                if group == group_id:
                    dict["id"] = user.id
                    users.append(dict)
        return users
    else:
        return None


def addUserToGroup(userid, groupid):
    print("test user added to group")
    data = {
        u'group_id': firestore.ArrayUnion([groupid])
    }
    db.collection(u'user').document(userid).update(data)


# All scheme functions
def addScheme(schedule_week, group_id, room_id):
    data = {
        u'assigned_to': group_id,
        u'room_id': room_id,
        u'schemename': "Test scheme name"
    }

    for key in schedule_week:
        data[key] = schedule_week[key]

    db.collection(u'scheme').add(data)


def deleteScheme(scheme_id):
    # delete the scheme
    db.collection(u'scheme').document(scheme_id).delete()


# All user functions
def getUsers():
    users = []
    docs = None
    docs = db.collection(u'user').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            dict["id"] = doc.id
            classname = ""
            if dict["is_teacher"] is False:
                # classname = getGroupById(dict["class_id"])
                classname = getClassById(dict["class_id"])
            dict["classname"] = classname
            users.append(dict)
        return users
    else:
        return None


# All students
def getStudents():
    students = []
    docs = None
    docs = db.collection(u'user').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            if dict["is_teacher"] is False:
                dict["id"] = doc.id
                classname = getClassById(dict["class_id"])
                dict["classname"] = classname
                students.append(dict)
        return students
    else:
        return None


# All teachers
def getTeachers():
    teachers = []
    docs = None
    docs = db.collection(u'user').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            if dict["is_teacher"] is True:
                dict["id"] = doc.id
                teachers.append(dict)
        return teachers
    else:
        return None


# All classes
def getDefaultGroups():
    classes = []
    docs = None
    docs = db.collection(u'group').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            if dict["is_class"] is True:
                dict["id"] = doc.id
                if doc.id == "cUJpi7aQjwQ60VHw1sZE":
                    teachers = db.collection(u'user').where(u'is_teacher', u'==', True).stream()
                    if teachers:
                        amount = len(list(teachers))
                        dict["number"] = amount
                    classes.append(dict)
                else:
                    number = db.collection(u'user').where(u'class_id', u'==', doc.id).stream()
                    if number:
                        amount = len(list(number))
                        dict["number"] = amount
                    classes.append(dict)
        return classes
    else:
        return None


# All nonclasses
def getNonDefaultGroups():
    nonclasses = []
    docs = None
    docs = db.collection(u'group').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            if dict["is_class"] is False:
                # number = db.collection(u'user').where(u'group_id', u'==', doc.id).stream()
                users = db.collection(u'user').stream()
                amount = 0
                if users:
                    for user in users:
                        info = user.to_dict()
                        if info["group_id"]:
                            for group in info["group_id"]:
                                if group == doc.id:
                                    amount += 1

                dict["id"] = doc.id
                dict["number"] = amount
                nonclasses.append(dict)
        return nonclasses
    else:
        return None


# All groups
def getAllGroups():
    groups = []
    docs = None
    docs = db.collection(u'group').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            dict["id"] = doc.id
            groups.append(dict)
        return groups
    else:
        return None


def getGroupById(group_id):
    doc_ref = db.collection(u'group').document(group_id)
    doc = doc_ref.get()
    schemes = []
    if doc.exists:
        dict = doc.to_dict()
        dict["id"] = group_id
        docs_scheme = db.collection(u'scheme').where(u'assigned_to', u'==', group_id).stream()
        if docs_scheme:
            for doc_scheme in docs_scheme:
                dict_scheme = doc_scheme.to_dict()

                dict_scheme["id"] = doc_scheme.id
                schemes.append(dict_scheme)

        return schemes, dict
    else:
        return schemes, []

def getClassById(class_id):
    doc_ref = db.collection(u'group').document(class_id)
    doc = doc_ref.get()
    if doc.exists:
        dict = doc.to_dict()
        groupname = dict["groupname"]
        return groupname


def deleteGroup(group_id):
    # first delete the schemes associated with this room
    doc_scheme = db.collection(u'scheme').where(u'assigned_to', u'==', group_id).get()

    if doc_scheme:
        batch = db.batch()
        for doc in doc_scheme:
            batch.delete(doc.reference)
        batch.commit()

    # delete the group where user is assigned to
    all_users = getUsers()
    for user in all_users:
        print(user["id"])
        user_ref = db.collection(u'user').document(user["id"])

        user_ref.update({u'group_id': firestore.ArrayRemove([group_id])})


    # delete the room itself
    db.collection(u'group').document(group_id).delete()


def getLogs():
    logs = []
    docs = None
    docs = db.collection(u'logging').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            dict["id"] = doc.id
            dict["date"] = doc.to_dict()['datetime'].date()
            dict["time"] = doc.to_dict()['datetime'].strftime("%H:%M:%S")
            user = getUserById(dict['user_id'])
            if user is None:
                dict["name"] = dict['user_id']
            else:
                dict["name"] = user['lastname'] + " " + user['firstname']
            scheme, room_info = getRoomById(dict['room_id'])
            if room_info is None:
                dict["room"] = "Unknown"
            else:
                dict["room"] = room_info['roomname']

            logs.append(dict)
        return logs
    else:
        return None

def getHistoryRoom(room_id):
    logs = []
    docs = None
    docs = db.collection(u'logging').stream()
    if docs:
        for doc in docs:
            dict = doc.to_dict()
            if dict["room_id"] == room_id:
                dict["id"] = doc.id
                dict["date"] = doc.to_dict()['datetime'].date()
                dict["time"] = doc.to_dict()['datetime'].strftime("%H:%M:%S")
                user = getUserById(dict['user_id'])
                if user is None:
                    dict["name"] = dict['user_id']
                else:
                    dict["name"] = user['lastname'] + " " + user['firstname']
                scheme, room_info = getRoomById(dict['room_id'])
                if room_info is None:
                    dict["room"] = "Unknown"
                else:
                    dict["room"] = room_info['roomname']

                logs.append(dict)
        return logs
    else:
        return None

def getParameters():
    parameters = db.collection(u'general_parameters').document(u'parameters').get()
    if parameters.exists:
        params = parameters.to_dict()
        return params["minimum_accuracy"], params["unlock_seconds"]

def editParameters(req):
    dict_params = {}
    if req['accuracy']:
        accuracy = req['accuracy']
        dict_params['minimum_accuracy'] = int(accuracy)
        dict_params['retrain_model'] = True
    if req['seconds']:
        seconds = req['seconds']
        dict_params['unlock_seconds'] = int(seconds)

    params_ref = db.collection(u'general_parameters').document(u'parameters')
    params_ref.update(dict_params)


def allowed_file(filename):
    allowed_ext = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext


"""
end 
"""


@blueprint.route('/rooms', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        addRoom(request.form['name'], request.form['location'])

        # check if the post request has the file part
        """if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            temp = tempfile.NamedTemporaryFile(delete=False)
            file.save(temp.name)
            storage().put(temp.name)
            
            # Clean-up temp image
            os.remove(temp.name)
        """
        file_path = r"/Users/onademuytere/Documents/GitHub/argon-dashboard-flask/apps/static/assets/img/rooms/iot_lab.jpeg"
        blob = bucket.blob(file_path)
        blob.upload_from_file(file_path)

    if getRooms():
        rooms = getRooms()
        return render_template('home/rooms.html', segment='rooms', rooms=rooms)
    else:
        return render_template('home/rooms.html', segment='rooms', rooms="hey")


@blueprint.route('/room-detail/<room_id>', methods=['GET', 'POST'])
@login_required
def room(room_id):
    if request.method == 'POST':
        if 'name' in request.form or 'location' in request.form:
            editRoom(request.form, room_id)
        else:
            group_id = request.form.get('selectGroup')
            schedule_week = {}
            for day in days_of_week:
                print(day)
                list = []
                if request.form[f'input11{day}'] != '' and request.form[f'input12{day}'] != '':
                    listElement = request.form[f'input11{day}'] + " - " + request.form[f'input12{day}']
                    list.append(listElement)
                if request.form[f'input21{day}'] != '' and request.form[f'input22{day}'] != '':
                    listElement = request.form[f'input21{day}'] + " - " + request.form[f'input22{day}']
                    list.append(listElement)
                schedule_week[day] = list
            addScheme(schedule_week, group_id, room_id)

    if getRoomById(room_id) and getAllGroups():
        schemes, dict = getRoomById(room_id)
        groups = getAllGroups()
        return render_template('home/room-detail.html', segment='room-detail', room=dict, schemes=schemes,
                               days_of_week=days_of_week, groups=groups)
    else:
        return render_template('home/room-detail.html', segment='room-detail', room=None, schemes=None,
                               days_of_week=days_of_week, groups=None)


@blueprint.route('/room-detail/<room_id>/delete-room', methods=['GET', 'POST'])
@login_required
def room_delete(room_id):
    deleteRoom(room_id)
    if getRooms():
        rooms = getRooms()
        print("deleted")
        return render_template('home/rooms.html', segment='rooms', rooms=rooms)
    else:
        return render_template('home/rooms.html', segment='rooms', rooms=[])


@blueprint.route('/room-detail/<scheme_id>/delete-scheme', methods=['GET', 'POST'])
@login_required
def scheme_delete(scheme_id):
    deleteScheme(scheme_id)

    if getRooms():
        rooms = getRooms()
        print("deleted")
        return render_template('home/rooms.html', segment='rooms', rooms=rooms)
    else:
        return render_template('home/rooms.html', segment='rooms', rooms=[])


@blueprint.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    #if getStudents() and getTeachers() and getClasses() and getNonClasses():
    data = getUsers()
    groups = getNonDefaultGroups()

    """else:
        return render_template('home/users.html', segment='users', students=[], teachers=[], classes=[], nonclasses=[])
    """
    return render_template('home/users.html', segment='users', type="All", data=data, groups=groups)


@blueprint.route('/users/<type>', methods=['GET', 'POST'])
@login_required
def user_types(type):
    data = None
    if type == "Students":
        data = getStudents()
    elif type == "Teachers":
        data = getTeachers()
    groups = getNonDefaultGroups()
    if data is not None:
        return render_template('home/users.html', segment='users', type=type, data=data, groups=groups)
    else:
        return render_template('home/users.html', segment='users', type=None, data=None, groups=groups)


@blueprint.route('/users/<userid>/add-to-group/<groupid>', methods=['GET', 'POST'])
@login_required
def user_to_group(userid, groupid):
    addUserToGroup(userid, groupid)
    return group(groupid)
    #return render_template('home/users.html', segment='users', type=type, data=data, groups=groups)



@blueprint.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    data = getDefaultGroups()
    if data:
        return render_template('home/groups.html', segment='groups', type=type, data=data)
    else:
        return render_template('home/groups.html', segment='groups', type=None, data=None)


@blueprint.route('/groups/<type>', methods=['GET', 'POST'])
@login_required
def group_types(type):
    data = None
    if type == "Groups":
        data = getNonDefaultGroups()
    if data is not None:
        return render_template('home/groups.html', segment='groups', type=type, data=data)
    else:
        return render_template('home/groups.html', segment='groups', type=None, data=None)


@blueprint.route('/group-detail/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    if request.method == 'POST':
        room_id = request.form.get('selectGroup')
        schedule_week = {}
        for day in days_of_week:
            print(day)
            list = []
            if request.form[f'input11{day}'] != '' and request.form[f'input12{day}'] != '':
                listElement = request.form[f'input11{day}'] + " - " + request.form[f'input12{day}']
                list.append(listElement)
            if request.form[f'input21{day}'] != '' and request.form[f'input22{day}'] != '':
                listElement = request.form[f'input21{day}'] + " - " + request.form[f'input22{day}']
                list.append(listElement)
            schedule_week[day] = list
        addScheme(schedule_week, group_id, room_id)
    schemes, dict = getGroupById(group_id)
    groupmembers = getUsersByGroup(group_id)
    rooms = getRooms()
    return render_template('home/group-detail.html', segment='group-detail', schemes=schemes, group=dict,
                           groupmembers=groupmembers, days_of_week=days_of_week, rooms=rooms)

    #else:
    #    return render_template('home/group-detail.html', segment='group-detail', groupname=None)

@blueprint.route('/group-detail/<group_id>/delete-group', methods=['GET', 'POST'])
@login_required
def group_delete(group_id):
    deleteGroup(group_id)
    return group_types("Groups")


@blueprint.route('/logging')
@login_required
def logging():
    if getLogs():
        logs = getLogs()
        print("logging")
        return render_template('home/logging.html', segment='logging', logs=logs)
    else:
        return render_template('home/logging.html', segment='logging', logs=None)


@blueprint.route('/history-room/<room_id>', methods=['GET', 'POST'])
@login_required
def history_room(room_id):
    data = None
    if room_id:
        data = getHistoryRoom(room_id)
        _, dict = getRoomById(room_id)
    if data is not None:
        return render_template('home/history-room.html', segment='history-room', logs=data, dict=dict)
    else:
        return render_template('home/history-room.html', segment='history-room', data=None)


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        editParameters(request.form)
    acc, sec = getParameters()
    return render_template('home/settings.html', segment='settings', acc=acc, sec=sec)


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
