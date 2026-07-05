# tools/reasoning/prompts.py

PROMPTS = {
    "answer": "Answer the following question clearly and concisely:\n\n{prompt}",
    "explain": "Explain the following concept or code in simple terms:\n\n{prompt}",
    "summarize": "Summarize the following text in {length}:\n\n{prompt}",
    "translate": "Translate the following text to {target_language}. Return only the translation:\n\n{prompt}",
    "rewrite": "Rewrite the following text to be {style}. Return only the rewritten text:\n\n{prompt}",
    "proofread": "Proofread the following text for grammar and clarity issues. List each issue found, then provide a corrected version:\n\n{prompt}",
    "brainstorm": "Brainstorm {count} distinct ideas for the following:\n\n{prompt}",
    "plan": "Create a step-by-step plan for the following goal:\n\n{prompt}",
    "extract": "Extract {what} from the following text. Return as a bulleted list:\n\n{prompt}",
    "analyze": "Analyze the following, covering key considerations and trade-offs:\n\n{prompt}",
    "compare": "Compare the following options: {prompt}. Cover key differences, pros, and cons of each.",
    "critique": "Critique the following, identifying weaknesses and suggesting improvements:\n\n{prompt}",
    "generate_code": "Write {language} code for the following requirement. Return only the code with brief comments:\n\n{prompt}",
    "write_email": "Write a {tone} email for the following purpose:\n\n{prompt}",
    "write_document": "Write a {doc_type} covering the following:\n\n{prompt}",
}


def build_prompt(task: str, **kwargs) -> str:
    """Fill in the template for a given task with provided kwargs."""
    template = PROMPTS.get(task)
    if template is None:
        raise ValueError(f"No prompt template for task '{task}'.")
    try:
        return template.format(**kwargs)
    except KeyError as exc:
        raise ValueError(f"Missing required argument for task '{task}': {exc}") from exc