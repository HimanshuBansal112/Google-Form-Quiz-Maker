# Google-Form-Quiz-Maker
## Install and setup python uv
1. Install `uv` by running `pip install uv` in Command Prompt.
2. Go to the project folder
3. Run
   
   ```bash
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
   
   You have to paste parent directory of `tools.py` in `path_to_this_project`.

3. Restart Claude Desktop

## How to setup for create.py
1. Get JSON file from google cloud console for google forms.
2. Paste it into project as `credentials.json`.
3. Assuming AI has processed using `tools.py` and created `form.json`, run `create.py` with `uv`.

   Optionally, You can also shuffle questions before `create.py` by running `shuffle.py` with `uv`.
