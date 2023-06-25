from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from api.config import AuthConfig
from api.v1.dependencies.database import get_dao_provider
from api.v1.models.token import Token
from customer_management.exceptions.user import UserNotFound
from customer_management.models import dto
from infrastructure.database.holder import DAO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/user/login')


def get_current_user(token: str = Depends(oauth2_scheme)):
    raise NotImplementedError


def get_auth_provider():
    raise NotImplementedError


class AuthProvider:
    def __init__(self, config: AuthConfig):
        self.config = config
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.secret_key = config.secret_key
        self.algorythm = 'HS256'
        self.access_token_expire = config.token_expire

    def verify_password(self, plain_password: str,
                        hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate(self, username: str, password: str,
                           dao: DAO) -> dto.User:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            user = await dao.user.get_by_username_with_password(username)
        except UserNotFound:
            raise http_status_401
        if not self.verify_password(password, user.hashed_password or ''):
            raise http_status_401
        return user.without_password()

    def create_access_token(self, data: dict,
                            expires_delta: timedelta) -> Token:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key,
                                 algorithm=self.algorythm)
        return Token(access_token=encoded_jwt, token_type='bearer')

    def create_user_token(self, user: dto.User) -> Token:
        return self.create_access_token(
            data={'sub': user.username}, expires_delta=self.access_token_expire
        )

    async def get_current_user(
            self,
            request: Request,
            token: str = Depends(oauth2_scheme),
            dao: DAO = Depends(get_dao_provider),
    ) -> dto.User:
        user = getattr(request.state, 'user', None)
        if user is not None:
            return user

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(token, self.secret_key,
                                 algorithms=[self.algorythm])
            username: str = payload.get('sub')
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        try:
            user = await dao.user.get_by_username(username=username)
        except UserNotFound:
            raise credentials_exception
        else:
            request.state.user = user
            await dao.user.update_user(user.id, {'last_activity': datetime.now()})
            await dao.commit()
        return user

    async def login_route(
            self,
            form_data: OAuth2PasswordRequestForm = Depends(),
            dao: DAO = Depends(get_dao_provider),
    ) -> Token:
        user = await self.authenticate(form_data.username,
                                       form_data.password, dao)
        return self.create_user_token(user)

    def setup_auth_routes(self, router: APIRouter):
        router.add_api_route('/login', self.login_route, methods=['POST'])
