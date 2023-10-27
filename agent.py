import argparse
import openai
import rich
from llama_index.agent import OpenAIAgent
from llama_hub.tools.openapi.base import OpenAPIToolSpec
from llama_index.tools.tool_spec.load_and_search.base import LoadAndSearchToolSpec


DEFAULT_API_SPEC = "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json"


def run_agent(api_key: str, api_spec: str=DEFAULT_API_SPEC):
    openai.api_key = api_key

    rich.print("Loading agent, this may take a few seconds...")

    open_spec = OpenAPIToolSpec(url=api_spec)
    wrapped_tools = LoadAndSearchToolSpec.from_defaults(
        open_spec.to_tool_list()[0],
    ).to_tool_list()

    agent = OpenAIAgent.from_tools(wrapped_tools)

    rich.print("Agent loaded, you can now interact with it.")
    print("")

    try:
        while True:
            prompt = input(">>> ")
            response_text = agent.chat(prompt).response
            print("")
            rich.print(response_text)
            print("")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--api_key",
        "-k",
        type=str,
        required=True,
        help="Open AI API key",
    )

    parser.add_argument(
        "--api_spec",
        "-s",
        type=str,
        default=DEFAULT_API_SPEC,
        help="URL for the Open API spec",
    )

    args = parser.parse_args()
    run_agent(**vars(args))