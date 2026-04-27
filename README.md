☕ MCP-Based AI Ordering System

An AI-powered ordering system where an LLM interacts with tools and resources using the Model Context Protocol (MCP). The system enables users to place orders and check order status through natural language.

🚀 Features
🤖 LLM-powered conversational ordering system
🧠 MCP-based architecture (Tools + Resources)
⚡ FastAPI backend
📦 Tool-based actions (create order, check status)
📊 Resource-based data access (menu items)
🧩 Database-integrated workflows
📝 Prompt-driven AI interactions

🏗️ Architecture
The system works in the following flow:

User Query
- User interacts via natural language

Agent Processing
- LLM interprets user intent

Tool Execution
- make_order → creates new order
- check_status → retrieves order status

Resource Access
- Menu items fetched via MCP resources

Response Generation
- AI returns final conversational response

🛠️ Tech Stack
Backend: FastAPI  
AI: LLM (via MCP)  
Protocol: Model Context Protocol (MCP)  
Database: PostgreSQL  

📦 Project Setup

1. Clone the repository
git clone https://github.com/aakashkarunanithi/mcp-ordering-system
cd mcp-ordering-system

2. Install dependencies
pip install -r requirements.txt

3. Setup environment variables

Create a .env file:

DATABASE_URL=
LLM_API_KEY=

4. Run the application
uvicorn main:app --reload

📂 Project Structure
src/
 ├── tools/
 ├── resources/
 ├── database/
 ├── prompts/
 └── main.py

🔐 Security
- Sensitive configuration stored in .env
- Database operations secured through backend validation
