
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spotify-d5016-default-rtdb.europe-west1.firebasedatabase.app'
})
# Get a reference to the root of the database
root = db.reference()

# Write data to the database
# root.child('users').push({
#     'name' : 'Mary Anning1', 
#     'since' : 1701
# })
# Read data from the database
# users_ref = root.child('users')
# users = users_ref.get()
# print(users)

# Get a reference to the "users" node
users_ref = db.reference('users')


# Query 3: Filter by child property "age" greater than 18
# query3 = users_ref.order_by_child('since').start_at(1702).get()
# print('Query 3:')
# print(query3)

# Query users where username and password are equal
query = users_ref.order_by_child('username').equal_to('izzy').get()
# Filter the query results by password
results = [user for user in query.values() if user.get('password') == 'izzy123']

print('Query results:')
print(results)
