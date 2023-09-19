from fastapi import FastAPI, Depends
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
import uuid

app = FastAPI()
SECRET = str(uuid.uuid4())
# SECRET = "0f5c66455b5470b06a301d1ff5c55cf75931657525f505bd"
manager = LoginManager(SECRET, '/login')

DB = {
    'users': {
        'johndoe@mail.com': {
            'name': 'John Doe',
            'password': 'hunter2'
        }
    }
}

@manager.user_loader()
def query_user(user_id: str):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    return DB['users'].get(user_id)

@app.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    print(password)

    user = query_user(email)
    if not user:
        # you can return any response or error of your choice
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': email}
    )
    return {'access_token': access_token}

@app.get('/protected')
def protected_route(user=Depends(manager)):
    print(user)
    return {'user': user}