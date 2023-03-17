# Dialogue Director

**This project is in rapid development and subject to change.**

Dialogue Director is a Python-based application that facilitates conversations between multiple ChatGPT agents. The goal of this project is to create engaging multi-agent dialogue using a structured configuration file to define the agents, their prompts, and other parameters.

## Usage

1. Install dependencies:

```shell
pip install -r requirements.txt
```

2. Run the application:

```shell
python dialogue_director.py example.yml
```

- Where `example.yml` is the path to a configuration file.

## Configuration

**The configuration file format is subject to change.**

Dialoge Director is configured with a YAML file which defines the properties of the conversation.

```yaml
parameters:
  ...
agents:
  ...
messages:
  ...
```

See `example.yml` for a full example.

### Parameters

The `parameters` section defines model parameters that will be passed to GPT. See the [OpenAI documentation](https://platform.openai.com/docs/api-reference/chat/create) for a full list.

```yaml
parameters:
  model: "gpt-3.5-turbo"  # Default
  temperature: 1.0        # Default
```

### Agents

The `agents` section defines the dialogue agents and their prompts. The key is the agent's name, and the value is a sub-dictionary of prompts.

- `prompt` specifies the system prompt that is used to generate the agent's response.

```yaml
agents:
  ALICE:
    prompt: |-
      You are Alice and are having a conversation with Bob.
  BOB:
    prompt: |-
      You are Bob and are having a conversation with Alice.
```

### Messages

The `messages` section defines the initial set of messages to start the dialogue. The key is the agent's name, and the value is the message it sent.

```yaml
messages:
  - ALICE: |-
      Hello Bob, how are you?
  - BOB: |-
      I'm well Alice, thanks for asking. How are you?
```
