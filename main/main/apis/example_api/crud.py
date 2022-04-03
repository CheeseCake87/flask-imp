from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound
from ...builtins.functions.auth import auth_password
from ...builtins.functions.auth import generate_salt
from ...builtins.functions.auth import generate_private_key
from ...builtins.functions.auth import sha_password
from .models import sql_do
from .models import Account
import json


def authenticate_request_failed(account_id, private_key) -> bool:
    """
    Used to authenticate the connection to the api using a private key stored in the database.

    :param account_id:
    :param private_key:
    :return bool:
    """
    try:
        query_account = sql_do.query(
            Account
        ).filter(
            Account.account_id == account_id,
            Account.private_key == private_key,
        ).first()
    except NoResultFound:
        return True
    if query_account is None:
        return True

    return False


def if_account_not_found(username) -> bool:
    """
    Returns True if the account is not found in the database.

    :param username:
    :return bool:
    """
    try:
        query_account = sql_do.query(
            Account
        ).filter(
            Account.username == username
        ).first()
    except NoResultFound:
        return True
    if query_account is None:
        return True

    return False


def if_account_is_found(username) -> bool:
    """
    Returns True if the account is found in the database.

    :param username:
    :return bool:
    """
    try:
        query_account = sql_do.query(
            Account
        ).filter(
            Account.username == username
        ).first()
    except NoResultFound:
        return False
    if query_account is None:
        return False

    return True


def sign_in(username, password) -> dict:
    """
    Authenticates the user via username and password; Hands over their stored private key for future connections.

    :param username:
    :param password:
    :return dict[return: bool, account_id, private_key]:
    """
    try:
        query_account = sql_do.query(
            Account
        ).filter(
            Account.username == username
        ).first()
    except NoResultFound:
        return {"return": False}
    if query_account is None:
        return {"return": False}
    if auth_password(input_password=password,
                     database_password=query_account.password,
                     database_salt=query_account.salt):
        return {
            "return": True,
            "account_id": query_account.account_id,
            "private_key": query_account.private_key
        }
    return {"return": False}


def sign_up(username, password) -> dict:
    """
    Adds a new user to the database; Generates a new private key.
    :param username:
    :param password:
    :return dict[return: bool]:
    """
    this_salt = generate_salt()
    this_private_key = generate_private_key(username)

    add_account = Account(
        username=username,
        password=sha_password(password, this_salt),
        salt=this_salt,
        private_key=this_private_key
    )

    sql_do.add(add_account)
    sql_do.commit()

    sql_do.commit()
    return {
        "return": True
    }


def update_password(username, password) -> dict:
    """
    Updates the user's password; Generates a new salt value.
    :param username:
    :param password:
    :return:
    """
    this_salt = generate_salt()

    update_account_query = sql_do.query(
        Account
    ).filter_by(
        username=username
    ).one()

    update_account_query.salt = this_salt
    update_account_query.password = sha_password(password, this_salt)
    sql_do.commit()
    return {
        "return": True
    }
