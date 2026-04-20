from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode
from repositories.database import Database
from sqlalchemy import text
from repositories.error_log import error_logger



class HealthCheckRepository():
    def __init__(self):
        self.db_instance = Database()

    async def health_check_repository(self)-> str:
        """Repository function to check the health of the database which returns a str"""
        try:
            db_session = self.db_instance.SessionLocal()
            orm_query = text("SELECT 1")
            result = db_session.execute(orm_query)
            if not (result.scalar() == 1):
                return "Unhealthy"           
            return "Healthy"

        except Custom_App_Exception:
            raise
        except Exception as e:
            error_logger.save_error(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            error_message=str(e),
            file_name="health_repository.py",
            function_name="health_check_repository"
        )
            raise Custom_App_Exception(
                message=f"Repository error: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
            )
        finally:
            if db_session:
                db_session.close()

health_repository=HealthCheckRepository()
        
          