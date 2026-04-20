from utils.invoke_llm import invoke_llm
from agents.system_prompt import system_prompt
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.resources import load_mcp_resources
from langchain_mcp_adapters.prompts import load_mcp_prompt
from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode
from repositories.error_log import error_logger
 
from models.user_query import StructuredOutput
 
PROMPT_ARGS = {
    "order_assistant": {"use": "prompt for order assistant"}
}
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"
 
class Agent:
 
    def __init__(self):
        self.agent = None
        self.client = None
 
    async def create_agent(self):
        """
            This function will be called from the invoke agent function.
            Then the control will reach this function and then llm will be invoked.
            And then the client will be integrated with the mcp server using the URL where it is exposed.
            Using using get_tools() function the tools that are available in the mcp server will be integrated and store in a variable tools.
            All the available prompts will be loaded in the meassages and the it will stored in the resource context
            After that agent will be created with create_react_agent() with the parameters invoked llm, tools and the the system prompt.
            If any errors occur before raising the error it will stored in the database for reference and then the error will be raised.
            """
        try:
            # 🔹 1. Get LLM
            llm = await invoke_llm.get_llm()
 
            # 🔹 2. Create MCP Client
            self.client = MultiServerMCPClient({
                "tools": {
                    "transport": "streamable_http",
                    "url": MCP_SERVER_URL
                }
            })
 
            # 🔹 3. Load tools
            tools = await self.client.get_tools()
 
            # 🔹 4. Load resources (IMPORTANT)
            resource_context = ""
 
            async with self.client.session("tools") as session:
                blobs = await load_mcp_resources(session)
 
                for blob in blobs:
                    uri = blob.metadata.get("uri", "unknown")
                    text = blob.as_bytes().decode("utf-8", errors="replace")
 
                    resource_context += f"\n[{uri}]\n{text}\n"
            # async with self.client.session("my_server") as session:
                list_result      = await session.list_prompts()
                available_prompts = list_result.prompts
                print(available_prompts)
                all_prompt_messages = []
                for prompt in available_prompts:
                    print(prompt,"__________")
                    args     = PROMPT_ARGS.get(prompt.name, {})
                    messages = await load_mcp_prompt(session,prompt.name,arguments=args)
                    print(messages,"========================")
                    all_prompt_messages.extend(messages)

            # 🔹 5. Create agent
            self.agent = create_react_agent(
                model=llm,
                tools=tools,
                prompt=system_prompt
                #response_format=StructuredOutput
            )
            messages = list(all_prompt_messages)

            if resource_context:
                messages.append(
                    HumanMessage(content=f"Available resources:\n{resource_context}")
                )
            # 🔹 6. Store resource context
            self.resource_context = messages
 
        except Exception as e:
            error_logger.save_error(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                error_message=str(e),
                file_name="agent.py",
                function_name="create_agent"
            )
 
            raise Custom_App_Exception(
                message=f"Agent creation failed: {str(e)}",
                code=ErrorCode.AGENT_CREATION_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR
            )
 
    async def invoke_agent(self, user_input: str) -> str:
        """
            After the call from the service the control will reach here.
            In this function we will create the agent by calling create_agent() function.
            The agent will be invoked with ainvoke() with the resource_context which will have all the prompts and the user_query.
            After that agent will call tools based on the user_query.
            After execution the response will be returned to the service and then it will be propagated further.
            If any errors occur before raising the error it will stored in the database for reference and then the error will be raised.
        """
        try:
            if not self.agent:
                await self.create_agent()
 
            
            #self.resource_context.append(("user", user_input))
            self.resource_context.append(HumanMessage(content=user_input))
 
            # 🔹 8. Invoke agent
            response = await self.agent.ainvoke({
                "messages": self.resource_context
            })
            print(response)
            # 🔹 9. Extract structured response
            # result = response["structured_response"].response
            # print(result)
            # return result
            return response["messages"][-1].content
 
        except Custom_App_Exception:
            raise
 
        except Exception as e:
            error_logger.save_error(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                error_message=str(e),
                file_name="agent.py",
                function_name="invoke_agent"
            )
 
            raise Custom_App_Exception(
                message=f"Agent invocation failed: {str(e)}",
                code=ErrorCode.AGENT_INVOCATION_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR
            )

agent=Agent()
 
