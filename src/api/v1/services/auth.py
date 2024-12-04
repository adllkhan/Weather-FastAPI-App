from datetime import datetime, timedelta

from passlib.context import CryptContext
from jwt import encode, decode, InvalidSignatureError

from ..repositories import UsersRepositories as Repositories
from ..schemas import Token, UserIn, UserOut
from ..models import User as UserModel
from ..core import (
    Config,
    InvalidTokenException,
    UserExistsException,
    InvalidCredentialsException,
    CannotCreateException,
)


class Services:
    def __init__(self):
        self.repositories = Repositories()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _verify(self, password: str, hashed_pwd) -> bool:
        return self.pwd_context.verify(secret=password, hash=hashed_pwd)

    def _generate_token(self, username: str) -> Token:
        data = {
            "sub": username,
            "exp": datetime.now() + timedelta(minutes=30)
        }
        token = encode(
            payload=data,
            key=Config().JWT_SECRET,
            algorithm=Config().JWT_ALGORITHM
        )
        return Token(
            access_token=token,
            token_type="Bearer",
        )

    async def register(self, user: UserIn) -> UserOut:
        if await self.repositories.get_by_username(user.username):
            raise UserExistsException()
        hashed_pwd = self.pwd_context.hash(user.password)
        user = UserModel(
            username=user.username,
            hashed_pwd=hashed_pwd,
        )
        user = await self.repositories.create(user)
        if not user:
            raise CannotCreateException()
        return UserOut(id=user.id, username=user.username)

    async def login(self, user: UserIn) -> Token:
        password = user.password
        user = await self.repositories.get_by_username(user.username)
        if not user:
            raise InvalidCredentialsException()
        hashed_pwd = user.hashed_pwd
        if not self._verify(
            password=password,
            hashed_pwd=hashed_pwd,
        ):
            raise InvalidCredentialsException()
        return self._generate_token(username=user.username)

    async def get_user(self, token: str) -> UserOut:
        try:
            payload = decode(
                jwt=token,
                key=Config().JWT_SECRET,
                algorithms=[Config().JWT_ALGORITHM]
            )
        except InvalidSignatureError:
            raise InvalidTokenException()
        if not payload["sub"]:
            raise InvalidTokenException()
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise InvalidTokenException()
        user = await self.repositories.get_by_username(username=payload["sub"])
        if not user:
            raise InvalidTokenException()
        return UserOut(id=user.id, username=user.username)
