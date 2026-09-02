# herdr-name-tab

Names every [Herdr](https://herdr.dev) tab with one word, taken from the first thing you typed in it.

```
6921         a Claude Code session porting an issue
proxy-proto  a session designing a protocol
syslog       a shell tailing a log
7083         work on an issue, named by its number
```

A tab keeps its name while the work continues, and is renamed only when the tab turns to an unrelated subject.

## Why not a rule

Tab titles usually come from the agent's session topic, which is a sentence: `claude › Design proxy protocol with protobuf messages`. Reducing that to the word that identifies the work is a judgment, not a string operation:

| Topic | Name | What was dropped |
| --- | --- | --- |
| **Design** proxy protocol with protobuf **messages** | `proxy-proto` | the verb and the filler noun |
| **Agent session** delegation **protocol refactor** | `delegation` | four words, three of them nouns |
| **Cloud** HTTP proxy **status** | `http-proxy` | both ends, keeping the middle |

No positional rule produces those, so a model makes the call.

## Why the name holds still

Asking a model to name the tab from the latest message renames it on every follow-up:

```
auto-title → 36 → herdr-restart      # one continuous task
```

Two things fix that. The **anchor** — the first input in the tab — is sent with every request, and the model judges whether the latest input still belongs to it. And the model is asked to *keep or replace*, seeing the name it already gave, with the bar for replacing set at "someone looking for this work would fail to find it under the old name". The same task now holds:

```
auto-title → auto-title → auto-title → auto-title → door-cam
                                                    ^ unrelated subject
```

Set `temperature: 0` (the default here) so the same input gives the same answer.

## Install

```sh
install -m 755 herdr-name-tab ~/.local/bin/
```

**Agent tabs** — add to `~/.claude/settings.json` so each prompt can name the tab. `async` keeps it off the critical path:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "~/.local/bin/herdr-name-tab", "async": true }] }
    ]
  }
}
```

**Every other tab** — name it from the commands you run:

```sh
cp hooks/herdr-name-tab.fish ~/.config/fish/conf.d/
```

Only a fish hook ships today. For zsh or bash, call `herdr-name-tab <the command line>` from `preexec` or a `DEBUG` trap; the script takes the command as arguments and backgrounds cleanly.

## Configure the model

Without configuration the script shells out to `claude -p`, which works but costs about four seconds per call — nearly all of it booting the CLI — and offers no temperature control, so names wobble. Any OpenAI-compatible endpoint is faster and steadier. Copy `config.example.json` to `~/.config/herdr-name-tab/config.json`:

```json
{
  "api_url": "https://api.openai.com/v1",
  "api_key_env": "OPENAI_API_KEY",
  "model": "gpt-4o-mini",
  "throttle": 60
}
```

A local runtime works and costs nothing per call — the task is small enough for a small model:

```json
{ "api_url": "http://127.0.0.1:11434/v1", "model": "qwen2.5:3b" }
```

Every key can also be set as `HERDR_NAME_TAB_API_URL`, `HERDR_NAME_TAB_MODEL`, and so on. `throttle` is the least time between two evaluations of one tab, in seconds.

A tab named from a **command** is named once and keeps that name: a shell holds many unrelated commands, and re-reading each one would rename the tab all day. Only a tab named from an agent's prompts is re-evaluated, because there the whole session is one task.

## Naming a tab yourself

Rename a tab by hand and the script never touches it again — the name is yours.

To hand a tab back, rename it to `-auto`. The next prompt or command names it afresh.

The anchor is the first input, so a word misheard by voice dictation would otherwise name the tab wrongly for good. When a later input shows the anchor named the wrong thing, the name is corrected; a merely *better* name for the same work is not a reason to rename.

## Relationship to herdr-auto-title

[herdr-auto-title](https://github.com/kryptamine/herdr-auto-title) solves the same problem the opposite way: it polls the session and builds a title from the directory, the branch, the process and the terminal title, deterministically and with no model. It gives you more information per tab. This gives you one word. Pick whichever suits your tab bar; running both means two things renaming the same tabs.

## Licence

MIT
