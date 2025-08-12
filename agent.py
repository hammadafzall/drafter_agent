"""
Drafter Agent - A Document Writing Assistant

This module provides an AI-powered document writing assistant that helps users
create, update, and save documents using LangChain and LangGraph.

Author: Hammad Afzal
"""

import os
import sys
from typing import Annotated, Sequence, TypedDict, Optional
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Load environment variables
load_dotenv()

# Global variable to store document content
document_content = ""

class AgentState(TypedDict):
    """State definition for the document agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool 
def update(content: str) -> str:
    """
    Update the document with the provided content.
    
    Args:
        content: The new content to replace the current document.
        
    Returns:
        A confirmation message with the updated document content.
    """
    global document_content
    if not content.strip():
        return "Error: Cannot update document with empty content."
    
    document_content = content.strip()
    return f"✅ Document has been updated successfully!\n\nCurrent content:\n{document_content}"

@tool
def save(filename: str) -> str:
    """
    Save the current document to a text file and finish the process.
    
    Args:
        filename: Name for the text file (with or without .txt extension).
        
    Returns:
        A confirmation message indicating success or failure.
    """
    global document_content
    
    if not document_content.strip():
        return "⚠️ Warning: Document is empty. Saving empty document."
    
    # Ensure filename has .txt extension
    if not filename.endswith('.txt'):
        filename = f'{filename}.txt'
    
    # Sanitize filename
    filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
    
    try:
        file_path = Path(filename)
        
        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(document_content)
        
        print(f"\n📄 Document saved successfully to: {file_path.absolute()}")
        return f"✅ Document has been saved successfully to '{file_path.name}'."
        
    except Exception as e:
        error_msg = f"❌ Error saving document: {str(e)}"
        print(error_msg)
        return error_msg

# Initialize tools and model
tools = [update, save]

try:
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        max_tokens=2000
    ).bind_tools(tools)
except Exception as e:
    print(f"❌ Error initializing OpenAI model: {e}")
    print("Please check your OPENAI_API_KEY environment variable.")
    sys.exit(1)

def create_system_prompt() -> SystemMessage:
    """Create the system prompt for the agent."""
    return SystemMessage(content=f"""
You are Drafter, a helpful and professional document writing assistant. Your role is to help users create, edit, and manage documents effectively.

CAPABILITIES:
- Update document content using the 'update' tool
- Save documents to files using the 'save' tool
- Provide writing suggestions and improvements
- Help with document structure and formatting

GUIDELINES:
- Always be helpful, professional, and clear in your responses
- When updating content, use the 'update' tool with the complete new content
- When saving, use the 'save' tool with an appropriate filename
- Show the current document state after any modifications
- Provide constructive feedback and suggestions
- Ask clarifying questions when needed

Current document content:
{document_content if document_content else "No content yet"}

Remember: Always show the current document state after any changes.
""")

def get_user_input(state: AgentState) -> HumanMessage:
    """Get user input based on the current state."""
    if not state['messages']:
        # First interaction
        welcome_message = """
🎉 Welcome to Drafter - Your AI Document Assistant!

I can help you:
• Create new documents from scratch
• Edit and improve existing content
• Save your work to files
• Provide writing suggestions

What would you like to create or work on today?
"""
        return HumanMessage(content=welcome_message)
    else:
        # Subsequent interactions
        try:
            user_input = input("\n💬 What would you like to do with the document? ")
            if not user_input.strip():
                return HumanMessage(content="Please provide some input or say 'save' to finish.")
            return HumanMessage(content=user_input.strip())
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Your work has not been saved.")
            sys.exit(0)
        except EOFError:
            print("\n\n👋 Goodbye! Your work has not been saved.")
            sys.exit(0)

def our_agent(state: AgentState) -> AgentState:
    """
    Main agent function that processes user input and generates responses.
    
    Args:
        state: Current agent state containing message history.
        
    Returns:
        Updated agent state with new messages.
    """
    system_prompt = create_system_prompt()
    user_message = get_user_input(state)
    
    # Build message list
    all_messages = [system_prompt] + list(state['messages']) + [user_message]
    
    try:
        response = model.invoke(all_messages)
        
        # Print AI response
        if response.content:
            print(f"\n🤖 AI: {response.content}")
        
        # Show tool usage
        if hasattr(response, "tool_calls") and response.tool_calls:
            tool_names = [tc['name'] for tc in response.tool_calls]
            print(f"🔧 Using tools: {', '.join(tool_names)}")
        
        return {"messages": list(state["messages"]) + [user_message, response]}
        
    except Exception as e:
        error_message = f"❌ Error processing request: {str(e)}"
        print(error_message)
        error_response = AIMessage(content=error_message)
        return {"messages": list(state["messages"]) + [user_message, error_response]}

def should_continue(state: AgentState) -> str:
    """
    Determine if the conversation should continue or end.
    
    Args:
        state: Current agent state.
        
    Returns:
        "continue" to keep the conversation going, "end" to finish.
    """
    messages = state["messages"]
    
    if not messages:
        return "continue"
    
    # Look for the most recent tool message
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
            "saved" in message.content.lower() and
            "document" in message.content.lower() and
            "successfully" in message.content.lower()):
            return "end"
    
    return "continue"

def print_messages(messages: Sequence[BaseMessage]) -> None:
    """
    Print recent messages in a readable format.
    
    Args:
        messages: List of messages to display.
    """
    if not messages:
        return
    
    # Show only the last 3 messages to avoid clutter
    recent_messages = messages[-3:]
    
    for message in recent_messages:
        if isinstance(message, ToolMessage):
            # Clean up tool result display
            content = message.content.strip()
            if content:
                print(f"📋 {content}")
        elif isinstance(message, HumanMessage):
            # Don't print user messages to avoid duplication
            pass
        elif isinstance(message, AIMessage):
            # Don't print AI messages as they're already shown
            pass

def setup_graph() -> StateGraph:
    """Set up the LangGraph workflow."""
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("agent", our_agent)
    graph.add_node("tools", ToolNode(tools))
    
    # Set entry point
    graph.set_entry_point("agent")
    
    # Add edges
    graph.add_edge("agent", "tools")
    
    # Add conditional edges
    graph.add_conditional_edges(
        "tools",
        should_continue,
        {
            "continue": "agent",
            "end": END
        }
    )
    
    return graph.compile()

def run_document_agent() -> None:
    """Main function to run the document agent."""
    print("\n" + "="*50)
    print("🚀 DRAFTER - AI Document Assistant")
    print("="*50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    try:
        # Initialize the application
        app = setup_graph()
        state = {"messages": []}
        
        # Run the agent
        for step in app.stream(state, stream_mode="values"):
            if "messages" in step:
                print_messages(step["messages"])
        
        print("\n" + "="*50)
        print("✅ Drafter session completed successfully!")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Your work has not been saved.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please try again or check your configuration.")

def main() -> None:
    """Entry point for the application."""
    try:
        run_document_agent()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()