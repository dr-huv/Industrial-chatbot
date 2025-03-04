def evaluate_response(query, response):
    """Evaluate and potentially improve a response"""
    # This is a simplified version of the self-rewarding mechanism

    # Check if response is too short
    if len(response) < 50:
        response += " Please let me know if you need more detailed information on this topic."

    # Check if response doesn't address specific products mentioned in query
    product_keywords = ["machine", "device",
                        "equipment", "system", "tool", "unit"]
    query_has_product = any(keyword in query.lower()
                            for keyword in product_keywords)

    if query_has_product and not any(keyword in response.lower() for keyword in product_keywords):
        response += " This solution applies to most industrial equipment, but may vary slightly depending on your specific model or configuration."

    # Check if response doesn't include next steps
    action_words = ["try", "check", "ensure", "adjust", "contact", "replace"]
    if not any(word in response.lower() for word in action_words):
        response += " I recommend checking your system documentation for model-specific instructions or contacting your maintenance team if the issue persists."

    return response
