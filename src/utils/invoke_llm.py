"""
config.py
Shared configuration for all sample code files.
Creates the Bedrock LLM client so you don't repeat setup in every file.
"""
import boto3
from settings import config
from langchain_aws import ChatBedrock
from typing import Any



class BedrockClient:
    async def get_bedrock_client(self)-> Any:
        """Create and return a Bedrock runtime client."""
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=config.region,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key

        )

class InvokeLLM:
    async def get_llm(self,max_tokens=500, temperature=0.7)-> ChatBedrock:
        """Create and return a ChatBedrock LLM instance."""
        return ChatBedrock(
            client=await bedrock_client.get_bedrock_client(),
            model_id=config.model_id,
            provider=config.provider,
            model_kwargs={
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
    
bedrock_client=BedrockClient()
invoke_llm=InvokeLLM()
