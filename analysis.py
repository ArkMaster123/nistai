from llama_index.core import VectorStoreIndex
from reader import PDFReader
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
import re
import json
import logging
import os

logger = logging.getLogger("uvicorn")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

NISTAI_PROMPT = '''
Act as a senior cybersecurity consultant specializing in security assessments and NIST framework analysis. Generate a comprehensive security assessment report with the following structure:

Required Output Format:
{
    "executive_summary": "",
    "security_risks": [{
        "title": "",
        "details": [],
        "impact": "",
        "severity": "High|Medium|Low"
    }],
    "security_gaps": [{
        "area": "",
        "current_state": "",
        "required_state": "",
        "priority": "Critical|High|Medium|Low"
    }],
    "nist_framework_scores": {
        "identify": {
            "score": "1-5",
            "findings": [],
            "key_gaps": ""
        },
        "protect": {
            "score": "1-5",
            "findings": [],
            "key_gaps": ""
        },
        "detect": {
            "score": "1-5",
            "findings": [],
            "key_gaps": ""
        },
        "respond": {
            "score": "1-5",
            "findings": [],
            "key_gaps": ""
        },
        "recover": {
            "score": "1-5",
            "findings": [],
            "key_gaps": ""
        }
    },
    "recommendations": [{
        "title": "",
        "priority": "Critical|High|Medium|Low",
        "implementation_complexity": "High|Medium|Low",
        "expected_impact": ""
    }]
}

Requirements:
1. Executive Summary must be concise and highlight an overview of the company, what it does, what they focus on and must start with the company's name 
2. Security Risks section should identify 4-6 major risks
3. Security Gaps section should list 4-8 specific gaps
4. NIST Framework scores must:
   - Use a 1-5 scale
   - Include specific findings for each category
   - Provide clear justification for scores
5. Recommendations should be:
   - Actionable
   - Prioritized
   - Aligned with identified risks and gaps

Analysis Guidelines:
- Evaluate all findings against industry standards
- Consider organizational context and assets
- Focus on practical, implementable solutions
- Highlight critical issues that need immediate attention
- Provide clear rationale for risk levels and priorities

The output should be a single, well-formed JSON object following the exact structure above. All findings must be based on the provided input document/assessment data.
'''


def create_index(file):

    logger.info("Creating Index")

    documents = PDFReader().load_data(file)
    index = VectorStoreIndex.from_documents(documents)

    return index


def vector_similarity_search(questions, index):

    logger.info("Performing Vector Search")

    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    query_engine = RetrieverQueryEngine(retriever=retriever, )

    responses = []

    for question in questions:
        response = query_engine.query(question)
        responses.append(response)

    return responses


def calculate_average_score(responses) -> float:
    scores = []

    # Loop through each response and collect scores from each NodeWithScore
    for response in responses:
        for node in response.source_nodes:
            scores.append(float(node.score))

    # Calculate and return the average score if there are any scores, otherwise return 0
    if scores:
        return round(sum(scores) / len(scores), 3) * 100
    else:
        return 0.0


def nist_analysis(file):

    questions = [
        "Can you provide a detailed overview of the company's most significant cybersecurity risks, including potential threats, their likelihood, and potential business impact?", 
        "What are the current gaps in the organization's security infrastructure, and how do they align with (or deviate from) the NIST Cybersecurity Framework across its five core functions (Identify, Protect, Detect, Respond, Recover)?",
        "Based on your current security assessment, what are the top priority recommendations for improving the company's cybersecurity posture, including their potential implementation complexity and expected business impact?", 
        "How would you characterize the overall maturity of your organization's cybersecurity strategy, including key achievements, challenges, and strategic direction?",
        "What specific security incidents, if any, has the organization experienced in the past year, and what were the key learnings and mitigation strategies implemented?"
    ]

    index = create_index(file)
    response = vector_similarity_search(questions, index)

    llm = OpenAI(model="gpt-4o")

    messages = [
        ChatMessage(role="system", content=NISTAI_PROMPT),
        ChatMessage(
            role="user",
            content=f"Here is the output from the Vector Search: {response}"),
    ]

    resp = llm.chat(messages)

    # Remove ```html from the beginning and ``` from the end
    response_cleaned = re.sub(r'^```json|```$', '', resp.message.content)

    response_cleaned = json.loads(response_cleaned)

    return response_cleaned
