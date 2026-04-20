from agents.agent import agent
from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode
from repositories.error_log import error_logger
from agents.agent import agent
from models.user_query import UserQuery


class ChatbotService:
    def __init__(self):
            self.agent = agent
    
    async def chatbot_service(self, request: UserQuery) -> str:
        """
        After the call from the router, the call will reach the function with the validated request payload.
        In this service function the agent will be invoked with the user_query.
        If any errors occur before raising the error it will stored in the database for reference and then the error will be raised.
        After further execution it reach the service and the response will be sent back to router.
        """
        try:
            response = await self.agent.invoke_agent(request.user_query)
            return response
        except Custom_App_Exception:
            raise
        except Exception as e:
            error_logger.save_error(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                error_message=str(e),
                file_name="service.py",
                function_name="chatbot_service"
            )
            raise Custom_App_Exception(
                message=f"Service error: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR
            )
        
service=ChatbotService()