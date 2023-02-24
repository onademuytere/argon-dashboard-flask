def plustwo():
    out = 1 + 2
    return out


def falldist(t,g=9.81):
    d = 0.5 * g * t**2
    return d


def getRooms():
    rooms = []
    docs = None
    docs = db.collection(u'room').stream()
    if docs:
        for doc in docs:
            rooms.append(doc.to_dict())
        return rooms
    else:
        return None
