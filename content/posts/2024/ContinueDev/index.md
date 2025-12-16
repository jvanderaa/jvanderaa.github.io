---
date: 2024-09-07
slug: continue-dev
categories:
- linux
- ai
title: Code Completion in VS Code with Ollama
toc: true
author: jvanderaa
params:
  showComments: true
---

The year 2024 will showcase the remarkable evolution and contributions of AI. One prominent application of AI lies in its ability to streamline the coding process. In this post I demonstrate how to utilize the [Continue](https://continue.dev) VS Code plugin as a viable alternative to the GitHub Copilot system. This will allow you to have choice on the AI back end or in this scenario, the capability to self host the AI system using [Ollama](https://ollama.com).

<!--more-->

## Getting Code Completion in VSCode

The realm of code completion tools is vast and varied, with  standing as a pioneer. This paid subscription service harnesses AI to empower developers with code completion, chat commands, and seamless interaction with their codebase. While a powerful asset, my deep involvement in open-source projects has drawn me to the impressive AI system within the  project. My curiosity about its potential led me to the exciting discovery that the plugin can recreate the [GitHub Copilot](https://github.com/features/copilot) experience within VSCode by leveraging [Ollama](https://ollama.com).

## Continue.dev

The Continue.dev plugin empowers developers in both VS Code and JetBrains environments by seamlessly integrating with a diverse array of AI systems, transforming them into invaluable coding assistants.  These AI connections include:

- [Ollama](https://ollama.com)
- [OpenAI](https://openai.com/)
- [Together](https://www.together.ai/)
- [Anthropic](https://anthropic.com/)
- [Mistral](https://mistral.ai/)
- [LM Studio](https://lmstudio.ai)

This flexibility in choosing your AI assistant ensures that developers can tailor their coding experience to their specific needs and preferences.  It's a feature that holds tremendous promise, and I'm eager to explore its potential.

## Ollama: Your Gateway to Open-Source LLM Access

Ollama emerges as a compelling open-source solution, offering the capability to leverage Large Language Models (LLMs) without incurring subscription costs. By harnessing your existing hardware and systems, Ollama provides a cost-effective pathway to integrating powerful AI language capabilities into your projects.

### Ollama: Embracing Local Execution

Ollama extends its accessibility across the three major platforms: Linux, MacOS, and Windows. Detailed installation guides tailored to your specific platform are readily available [here](https://ollama.com/download). If you're equipped with a Mac featuring Apple Silicon, Ollama seamlessly runs directly on your machine. However, for other systems, additional hardware might be necessary to unlock Ollama's full potential.

In my case, I repurposed my [Dev Workstation](https://josh-v.com/desktop-build-2023/), augmenting it with a more powerful graphics card. While my original setup sufficed for non-intensive tasks, the surging prominence of AI prompted this strategic investment. Initiating Ollama via the provided shell script proved effortless. Subsequently, I configured Ollama for network accessibility, enabling its utilization across my local development environment, spanning both my primary development machine and other devices I leverage for coding endeavors.

{{< alert "circle-info" >}}
**Exposing Ollama to the Local Network**

I'll be covering this in another blog post soon, the next one up after this!

{{< /alert >}}
{{< alert "circle-info" >}}
**What is Ollama?**

If you are looking for more of what Ollama is, perhaps the best route is to review the [NetworkChuck YouTube video](https://www.youtube.com/watch?v=Wjrdr0NU4Sk) on it. The short story is that Ollama helps to provide LLM capabilities locally. I combine it with [Open WebUI](https://openwebui.com/) to get the same LLM experience that you get with ChatGPT locally.

{{< /alert >}}
## Continue

With Ollama successfully set up, it's time to harness its power within your preferred development environment. Install the Continue plugin for VS Code (while I'm demonstrating this in VS Code, it functions seamlessly in JetBrains products as well). Once Continue is installed and configured to connect to your local Ollama instance, you'll unlock real-time code completion suggestions directly within your editor.

Let's put this into action by creating a new file. I've named mine `try_code_complete.py`. I personally use the `try_` prefix to denote files that are part of my active experimentation and development process.

### Generating Code To Start

The first piece of Continue is that you can use the keyboard shortcut `Ctrl+I` / `Cmd+I` to bring up a prompt to send to the Ollama model (starcoder2). I sent a request to `Generate a hello world python file`. 

![Continue Prompt in VS Code](./prompt.png)

I then got back the following:

```python
import requests
import time
from colorama import Fore, Style


def main():
    print(f"{Fore.CYAN}What's your name? {Style.RESET_ALL}")
    name = input()

    for i in range(5):
        time.sleep(.1)
        print(
            f"{Fore.GREEN}Hello, {name}! {i + 1}/{5} {Style.RESET_ALL}", end="\r"
        )


if __name__ == "__main__":
    main()

```

As with using AI in any system, there are going to be some things that are not quite right at times. In this case, it generated a new to me type of Hello World file that blinked the name entered in via text. However, the blinking happened so fast, that I barely noticed what it was doing initially. The second inacurracy is that the requests library is not used by the script anywhere. So there is no need to import the requests library. Updating the Python code to blink more slowly and removing the requests library I came up with this:

```python
import time
from colorama import Fore, Style


def main():
    print(f"{Fore.CYAN}What's your name? {Style.RESET_ALL}")
    name = input()

    for i in range(5):
        time.sleep(1)
        print(
            f"{Fore.GREEN}Hello, {name}! {i + 1}/{5} {Style.RESET_ALL}", end="\r"
        )


if __name__ == "__main__":
    main()
```

With this updated, I can now see the output a little better, during one of the output prompts I captured:

```
What's your name? 
Josh-V
Hello, Josh-V! 4/5 

```

### Code Completion

Next up is the code completion. With a new file I started filling in the start of things of having a personal Hello World with providing the comment `Add two random numbers together`. It then generated the output as one may expect for using random:

![alt text](image.png)

What was not completed with the code completion was the import of the library into the file. So just relying on the code completion itself is not a recommended expectation that the code will just work. You need to know where things are going and what can be done.

With code completion, I have found that writing the comments of what you intend to do will help out the system significantly. Which when using code completion to assist you in your code writing, will get your code more completely documented.

### Code Tests

As an example, the continue.dev team included a custom command for testing code as an example. The configuration for continue is stored in the `~/.continue/config.json` file. This file contains the configurations that are used by the continue.dev tooling. It also includes the custom commands that are available to be run. 

The JSON snippet for the custom command is:

```json
  "customCommands": [
    {
      "name": "test",
      "prompt": "{{{ input }}}\n\nWrite a comprehensive set of unit tests for the selected code. It should setup, run tests that check for correctness including important edge cases, and teardown. Ensure that the tests are complete and sophisticated. Give the tests just as chat output, don't edit any file.",
      "description": "Write unit tests for highlighted code"
    }
  ],
```

When using the Continue chat (on the right of the VS Code browser), you can use slash commands to execute the various prompt. For example, to run the test command on the selected code, you would type `/test`. When this executed the system provided a test that would provide Python Unittest output. While Unittest is great, I prefer to use pytest myself from a readability perspective and output readability. So I created a second chat command, pytest, that would be the same command as seen above in pytest format.

{{< alert "circle-info" >}}
**Where is the toolbar?**

In my VS Code, the right hand toolbar was missing. I could not find the Continue plugin anywhere. It was within the Secondary Side Bar. To show the secondary toolbar, use the View menu on VS code. In the Linux version of the app, it is nested in View > Appearance.

{{< /alert >}}
```json
  "customCommands": [
    {
      "name": "pytest",
      "prompt": "{{{ input }}}\n\nWrite a comprehensive set of unit tests for the selected code using pytest. It should setup, run tests that check for correctness including important edge cases, and teardown. Ensure that the tests are complete and sophisticated. Give the tests just as chat output, don't edit any file.",
      "description": "Write unit tests for highlighted code"
    }
  ],
```

Now it gives the results in pytest format. As part of the reading of the code to generate the tests, it suggested that I convert the straight multiplication into a function that calculates the area. So after adding the function, highlighting the function, and using the chat to generate the pytest tests, here is the recommended pytest file:

```python
# tests/test_file.py

import pytest
from file import calculate_area


@pytest.fixture
def rectangle_data():
    return [
        {"length": 2, "width": 3},
        {"length": 4, "width": 5},
        {"length": 0, "width": 0},
        {"length": -1, "width": 2},
    ]


class TestCalculateArea:
    @pytest.mark.parametrize("input_data", rectangle_data)
    def test_calculate_area(self, input_data):
        length = input_data["length"]
        width = input_data["width"]
        expected_area = length * width
        assert calculate_area(length, width) == expected_area

    def test_calculate_area_zero_length(self):
        length = 0
        width = 3
        expected_area = 0
        assert calculate_area(length, width) == expected_area

    def test_calculate_area_negative_length(self):
        length = -1
        width = 2
        expected_area = 0  # Area of a rectangle with negative length is not defined in the problem, so we set it to 0 for simplicity
        assert calculate_area(length, width) == expected_area

    def test_calculate_area_zero_width(self):
        length = 4
        width = 0
        expected_area = 0
        assert calculate_area(length, width) == expected_area

    def test_calculate_area_both_zero(self):
        length = 0
        width = 0
        expected_area = 0
        assert calculate_area(length, width) == expected_area

```

## Summary

The AI space is currently undergoing a period of rapid evolution. New ideas and articles are emerging almost daily, highlighting the exciting potential of this technology. Leveraging AI and LLMs for assistance remains an area of active development and innovation. Continue.dev's ability to connect LLMs with IDEs like VS Code and JetBrains products promises further improvements in code quality and development workflows.

For me, a prime example of this potential lies in generating unit tests for existing codebases. This offers a powerful method for preventing regression bugs and ensuring code stability.

We are only beginning to explore the possibilities of AI-assisted coding. The examples shared here demonstrate the capabilities of Continue.dev and Ollama in streamlining development tasks, from code completion to unit test generation. Crucially, AI should not be viewed as a replacement for writing code but rather as a valuable tool to augment your own skills and expertise. It remains essential to understand the code generated by AI and to ensure adherence to best practices.

The combination of Continue.dev, Ollama, and your own coding prowess opens doors to enhanced productivity and code quality. By embracing AI assistance responsibly and strategically, developers can unlock new levels of efficiency and innovation.

> [!INFO]- Editorial assistance
> This blog post had editing assistance from Google Gemini Advanced - 2024-09-07. The structure of the post was not altered and no significant content was added by the editing.