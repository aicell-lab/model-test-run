from pathlib import Path
import tempfile

class Config:
    class Workspace:
        server_url = "https://hypha.aicell.io"
        workspace_id = "model-test"
        workspace_name = "model-test"
        service_id = "model-testing"        
        client_id = "tester"
        client_name = "MTest"
        TOKEN_VAR_NAME = "MTEST_SERVICE_TOKEN"
    class Storage:
        tmp_dir = Path(tempfile.gettempdir())
    UNKNOWN_NAME = "N/A"