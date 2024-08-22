from datetime import datetime
import uuid
from datetime import timedelta

class SessionManager:
    def __init__(self, crud):
        self.crud = crud
    
    def manage_session(self, user_id):
         # Check if a valid session exists
        session_record = self.crud.select_all(primaryKey_value=user_id)
        if session_record and session_record[0][6] > datetime.now():
                # Update session expiry to +30 min
                new_expiry = datetime.now() + timedelta(minutes=30)
                self.crud.update(column='session_expiry', column_value=new_expiry, primaryKey_value=user_id)
                # Generate a new session key
                new_session_key = str(uuid.uuid4())
                self.crud.update(column='session_key', column_value=new_session_key, primaryKey_value=user_id)
                self.crud.commit()
                return new_session_key

        # If no valid session exists, create a new one"""
        new_session_key = str(uuid.uuid4())
        logged_in = datetime.now()
        session_expiry = logged_in + timedelta(minutes=30)
        
        self.crud.insert(
            user_id=user_id,
            session_key=new_session_key,
            logged_in=logged_in,
            session_expiry=session_expiry,
            remote_addr="",
            remote_host="",
            status=0,
            origin=0
        )

        self.crud.commit()
        return new_session_key