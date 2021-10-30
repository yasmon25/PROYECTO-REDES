from pymongo import MongoClient
from datetime import datetime

MONGO_URI = 'mongodb://localhost'
client = MongoClient(MONGO_URI)

# La base de datos se llama project
db = client['project']

# user es un objeto json
# user = {_id: {{username}}, username: {{username}}, password: {{password}}, 
#         date_added: {{date_added}}}
def new_user(username, password):

    now = datetime.now()

    second = '0' + str(now.second) if now.second < 10 else str(now.second)
    minute = '0' + str(now.minute) if now.minute < 10 else str(now.minute)
    hour = '0' + str(now.hour) if now.hour < 10 else str(now.hour)

    day = '0' + str(now.day) if now.day < 10 else str(now.day)
    month = '0' + str(now.month) if now.month < 10 else str(now.month)

    date = day + '/' + month + '/' + str(now.year) + ' ' + hour + ':' + minute + ':' + second

    user = {
            '_id': username, 
            'username': username, 
            'password': password, 
            'date_added': date}    
    users = db['user']

    try:
        users.insert_one(user)
        return ' '
    except ValueError:
        return 'ERROR (new_user): ' + ValueError
        

# Devuelve todos los usuarios de la colección
def get_users():
    users = db['user']
    return users.find()

# Devuelve un usuario de la colección
def get_user(username, password):
    users = db['user']
    return users.find_one({"username": username, "password": password})   

# Actualiza un usuario por su _id
def update_user(_id, username, password):
    users = db['user']
    try:
        new_data = {"username": username, "password": password}
        users.update_one({'_id': _id}, {"$set": new_data})
        return ' '
    except ValueError:
        return 'ERROR (update_user): ' + ValueError

# Elimina un usuario por su _id
def delete_user(_id):
    users = db['user']
    try:
        users.delete_one({'_id': _id})
        return ' '
    except ValueError:
        return 'ERROR (delete_user): ' + ValueError
    

if __name__ == '__main__':
    
    users = db['user']
    results = users.find()
    for result in results:
        print(result)























