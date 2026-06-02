from brb.llm.BaseLLM import BaseLLM
from google import genai
from brb.llm.errors import GeminiError

_PROMPT = """
    Base on the following message and the last {l} terminal commands, write what the user was working on:
    
    Message: {message}
    
    Terminal Commands: {lastcommands}
"""

class GeminiLLM(BaseLLM):
    _client: genai.Client | None = None

    def __init__(self, api_key: str | None, model: str = "gemini-2.5-flash-lite"):
        if api_key is None:
            raise GeminiError("API key is required. Run: brb set-key <your_api_key>")
        if GeminiLLM._client is None:
            GeminiLLM._client = genai.Client(api_key = api_key)
        self.model = model

    def createMessage(self, message, lastcommands: list[str]) -> str:
        fullprompt = _PROMPT.format(l=len(lastcommands), message=message, lastcommands=lastcommands)
        response = GeminiLLM._client.models.generate_content(
            model = self.model,
            contents = fullprompt,
        )

        if response.text is None:
            raise GeminiError(response)

        return response.text