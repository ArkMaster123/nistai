# nistai_prompt.py

SYSTEM_PROMPT = """You are an expert cybersecurity consultant specializing in NIST framework analysis. 
Provide detailed security assessments with clear justifications for all findings and scores."""

ANALYSIS_PROMPT = """Analyze this document comprehensively for security and compliance issues.
Structure your response in HTML format with the following specific sections:

1. SECURITY RISKS AND CHALLENGES
- Identify at least 6 specific security risks
- For each risk, explain the potential impact
- Categorize risks by severity (High/Medium/Low)

2. SECURITY GAPS
- Identify at least 4 major security control gaps
- For each gap, explain why it's significant
- Include specific recommendations to address each gap

3. NIST FRAMEWORK DETAILED ANALYSIS
For each NIST function, provide:

a) IDENTIFY (/5)
- Asset Management assessment
- Business Environment analysis
- Governance structure evaluation
- Risk Assessment methodology review
- Detailed justification for score

b) PROTECT (/5)
- Access Control measures
- Data Security protocols
- Information Protection processes
- Protective Technology evaluation
- Detailed justification for score

c) DETECT (/5)
- Anomalies and Events monitoring
- Security Continuous Monitoring
- Detection Processes assessment
- Detailed justification for score

d) RESPOND (/5)
- Response Planning evaluation
- Communications assessment
- Analysis capabilities
- Mitigation measures
- Detailed justification for score

e) RECOVER (/5)
- Recovery Planning assessment
- Improvement recommendations
- Communications strategies
- Detailed justification for score

4. PRIORITY RECOMMENDATIONS
- List at least 5 specific, actionable recommendations
- Prioritize by impact and implementation effort
- Include estimated implementation timeframes
- Provide success metrics for each recommendation

5. OVERALL RISK RATING
- Provide a final risk rating (High/Medium/Low)
- Include detailed justification for the rating
- List key factors influencing the rating

Format the response in clean HTML with clear section headers and structured content.
Use bullet points for better readability where appropriate.
Ensure each NIST score includes specific examples and detailed reasoning.
"""

def get_claude_messages(pdf_base64: str):
    """Return the formatted messages for Claude API"""
    return [{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_base64
                }
            },
            {
                "type": "text",
                "text": ANALYSIS_PROMPT
            }
        ]
    }]