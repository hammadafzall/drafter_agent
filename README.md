# 🚀 Drafter - AI Document Assistant

A powerful AI-powered document writing assistant built with LangChain and LangGraph that helps you create, edit, and manage documents efficiently.

## ✨ Features

- **🤖 AI-Powered Writing**: Get intelligent suggestions and improvements for your documents
- **📝 Real-time Editing**: Update and modify document content seamlessly
- **💾 Smart Saving**: Save documents with automatic file management
- **🎯 Professional Interface**: Clean, user-friendly command-line interface
- **🛡️ Error Handling**: Robust error handling and graceful failure recovery
- **🔒 Security**: Environment-based API key management

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/hammadafzall/drafter_agent.git
   cd drafter_agent
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**:
   ```bash
   python agent.py
   ```

## 🎯 Usage

### Starting Drafter

Simply run the application:

```bash
python agent.py
```

You'll see a welcome message and can start creating documents immediately.

### Basic Workflow

1. **Create a Document**: Tell Drafter what you want to create
2. **Edit Content**: Make changes and improvements
3. **Save**: Save your work to a file when finished

### Example Session

```
🚀 DRAFTER - AI Document Assistant
==================================================

🎉 Welcome to Drafter - Your AI Document Assistant!

I can help you:
• Create new documents from scratch
• Edit and improve existing content
• Save your work to files
• Provide writing suggestions

What would you like to create or work on today?

💬 What would you like to do with the document? Create a business proposal for a tech startup

🤖 AI: I'll help you create a comprehensive business proposal for a tech startup. Let me start by creating a structured document with all the essential sections.

🔧 Using tools: update

📋 ✅ Document has been updated successfully!

Current content:
# Tech Startup Business Proposal

## Executive Summary
[To be developed based on your specific startup idea]

## Company Overview
- Company Name: [Your Startup Name]
- Industry: Technology
- Mission: [Your mission statement]
- Vision: [Your vision statement]

## Market Analysis
- Target Market: [Define your target audience]
- Market Size: [Market opportunity]
- Competitive Landscape: [Key competitors]

## Product/Service Description
- Core Product: [Main product/service]
- Key Features: [List of features]
- Value Proposition: [What makes you unique]

## Business Model
- Revenue Streams: [How you'll make money]
- Pricing Strategy: [Your pricing approach]
- Cost Structure: [Key costs]

## Marketing Strategy
- Marketing Channels: [How you'll reach customers]
- Sales Strategy: [How you'll sell]
- Growth Plan: [How you'll scale]

## Financial Projections
- Revenue Forecast: [3-5 year projections]
- Funding Requirements: [How much you need]
- Use of Funds: [How you'll spend the money]

## Team
- Key Personnel: [Founders and key team members]
- Advisory Board: [Advisors and mentors]

## Risk Analysis
- Key Risks: [Potential challenges]
- Mitigation Strategies: [How you'll address risks]

## Conclusion
[Summary and call to action]

💬 What would you like to do with the document? Add more details to the executive summary

🤖 AI: I'll enhance the executive summary section with more specific details and compelling content.

🔧 Using tools: update

📋 ✅ Document has been updated successfully!

Current content:
# Tech Startup Business Proposal

## Executive Summary
Our innovative tech startup aims to revolutionize [specific industry/problem] by providing [unique solution]. With a projected market opportunity of $[X] billion and a proven team with [X] years of combined experience, we are seeking $[X] in funding to accelerate our growth and capture market share.

**Key Highlights:**
- **Problem**: [Describe the problem you're solving]
- **Solution**: [Your innovative solution]
- **Market**: $[X] billion addressable market
- **Traction**: [Current achievements, users, revenue]
- **Team**: Experienced founders with [relevant background]
- **Funding**: Seeking $[X] for [specific use of funds]

**Financial Projections:**
- Year 1 Revenue: $[X]
- Year 3 Revenue: $[X]
- Break-even: [Timeline]
- Exit Strategy: [IPO, acquisition, etc.]

This investment opportunity offers [X]% potential return with a clear path to profitability and market leadership.

[Rest of document remains the same...]

💬 What would you like to do with the document? save as startup_proposal

🔧 Using tools: save

📄 Document saved successfully to: F:\AI Projects\drafter_agent\startup_proposal.txt

📋 ✅ Document has been saved successfully to 'startup_proposal.txt'.

==================================================
✅ Drafter session completed successfully!
==================================================
```

## 🔧 Configuration

### Environment Variables

| Variable         | Description         | Required |
| ---------------- | ------------------- | -------- |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes      |

### Model Configuration

You can modify the AI model settings in `agent.py`:

```python
model = ChatOpenAI(
    model="gpt-4o",        # Model to use
    temperature=0.7,       # Creativity level (0.0-1.0)
    max_tokens=2000        # Maximum response length
).bind_tools(tools)
```

## 🏗️ Architecture

The application uses a LangGraph-based architecture with the following components:

- **Agent State**: Manages conversation history and document state
- **Tools**: `update` and `save` functions for document operations
- **Graph Workflow**: Orchestrates the conversation flow
- **Error Handling**: Graceful handling of API errors and user interruptions

## 🛡️ Security

- API keys are stored in environment variables (`.env` file)
- The `.env` file is excluded from version control
- Input validation and sanitization for file operations
- Graceful error handling to prevent information leakage

## 🐛 Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**

   - Ensure your `.env` file exists and contains the API key
   - Check that the key is valid and has sufficient credits

2. **"Error initializing OpenAI model"**

   - Verify your internet connection
   - Check that your API key is correct
   - Ensure you have sufficient API credits

3. **File permission errors**
   - Check that you have write permissions in the current directory
   - Try running with administrator privileges if needed

### Getting Help

If you encounter issues:

1. Check the error messages for specific details
2. Verify your environment setup
3. Ensure all dependencies are installed correctly
4. Check your OpenAI API key and credits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- Graph workflow using [LangGraph](https://langchain.com/langgraph)

---

**Made with ❤️ by Hammad Afzal**
