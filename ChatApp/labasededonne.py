import sqlite3

conn = sqlite3.connect('chatapplication.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS signup (username TEXT PRIMARY KEY, password TEXT, email TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY,sender TEXT,receiver TEXT,content TEXT,"
               "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
cursor.execute("CREATE TABLE IF NOT EXISTS room (admin TEXT , roomn TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS rooms (user TEXT , roomn TEXT)")
conn.commit()
conn.close()


def ajouter_message(sender, receiver, content):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)", (sender, receiver, content))
    conn.commit()
    conn.close()


def recuperer_historique(sender, receiver):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sender, content FROM messages WHERE (sender = ? AND receiver = ?) OR (sender = "
                   "? AND receiver = ?)", (sender, receiver, receiver, sender))
    historique = cursor.fetchall()
    conn.close()
    return historique


def recuperer_groupe(receiver):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sender, content  FROM messages WHERE receiver = ?", (receiver,))
    historique = cursor.fetchall()
    conn.close()
    return historique


def serch(nickname, code):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM signup WHERE username = ? and password= ?", (nickname, code))
    if cursor.fetchone():
        conn.close()
        return 0
    else:
        conn.close()
        return 1


def addto_data(username, password, email):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO signup (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()


def addto_data_vr(username):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT phone FROM signup WHERE username = ?", (username,))
    liste = cursor.fetchall()
    conn.close()
    return liste


def verification(nickname):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM signup WHERE username = ?", (nickname,))
    if cursor.fetchone():
        conn.close()
        return 0
    else:
        conn.close()
        return 1


def offline():
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM signup")
    liste_offline = cursor.fetchall()
    conn.close()
    return liste_offline


def change_name(newname, oldname):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE signup SET username = ? WHERE username = ?", (newname, oldname))
    cursor.execute("UPDATE messages SET sender = ? WHERE sender = ?", (newname, oldname))
    cursor.execute("UPDATE messages SET receiver = ? WHERE receiver = ?", (newname, oldname))
    cursor.execute("UPDATE rooms SET user = ? WHERE user = ?", (newname, oldname))
    conn.commit()
    conn.close()


def creerroom(admin, roomin):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO room (admin, roomn) VALUES (?, ?)", (admin, roomin))
    conn.commit()
    conn.close()


def allrooms():
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT roomn from room")
    room_names = cursor.fetchall()
    conn.close()
    return room_names


def add_to_rooms(usernom, groupnom):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rooms VALUES (?, ?)", (usernom, groupnom))
    conn.commit()
    conn.close()


def verf_room(groupnom):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user FROM rooms WHERE roomn = ?", (groupnom,))
    members = cursor.fetchall()
    conn.close()
    return members


def verf_histo():
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT roomn FROM room")
    slnom = cursor.fetchall()
    conn.close()
    return slnom





def recupere_timegr(receiver):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()

    cursor.execute("SELECT strftime('%Y', timestamp) AS years, strftime('%m', timestamp) AS months, "
                   "strftime('%d', timestamp) AS days, strftime('%H', timestamp) AS hours, "
                   "strftime('%M', timestamp) AS minutes FROM messages WHERE receiver = ?;", (receiver,))
    results = cursor.fetchall()
    conn.close()
    return results


def recupere_timepr(sender, receiver):
    conn = sqlite3.connect('chatapplication.db')
    cursor = conn.cursor()
    cursor.execute("SELECT strftime('%Y', timestamp) AS years, strftime('%m', timestamp) AS months, "
                   "strftime('%d', timestamp) AS days, strftime('%H', timestamp) AS hours, "
                   "strftime('%M', timestamp) AS minutes FROM messages WHERE (sender = ? AND receiver = ?) OR (sender ="
                   "? AND receiver = ?)", (sender, receiver, receiver, sender))
    results = cursor.fetchall()
    conn.close()
    return results