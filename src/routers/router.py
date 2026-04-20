from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from models.api_response_dto import APIResponse
from models.user_query import UserQuery
from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode
from services.service import service
from repositories.error_log import error_logger
from services.health_service import health_service


router = APIRouter(prefix="/api/v1")

@router.post("/chat")
async def chatbot_router(
    request: UserQuery = Body(...)
)-> JSONResponse:
    """
    This is a router chatbot_router() function that will route to the specific based on the endpoint invoked by the user.
    The parameter for this function is the user_query.
    It will process the user input using pydantic validation.
    After it will be propagated to service to carry on with the execution.
    If any error occur in router custom_app_exception will be raised.
    Before raising the error, it will be inserted into database for reference.
    After the execution the result will reach the router, it will converted into api response and then into JSON Response.
    """
    try:
        result = await service.chatbot_service(request)
        
        data =APIResponse(
            data=result,
            code=HttpStatusCode.OK,
            message ='Chatbot called successfully'
        )
        return JSONResponse(
            content= data.to_dict(),
            status_code=data.code,
        )
    except Custom_App_Exception:
        raise
    except Exception as e:
        error_logger.save_error(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            error_message=str(e),
            file_name="router.py",
            function_name="chatbot_service"
        )
        raise Custom_App_Exception(
            message=f"Router error: {str(e)}",
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            status_code=HttpStatusCode.INTERNAL_SERVER_ERROR
        )
    
@router.get("/health")
async def health_check_router() -> JSONResponse:
    """Router function to check the health of the database. It returns JSONResponse"""
    try:
        result = await health_service.health_check_service()
        print(result,"result")
        data =APIResponse(
            data=result,
            code=HttpStatusCode.OK
        )
        return JSONResponse(
            content= data.to_dict(),
            status_code=data.code
        )
    except Custom_App_Exception:
        raise
    except Exception as e:
        error_logger.save_error(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            error_message=str(e),
            file_name="router.py",
            function_name="health_check_router"
        )
        raise Custom_App_Exception(
            message=f"Router error: {str(e)}",
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            status_code=HttpStatusCode.INTERNAL_SERVER_ERROR
        )

    

