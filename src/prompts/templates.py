def create_enhanced_prompt(query, matches):
    """Create an enhanced prompt using dynamic fine-control"""
    # Base prompt
    prompt = f"User query: {query}\n\n"

    # Add context from knowledge base matches
    if matches:
        prompt += "Relevant information from knowledge base:\n\n"

        for i, match in enumerate(matches):
            if match["type"] == "faq":
                prompt += f"FAQ {i+1} (Relevance: {match['similarity']:.2f}):\n"
                prompt += f"Question: {match['data']['question']}\n"
                prompt += f"Answer: {match['data']['answer']}\n\n"
            else:  # complaint
                prompt += f"Similar Issue {i+1} (Relevance: {match['similarity']:.2f}):\n"
                prompt += f"Problem: {match['data']['description']}\n"
                prompt += f"Solution: {match['data']['solution']}\n\n"

    # Add instructions for response generation
    prompt += "Instructions:\n"
    prompt += "1. Provide a helpful, concise response addressing the user's query.\n"
    prompt += "2. Include specific details from the knowledge base when relevant.\n"
    prompt += "3. If the query mentions specific products, highlight solutions for those products.\n"
    prompt += "4. Format your response in a conversational, supportive tone.\n"
    prompt += "5. If multiple solutions exist, prioritize the most effective one first.\n"

    return prompt
