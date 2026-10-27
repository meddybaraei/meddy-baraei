# agent-hub

A Claude Code mod that adds:

- **Agents dashboard pane**: shows each sub-agent in this session (status, model, what it is doing now), the other sessions it can reach, and the messages sent between them. Open it with `/agent-hub`.
- **Session-to-session messaging**: `/msg <session or agent name> <text>` sends a message to another running session or agent. Claude can also message other sessions with its own SendMessage tool, and those messages show in the pane.
- **Cheaper model for simple jobs**: sub-agents doing simple work (lookups, searches, short summaries, renames, formatting) run on `haiku`. Design, debugging, refactoring and build work stays on the main model. It also adds an `agent-hub:quick` agent type that always runs on the cheaper model. Turn this on or off with `/cheap on` or `/cheap off`, or with the button in the pane. You can change the model under `/config` (`cheapModel`).

## Install

Load it for one session with `claude --plugin-dir mods/agent-hub`.
