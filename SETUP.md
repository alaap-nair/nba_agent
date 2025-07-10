# 🚀 NBA Agent Setup Guide

## Environment Variables Configuration

Create a `.env` file in the project root directory with the following variables:

```bash
# Required: OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Judgment Labs Configuration (for testing and monitoring)
JUDGMENT_API_KEY=your_judgment_labs_api_key_here
JUDGMENT_ORG_ID=your_judgment_organization_id_here

# Optional: Application Settings
NBA_AGENT_CACHE_TTL=3600
NBA_AGENT_MAX_RETRIES=3
NBA_AGENT_LOG_LEVEL=INFO

# Optional: Development Settings
DEBUG=False
DEVELOPMENT_MODE=False
```

## Getting Your API Keys

### OpenAI API Key (Required)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key and add it to your `.env` file

### Judgment Labs API Key (Optional)
1. Visit [Judgment Labs](https://app.judgmentlabs.ai/)
2. Create an account or log in
3. Navigate to your organization settings
4. Generate an API key
5. Copy both the API key and Organization ID to your `.env` file

## Verification

To verify your setup is working:

```bash
# Test the basic agent
python apps/chat.py

# Test with a simple query
# Example: "What are LeBron's stats this season?"
```

## Troubleshooting

- **Missing OpenAI key**: You'll see authentication errors
- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Port conflicts**: Use `--server.port 8502` with Streamlit commands
- **Cache issues**: Delete the `cache/` directory to reset 