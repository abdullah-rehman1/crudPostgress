import os
import bcrypt
import binascii
from dotenv import load_dotenv
from auth_manager import AuthManager
from crud import Crud

def main():
    # Load environment variables from the .env file
    load_dotenv()

    #connect to db
    table = Crud(
        table = "user",
        primarykey = "id"
    )
    table.connect()
    
    #Create Instance of AuthManager for authentication
    auth_manager = AuthManager(crud=table)
    
    #verifying user credentials, printing returned session_key
    print(auth_manager.login("jane_smith","jane_smith124"))

if __name__ == "__main__":
    main()