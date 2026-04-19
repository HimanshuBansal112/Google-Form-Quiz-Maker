# Google-Form-Quiz-Maker
## Install and setup python uv
1. Install `uv` by running `pip install uv` in Command Prompt.
2. Go to the project folder
3. Run
   
   ```bash
   uv init .
   uv venv
   .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

## For AI connection
You can connect any client to this tool either programmatically or using AI apps.

### How to add to Claude Desktop on Windows
1. Open `claude_desktop_config.json`
2. Add this configuration:
   ```json
    "mcpServers": {
     "quizMaker": {
       "command": "path_to_uv",
       "args": [
         "run",
         "--directory",
         "path_to_this_project",
         "tools.py"
       ]
     }
   }
   ```
   You can get `path_to_uv` using `where uv` in cmd.
   
   You have to paste parent directory of `tools.py` in `path_to_tools.py`.

3. Restart Claude Desktop

### How to add to Codex on Windows
1. Open codex, click on settings.
2. Go to MCP server, click on Add server.
3. Choose STDIO, write name for MCP server.
4. Write `uv` in "Command to launch".
5. Add four Arguments in given order:
   a. --directory
   b. path_to_tools.py
   c. run
   d. tools.py
6. Click on save.

### How to add to Codex CLI on Windows
1. In cmd, run `codex mcp add "quizMaker" -- uv --directory "path_to_tools.py" run tools.py`. You can replace quizMaker, with any server name you want.
2. Now, run `codex` in cmd.
3. You will see mcp connected.

## How to setup for create.py
1. Get JSON file from google cloud console for google forms.
2. Paste it into project as `credentials.json`.
3. Assuming AI has processed using `tools.py` and created `form.json`, run `create.py` with `uv`.

   Optionally, You can also shuffle questions before `create.py` by running `shuffle.py` with `uv`.
