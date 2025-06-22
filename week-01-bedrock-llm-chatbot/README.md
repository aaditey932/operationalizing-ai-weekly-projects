# 🤖 AWS Bedrock Chatbot

A simple and interactive chatbot application built with Streamlit and Amazon Bedrock's Nova Lite model. This project demonstrates how to create a conversational AI interface using AWS's managed AI services.

## 📋 Overview

This chatbot application provides a clean, web-based interface for interacting with Amazon's Nova Lite language model through AWS Bedrock. Users can have natural conversations with the AI, and the chat history is maintained throughout the session.

## ✨ Features

- **Interactive Chat Interface**: Clean, user-friendly chat UI built with Streamlit
- **AWS Bedrock Integration**: Leverages Amazon Nova Lite model for AI responses
- **Session Management**: Maintains chat history during the session
- **Error Handling**: Graceful error handling for API failures
- **Responsive Design**: Wide layout with sidebar for instructions
- **Clear Chat History**: Option to reset conversation history

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Amazon Nova Lite (via AWS Bedrock)
- **AWS Services**: Bedrock Runtime
- **Python Libraries**: 
  - `boto3` - AWS SDK
  - `streamlit` - Web interface
  - `langchain` - LLM framework (imported but not actively used)

## 📋 Prerequisites

- Python 3.7+
- AWS Account with Bedrock access
- AWS CLI configured with appropriate credentials
- Access to Amazon Nova Lite model in AWS Bedrock

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd bedrock-chatbot
```

### 2. Install Dependencies
```bash
pip install streamlit boto3 langchain langchain-community
```

### 3. Configure AWS Credentials
Make sure your AWS profile is properly configured. The application uses the profile named `aaditey-personal` by default.

```bash
aws configure --profile aaditey-personal
```

Or update the `AWS_PROFILE` environment variable in the code to match your profile name.

### 4. Enable Bedrock Model Access
Ensure you have access to the Amazon Nova Lite model in AWS Bedrock console:
1. Go to AWS Bedrock console
2. Navigate to Model Access
3. Request access to `amazon.nova-lite-v1:0` if not already enabled

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 🔧 Configuration

### Model Parameters
The chatbot is configured with the following parameters:
- **Max Tokens**: 512
- **Temperature**: 0.7 (controls creativity)
- **Top P**: 0.9 (nucleus sampling)

You can modify these parameters in the `my_chatbot()` function to adjust the model's behavior.

### AWS Region
The application is configured to use `us-east-1`. Update the `region_name` parameter if you want to use a different region.

## 📁 Project Structure

```
bedrock-chatbot/
│
├── app.py                 # Main application file
├── README.md             # This file
└── requirements.txt      # Python dependencies (optional)
```

## 🎯 Key Learnings

This project provided hands-on experience with:
- **AWS Bedrock Fundamentals**: Understanding how to integrate and use AWS Bedrock for AI applications
- **LLM Integration**: Learning to work with large language models through AWS managed services
- **Streamlit Development**: Building interactive web applications with Streamlit
- **AWS SDK Usage**: Using boto3 to interact with AWS services programmatically
- **Error Handling**: Implementing robust error handling for cloud service integrations

## 🔍 Usage

1. Launch the application using the setup instructions above
2. Type your message in the chat input at the bottom
3. Press Enter or click send
4. The AI will respond based on your query
5. Use the "Clear Chat History" button in the sidebar to reset the conversation

## ⚠️ Important Notes

- Ensure your AWS credentials have the necessary permissions for Bedrock
- The Nova Lite model must be enabled in your AWS account
- API calls to Bedrock will incur AWS charges
- Chat history is only maintained during the current session

## 🚧 Future Enhancements

- Add conversation memory across sessions
- Implement different model selection options
- Add file upload capabilities
- Include conversation export functionality
- Add user authentication
- Implement rate limiting

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Powered by Amazon Bedrock Nova** 🚀