# AgentBF2
Simplest telegram bot for the simplest tasks how to restore order on the battlefield 2 game server

The project is being developed on the basis of aiogram. Python version 3.10. 
Essence of the project is to create a simple application that will allow you to manage BF2 game servers using a telegram bot, that is, remotely ban, kick, and so on.

---
### List of commands
| Name | Arguments | Description |
| ----------- | ----------- | ----------- |
| si | `<server name>` | Information about the server. For example, name, status, current online, current map and next |
| rcon | `<server name>` `<command>` | Sends the rcon command and get a response. A simple command, nothing special |
###### If the argument has `<>`, then it is mandatory, `()` is optional, in front of `*` is a variable number of positional arguments

---
### Config

```
# Telegram bot token.
token: "<token>"
# The list of users, their access level and the servers allowed to them. Here you can configure access to some server and commands.
users:
  # This is the telegram user ID. To find out, use special bots.
  0000000000:
    # Access level. To execute a command, it must be equal to or higher than a certain command. With the help of a system of levels, you can recreate a primitive system of groups, a chief administrator, a chief moderator, a moderator, and so on. wow
    level: 100
    # List of servers. These are the servers that the user can interact with.
    servers:
    - local
# List of commands. Everything is simple here - the name of the team and its level required for its execution.
commands:
  info: 0
# List of servers. It's a little more complicated here. The name of the server and its data for connection, authorization. The data is encrypted (albeit simply). They should not have the original appearance, it's such a simple protection from prying eyes and nothing more.
servers:
  local: "MTI3LjAuMC4xOjQ3MTE6c3VwZXIxMjM="
```
---
> ⚠️ Please do not use this bot on public servers. The project is not ready yet and I hope you understand why you should not do it yet.
