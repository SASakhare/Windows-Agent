# tools/reasoning/reasoning_tool.py
import os
from typing import Any, Dict, List, Optional

from src.agent.tools.base_tool import BaseTool
from .prompts import build_prompt


class ReasoningTool(BaseTool):
    """Cognitive tasks that don't touch the OS, browser, or filesystem:
    answering questions, summarizing, translating, brainstorming,
    planning, analysis, and code/text generation. Backed by an LLM
    call, not by any external system.
    """

    def __init__(self, model: str = "claude-sonnet-4-6") -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set.")
        self._client = None
        self._model = model

    @property
    def name(self) -> str:
        return "reasoning"

    @property
    def description(self) -> str:
        return "Think, analyze, summarize, translate, plan, brainstorm, and generate text/code via an LLM call."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "answer": self.answer,
            "explain": self.explain,
            "summarize": self.summarize,
            "translate": self.translate,
            "rewrite": self.rewrite,
            "proofread": self.proofread,
            "brainstorm": self.brainstorm,
            "plan": self.plan,
            "extract": self.extract,
            "analyze": self.analyze,
            "compare": self.compare,
            "critique": self.critique,
            "generate_code": self.generate_code,
            "write_email": self.write_email,
            "write_document": self.write_document,
            "fallback":self.fallback,
        }
        if action not in actions:
            if action not in actions:
                # Unknown action name entirely (typo, made-up action) — still
                # route through fallback instead of raising, since the LLM's
                # intent is recoverable even if the exact action name is wrong.
                return self.fallback(
                    user_input=kwargs.get("prompt") or kwargs.get("question") or kwargs.get("text") or str(kwargs),
                    context=f"Requested unknown action '{action}' on ReasoningTool.",
                )
            
        return actions[action](**kwargs)

    # ==========================================================
    # Core LLM call — shared by every method below
    # ==========================================================

    def _call(self, prompt: str, max_tokens: int = 1024) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text")

    # ==========================================================
    # Question answering / explanation
    # ==========================================================

    def answer(self, question: str) -> str:
        """Answer a factual or conceptual question.

        Args:
            question: The question to answer.

        Returns:
            The answer text.
        """
        return self._call(build_prompt("answer", prompt=question))

    def explain(self, content: str) -> str:
        """Explain a concept, code snippet, or idea in simple terms.

        Args:
            content: The concept or code to explain.

        Returns:
            The explanation text.
        """
        return self._call(build_prompt("explain", prompt=content))

    # ==========================================================
    # Summarization / translation
    # ==========================================================

    def summarize(self, text: str, length: str = "3-5 sentences") -> str:
        """Summarize a piece of text.

        Args:
            text: Text to summarize.
            length: Desired summary length, e.g. "one sentence", "a paragraph".

        Returns:
            The summary text.
        """
        return self._call(build_prompt("summarize", prompt=text, length=length))

    def translate(self, text: str, target_language: str) -> str:
        """Translate text into another language.

        Args:
            text: Text to translate.
            target_language: Language to translate into, e.g. "Hindi", "Marathi".

        Returns:
            The translated text.
        """
        return self._call(build_prompt("translate", prompt=text, target_language=target_language))

    # ==========================================================
    # Text editing
    # ==========================================================

    def rewrite(self, text: str, style: str = "clearer and more concise") -> str:
        """Rewrite text in a different style/tone.

        Args:
            text: Text to rewrite.
            style: Desired style, e.g. "more formal", "friendlier", "shorter".

        Returns:
            The rewritten text.
        """
        return self._call(build_prompt("rewrite", prompt=text, style=style))

    def proofread(self, text: str) -> str:
        """Proofread text for grammar/clarity issues and return corrections.

        Args:
            text: Text to proofread.

        Returns:
            List of issues found plus a corrected version.
        """
        return self._call(build_prompt("proofread", prompt=text))

    # ==========================================================
    # Brainstorming / planning
    # ==========================================================

    def brainstorm(self, topic: str, count: int = 5) -> str:
        """Brainstorm ideas for a topic or problem.

        Args:
            topic: The topic or problem to brainstorm about.
            count: Number of distinct ideas to generate.

        Returns:
            List of ideas as text.
        """
        return self._call(build_prompt("brainstorm", prompt=topic, count=count))

    def plan(self, goal: str) -> str:
        """Create a step-by-step plan for a goal.

        Args:
            goal: The goal to plan for.

        Returns:
            A step-by-step plan as text.
        """
        return self._call(build_prompt("plan", prompt=goal))

    # ==========================================================
    # Extraction / analysis
    # ==========================================================

    def extract(self, text: str, what: str = "key entities and facts") -> str:
        """Extract specific information from text (entities, tasks,
        requirements, keywords, etc).

        Args:
            text: Text to extract from.
            what: What to extract, e.g. "action items", "dates", "requirements".

        Returns:
            Extracted items as a bulleted list.
        """
        return self._call(build_prompt("extract", prompt=text, what=what))

    def analyze(self, subject: str) -> str:
        """Analyze a topic, decision, or piece of content for key
        considerations and trade-offs.

        Args:
            subject: What to analyze.

        Returns:
            The analysis text.
        """
        return self._call(build_prompt("analyze", prompt=subject))

    def compare(self, options: str) -> str:
        """Compare two or more options.

        Args:
            options: Description of the options to compare, e.g.
                "React vs Vue for a small team".

        Returns:
            Comparison text covering pros/cons of each option.
        """
        return self._call(build_prompt("compare", prompt=options))

    def critique(self, content: str) -> str:
        """Critique content and suggest improvements.

        Args:
            content: The content to critique (text, code, plan, etc).

        Returns:
            Critique text with identified weaknesses and suggestions.
        """
        return self._call(build_prompt("critique", prompt=content))

    # ==========================================================
    # Generation
    # ==========================================================

    def generate_code(self, instruction: str, language: str = "python") -> str:
        """Generate code for a given requirement.

        Args:
            instruction: What the code should do.
            language: Programming language to generate.

        Returns:
            Generated code with brief comments.
        """
        return self._call(build_prompt("generate_code", prompt=instruction, language=language))

    def write_email(self, instruction: str, tone: str = "professional") -> str:
        """Write an email for a given purpose.

        Args:
            instruction: What the email should accomplish, e.g. "leave application for 2 days".
            tone: Tone of the email, e.g. "professional", "casual", "apologetic".

        Returns:
            The drafted email text.
        """
        return self._call(build_prompt("write_email", prompt=instruction, tone=tone))

    def write_document(self, instruction: str, doc_type: str = "report") -> str:
        """Write a document (report, README, blog post, etc).

        Args:
            instruction: What the document should cover.
            doc_type: Type of document, e.g. "README", "blog post", "SOP".

        Returns:
            The drafted document text.
        """
        return self._call(build_prompt("write_document", prompt=instruction, doc_type=doc_type))


    def fallback(self, user_input: str, context: Optional[str] = None) -> str:
        """Fallback handler for when no specific tool or action matches
        the user's request. Answers directly using the LLM with whatever
        context is available, rather than failing with 'unknown action'.

        Use this when:
        - The planner couldn't map the request to any registered tool.
        - The request is a general conversational question with no
        clear action (e.g. "what do you think about X").
        - All other ReasoningTool methods are a poor fit for the phrasing.

        Args:
            user_input: The original, unmodified user question/request.
            context: Optional extra context (e.g. conversation history,
                partial results from earlier failed tool attempts, or a
                note on why no tool matched) to help the LLM respond well.

        Returns:
            The LLM's best-effort response to the user's request.
        """
        prompt = (
            "You are an AI agent's fallback reasoning step. No specific tool "
            "or action matched the user's request, so respond to it directly "
            "and helpfully using your own knowledge and judgement.\n\n"
        )
        if context:
            prompt += f"Context:\n{context}\n\n"
        prompt += f"User request:\n{user_input}"

        return self._call(prompt)

if __name__ == "__main__":
    tool = ReasoningTool()
    print(tool.execute("answer", question="What is a BLE GATT service?"))
    print(tool.execute("plan", goal="Migrate a Flask app to FastAPI"))