from anthropic import Anthropic

class OutputReviser:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def revise_output_to_comply_with_rules(self, original_output, explanation, recommendation):
        """
        Generates a revised version of the original output that complies with the rules,
        based on the provided explanation and recommendation.

        Args:
            original_output (str): The original output generated by the model.
            explanation (str): Explanation of why the original output was not compliant.
            recommendation (str): Recommendations on how to modify the output to comply.

        Returns:
            str: The revised output that complies with the specified rules.
        """
        request_data = {
            "model": "claude-3-opus-20240229",
            "messages": [
                {
                    "role": "system",
                    "content": "Given the original output, an explanation of a violation, and a recommendation to improve the output, generate a revised output that complies with the rules."
                },
                {
                    "role": "user",
                    "content": f"Original Output:\n{original_output}\n\nExplanation of Violation:\n{explanation}\n\nRecommendation:\n{recommendation}\n\nRevised Output (complying with the rules):"
                }
            ]
        }

        response = self.client.chat.completions.create(**request_data)
        revised_output = response.choices[0].message.content.strip()
        return revised_output