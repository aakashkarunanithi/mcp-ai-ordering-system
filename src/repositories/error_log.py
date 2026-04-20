from sqlalchemy.orm import Session
from repositories.schema.chatbot_schema import Error
from repositories.database import Database

class ErrorLog:
    db_instance=Database()
    def save_error(self,  error_code: str, error_message: str, file_name: str, function_name: str) -> bool:
        """
        This is method is used to store the error in the database by creating a session with the instance of the database.
        """
        db_session = self.db_instance.SessionLocal()
        error = Error(
            error_code=error_code,
            error_message=error_message,
            file_name=file_name,
            function_name=function_name
        )
        db_session.add(error)
        db_session.commit()
        return True
    
error_logger=ErrorLog()
