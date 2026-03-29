# 01 — Hello

Simplest possible adk-teams agent. One persona, no tools, no base inheritance.

## What this teaches

- Minimal `config.yaml` persona definition
- Using `build_persona_prompt` to generate a system prompt from YAML
- Running a single agent with `adk run`

## Run

```bash
pip install -e ../..
cd agents && adk run greeter
```
