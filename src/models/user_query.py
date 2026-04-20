from pydantic import BaseModel

class UserQuery(BaseModel):
    """Pydantic model for user input validation"""
    user_query: str

class StructuredOutput(BaseModel):
    """Pydantic model structured agent output"""
    user_query: str
    response: str