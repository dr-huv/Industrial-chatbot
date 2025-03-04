# Or use ollama_client based on your config
from src.models.groq_client import generate_response


class TechnicalReasoner:
    def __init__(self):
        # Words that might indicate a complex technical issue
        self.complexity_indicators = [
            "troubleshoot", "diagnose", "complex", "intermittent", "multiple",
            "inconsistent", "sequence", "steps", "procedure", "advanced",
            "technical", "expert", "engineer", "specialist", "workflow"
        ]

    def is_complex_issue(self, query):
        """Determine if a query represents a complex issue that needs reasoning"""
        # Check for complexity indicators
        query_lower = query.lower()
        indicator_count = sum(
            1 for indicator in self.complexity_indicators if indicator in query_lower)

        # If multiple indicators or query is long, it might be complex
        return indicator_count >= 2 or len(query.split()) > 15

    def generate_reasoning(self, query, context_docs=None):
        """Generate step-by-step reasoning for a complex issue"""
        # Create a prompt for reasoning
        reasoning_prompt = self._create_reasoning_prompt(query, context_docs)

        # Generate reasoning steps
        reasoning = generate_response(reasoning_prompt)

        return reasoning

    def generate_solution_with_reasoning(self, query, reasoning, context_docs=None):
        """Generate a final solution based on reasoning"""
        # Create a prompt for the final solution
        solution_prompt = self._create_solution_prompt(
            query, reasoning, context_docs)

        # Generate the final solution
        solution = generate_response(solution_prompt)

        # Combine reasoning and solution
        complete_response = f"{reasoning}\n\nBased on this analysis, here's the solution:\n\n{solution}"

        return complete_response

    def _create_reasoning_prompt(self, query, context_docs=None):
        """Create a prompt for step-by-step reasoning"""
        prompt = f"""
        You are an expert industrial support technician. I need your help to analyze this problem step-by-step:
        
        Problem: {query}
        
        Let's break down this issue systematically:
        """

        # Add context documents if available
        if context_docs:
            prompt += "\n\nRelevant information from knowledge base:\n"
            for i, doc in enumerate(context_docs):
                prompt += f"{i+1}. {doc['text']}\n"

        prompt += """
        Please analyze this problem step-by-step, considering:
        1. What are the possible causes?
        2. What diagnostic steps would you take?
        3. What information would you need to gather?
        4. What are the potential solutions based on different root causes?
        
        Format your response as a clear step-by-step analysis.
        """

        return prompt

    def _create_solution_prompt(self, query, reasoning, context_docs=None):
        """Create a prompt for the final solution based on reasoning"""
        prompt = f"""
        Based on the following analysis of this industrial problem:
        
        Problem: {query}
        
        Analysis:
        {reasoning}
        
        Please provide a clear, comprehensive solution that:
        1. Addresses the most likely root cause
        2. Provides actionable steps for the user
        3. Includes any necessary precautions or warnings
        4. Offers alternative approaches if the main solution doesn't work
        
        Format the solution in a clear, easy-to-follow manner.
        """

        return prompt
