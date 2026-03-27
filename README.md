# Google-Form-Quiz-Maker
## Install and setup python uv
1. Install `uv` using `pip install uv` in cmd.
2. Go to project folder
3. Run
```bash
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

## For AI connection
You can connect any client to this tool, either by programming or using AI Apps.
For **Claude Desktop** on **Windows**:

## Add to Claude
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
You can get `path_to_uv` using where uv in cmd
You have to past parent directory of `tools.py`
3. Restart Claude Desktop

## How to setup for create.py
1. Get `json` file from google cloud console for google forms.
2. Paste it into project as `credentials.json`.
3. Assuming claude has processed and created `form.json`, run `create.py` with `uv`.

Optionally, You can also shuffle questions before `create.py` by running `shuffle.py` with `uv`.
