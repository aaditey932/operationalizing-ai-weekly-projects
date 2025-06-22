# 🤖 AWS Bedrock Agent Chatbot

A multilingual chatbot application built with Streamlit and Amazon Bedrock Agents. This project demonstrates how to create an intelligent conversational AI interface using AWS's managed agent services with support for multiple languages.

## 📋 Overview

This chatbot application provides a clean, web-based interface for interacting with a custom Amazon Bedrock Agent. Users can have natural conversations with the AI in their preferred language (English or Spanish), and the chat history is maintained throughout the session. The agent processes streaming responses for real-time interaction.

## ✨ Features

- **Interactive Chat Interface**: Clean, user-friendly chat UI built with Streamlit
- **AWS Bedrock Agent Integration**: Leverages custom Bedrock Agent for intelligent responses
- **Multilingual Support**: Choose between English and Spanish responses
- **Streaming Responses**: Real-time response processing with streaming chunks
- **Session Management**: Maintains chat history during the session
- **Language Settings**: Easy language switching via sidebar
- **Error Handling**: Graceful error handling for API failures
- **Responsive Design**: Wide layout with sidebar for settings and instructions
- **Clear Chat History**: Option to reset conversation history

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Service**: Amazon Bedrock Agent
- **AWS Services**: Bedrock Agent Runtime
- **Python Libraries**: 
  - `boto3` - AWS SDK
  - `streamlit` - Web interface
  - `uuid` - Session ID generation
  - `re` - Response parsing

## 📋 Prerequisites

- Python 3.7+
- AWS Account with Bedrock Agent access
- AWS CLI configured with appropriate credentials
- A configured Bedrock Agent with the specified Agent ID and Alias ID
- Appropriate IAM permissions for Bedrock Agent Runtime

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd bedrock-agent-chatbot
```

### 2. Install Dependencies
```bash
pip install streamlit boto3
```

### 3. Configure AWS Credentials
Make sure your AWS profile is properly configured. The application uses the profile named `aaditey-personal` by default.

```bash
aws configure --profile aaditey-personal
```

Or update the `AWS_PROFILE` environment variable in the code to match your profile name.

### 4. Configure Agent IDs
Update the agent configuration in the code with your specific agent details:

```python
agent_id = "YOUR_AGENT_ID"
agent_alias_id = "YOUR_AGENT_ALIAS_ID"
```

Current configuration:
- **Agent ID**: `SYDHEELWTH`
- **Agent Alias ID**: `NV9MMGMZ43`

### 5. Set Up IAM Permissions
Ensure your AWS credentials have the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent"
            ],
            "Resource": "*"
        }
    ]
}
```

### 6. Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 🔧 Configuration

### Agent Settings
The chatbot uses the following configuration:
- **Region**: `us-east-1`
- **Service**: `bedrock-agent-runtime`
- **Session Management**: Unique UUID for each conversation
- **Response Processing**: Supports both direct text and `<final_response>` tag extraction

### Language Support
Currently supports:
- **English** (default)
- **Spanish**

Additional languages can be easily added by updating the language selectbox options.

## 📁 Project Structure

```
bedrock-agent-chatbot/
│
├── app.py                 # Main application file
├── README.md             # This file
└── requirements.txt      # Python dependencies (optional)
```

## 🎯 Key Learnings

This project provided hands-on experience with:
- **AWS Bedrock Agents**: Understanding how to integrate and use AWS Bedrock Agents for conversational AI
- **Agent Runtime Management**: Learning to work with Bedrock Agent Runtime for real-time interactions
- **Streaming Response Handling**: Processing streaming responses from AWS services
- **Multilingual AI Applications**: Implementing language selection and context passing
- **Session Management**: Using unique session IDs for conversation tracking
- **Response Parsing**: Extracting structured responses using regex patterns
- **Streamlit Advanced Features**: Building more sophisticated UIs with settings and state management

## 🔍 Usage

1. Launch the application using the setup instructions above
2. Select your preferred language from the sidebar dropdown
3. Type your message in the chat input at the bottom
4. Press Enter or click send
5. The agent will respond in your selected language
6. Use the "Clear Chat History" button in the sidebar to reset the conversation
7. Change languages at any time using the sidebar settings

## ⚠️ Important Notes

- Ensure your AWS credentials have the necessary permissions for Bedrock Agent Runtime
- The Bedrock Agent must be properly configured and deployed in your AWS account
- Each conversation uses a unique session ID, so context doesn't persist between app restarts
- API calls to Bedrock Agent will incur AWS charges
- The agent processes streaming responses, which may take a moment to complete

## 🏗️ Agent Architecture

This application integrates with a Bedrock Agent that:
- Processes natural language queries
- Supports multilingual responses
- Can be enhanced with knowledge bases, action groups, and guardrails
- Provides streaming responses for better user experience

## 🚧 Future Enhancements

- **Persistent Sessions**: Store session IDs to maintain conversation context
- **More Languages**: Add support for additional languages
- **Voice Input/Output**: Integrate speech-to-text and text-to-speech
- **File Upload**: Allow document uploads for context-aware conversations
- **Conversation Export**: Export chat history to files
- **Custom Themes**: Add UI customization options
- **Agent Metrics**: Display response times and token usage
- **Multi-Agent Support**: Switch between different agents

## 🔧 Troubleshooting

### Common Issues:
1. **Agent Not Found**: Verify your agent ID and alias ID are correct
2. **Permission Denied**: Check IAM permissions for Bedrock Agent Runtime
3. **Region Issues**: Ensure your agent is in the same region as specified in the code
4. **Streaming Errors**: Check network connectivity and AWS service status

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Powered by Amazon Bedrock Agent** 🚀