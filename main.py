import os
import bcrypt
import binascii
from dotenv import load_dotenv
from crud import Crud

def main():
    # Load environment variables from the .env file
    load_dotenv()
    table = Crud(
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        port = os.getenv('PORT'),
        dbname = os.getenv('DB_NAME'),
        table = os.getenv('TABLE'),
        primarykey = os.getenv('PRIMARY_KEY')
    )

    table.connect()
    
    table.insert(
        loginname="john_doe",
        usergroup=2,
        username="John",
        password="john_do",
        firstname="John",
        middlename="A.",
        lastname="Doe",
        email="john.doe@example.com",
        access_level=3,
        status=1,
        language="English",
        profile_id=1001,
        login_attempts=5,
        last_login_attempt="2024-08-15 10:00:00",
        dbi_agent_id=2001,
        dbi_key="somekey",
        dbi_last_syncronized="2024-08-15 09:00:00",
        dbi_last_modified="2024-08-15 08:00:00",
        picture_id=3001
    )

    table.commit()
    table.select_all()

    table.update(
        column = 'email',
        column_value = 'john.doe@gmail.com',
        primaryKey_value = '1'
    )

    table.commit()
    table.select_all()

    salt = bcrypt.gensalt()
    password = "jane_smith124"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    table.insert(
        loginname="jane_smith",
        usergroup=3,
        username="Jane",
        password= hashed_password,
        firstname="Jane",
        middlename="B.",
        lastname="Smith",
        email="jane.smith@example.com",
        access_level=2,
        status=0,
        language="French",
        profile_id=1002,
        login_attempts=3,
        last_login_attempt="2024-08-14 15:00:00",
        dbi_agent_id=2002,
        dbi_key="anotherkey",
        dbi_last_syncronized="2024-08-14 14:00:00",
        dbi_last_modified="2024-08-14 13:00:00",
        picture_id=3002
    )

    table.commit()
    table.select_all()

    #verifying user credentials, with incorrect password
    testloginname = "jane_smith"
    testpassword = "jane_smith124"
    table_values = table.select(
        columns = ['loginname', 'password' ],
        primaryKey_value = '2'
    )

    loginname, hashed_password = table_values[0]
    hex_string = hashed_password.replace('\\x', '')

    if(loginname==testloginname and bcrypt.checkpw(testpassword.encode('utf-8'), binascii.unhexlify(hex_string))):
        print("Valid credentials")
    else:
        print("Invalid Credentials")

if __name__ == "__main__":
    main()