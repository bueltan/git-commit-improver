import unittest
from unittest.mock import patch, MagicMock
import io
import json
from urllib import request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"  # or "llama3:instruct"


# Import from your script (adjust path if needed)
import modify_commit_msg as mco

class TestModifyCommitMsg(unittest.TestCase):

    @patch("modify_commit_msg.request.urlopen")
    def test_call_llama_success(self, mock_urlopen):
        # Mock response content
        mock_response = {"response": "Refactor authentication logic for clarity."}
        mock_stream = io.BytesIO(json.dumps(mock_response).encode("utf-8"))
        mock_urlopen.return_value.__enter__.return_value = mock_stream

        # Test the function
        input_prompt = "fix auth bug"
        expected = "Refactor authentication logic for clarity."
        result = mco.call_llama(input_prompt)

        self.assertEqual(result, expected)

    @patch("modify_commit_msg.call_llama", return_value="Improved message")
    def test_main_writes_updated_message(self, mock_call_llama):
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile("w+", delete=False) as tmpfile:
            tmpfile.write("Initial message")
            tmpfile.flush()
            tmpfile_name = tmpfile.name

        # Simulate command-line args
        with patch("sys.argv", ["script", tmpfile_name]):
            mco.main()

        # Read the updated file
        with open(tmpfile_name, "r") as f:
            updated_content = f.read()

        self.assertEqual(updated_content, "Improved message")

class TestOllamaIntegration(unittest.TestCase):
    def test_llama_responds_to_prompt(self):
        prompt = "Fix spelling and grammar. Only reply with the corrected text: fix an bug in the loggin form valaidation"
        payload = json.dumps({
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }).encode("utf-8")

        req = request.Request(OLLAMA_URL, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")

        with request.urlopen(req) as resp:
            result = json.load(resp)
    
        print("LLaMA response:", result["response"].strip())
        assert (result["response"].strip() == "Fix a bug in the login form validation.")
        self.assertIn("login", result["response"].lower())
        self.assertIn("bug", result["response"].lower())

if __name__ == "__main__":
    unittest.main()
