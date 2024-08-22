import bcrypt
import binascii
import psycopg2.sql as sql
from dotenv import load_dotenv
from session_manager import SessionManager
from crud import Crud

class AuthManager:
    def __init__(self, crud):
        self.crud = crud
    
    def authenticate_user(self, loginname, password):
        # getting record against loginname, password
        select_query = sql.SQL("SELECT id, password FROM {} WHERE loginname = {}").format(
            sql.Identifier(self.crud.table),
            sql.Placeholder()
        )
        self.crud._execute(select_query, (loginname,))
        table_values = self.crud._cursor.fetchone()

        # if no record found
        if not table_values:
            return None, "Invalid Credentials"
        
        # else, getting id and password
        id, hashed_password = table_values
        hex_string = hashed_password.replace('\\x', '')

        # comparing entered and fetched password
        if bcrypt.checkpw(password.encode('utf-8'), binascii.unhexlify(hex_string)):
            return id, "Valid credentials"
        else:
            return None, "Invalid Credentials"
    
    def login(self, loginname, password):
        # calling authenticate_user method, returns user record if found
        user_id, auth_message = self.authenticate_user(loginname, password)
        load_dotenv()

        # connecting to login table
        table = Crud(
            table = "login",
            primarykey = "id"
        )
        table.connect()
        
        # managing session if user record exists
        if user_id:
            session_manager = SessionManager(crud=table)
            # calling manage_session method, returns session_key
            session_key = session_manager.manage_session(user_id)
            print(auth_message)
            return session_key
        else:
            print(auth_message)
            return None

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)