# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within ISO20022 RAG, please send an email to gadeshivani@gmail.com. All security vulnerabilities will be promptly addressed.

Please include the following information in your report:
- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## Security Measures

1. **API Key Protection**:
   - All API keys must be stored in environment variables
   - Never commit API keys to version control
   - Use the provided env.template for configuration

2. **Data Security**:
   - Financial message content is processed in memory only
   - No persistent storage of message content
   - All outputs are sanitized for sensitive information

3. **Code Security**:
   - Regular dependency updates
   - Automated security scanning
   - Input validation and sanitization

4. **Usage Guidelines**:
   - Always use HTTPS for API connections
   - Implement rate limiting in production
   - Monitor API usage and costs
   - Follow ISO20022 security guidelines

## Intellectual Property

This project is protected by:
1. Copyright (c) 2025 Shivani Gade
2. MIT License
3. Required attribution for academic and commercial use

## Third-Party Components

This project uses the following major components:
- OpenAI API: Subject to OpenAI's terms of service
- Google Generative AI: Subject to Google's terms of service
- LangChain: Apache 2.0 License
- Other dependencies: See requirements.txt for full list

## Compliance

When using this system in a production environment:
1. Ensure compliance with financial regulations
2. Implement proper audit logging
3. Follow data protection requirements
4. Monitor for regulatory changes 