import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime
from main import app  # Replace with the correct import path


class TestProcessEvent(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("main.get_db_connection")
    def test_process_event_success_status_code(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_conn.commit.return_value = None

        # Prepare test data
        event_data = {
            "userid": "test_user",
            "eventname": "test_event"
        }

        # Send POST request to the /process_event endpoint
        response = self.client.post("/process_event", json=event_data)

        # Assert only the status code
        self.assertEqual(response.status_code, 200)

    @patch("main.get_db_connection")
    def test_process_event_success_message(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_conn.commit.return_value = None

        # Prepare test data
        event_data = {
            "userid": "test_user",
            "eventname": "test_event"
        }

        # Send POST request to the /process_event endpoint
        response = self.client.post("/process_event", json=event_data)

        # Assert only the response message
        self.assertEqual(response.json(), {"message": "Event processed successfully"})

    @patch("main.get_db_connection")
    def test_process_event_db_commit(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_conn.commit.return_value = None

        # Prepare test data
        event_data = {
            "userid": "test_user",
            "eventname": "test_event"
        }

        # Send POST request to the /process_event endpoint
        self.client.post("/process_event", json=event_data)

        # Assert only the database commit
        mock_conn.commit.assert_called_once()

    @patch("main.get_db_connection")
    def test_process_event_db_execute(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_conn.commit.return_value = None

        # Prepare test data
        event_data = {
            "userid": "test_user",
            "eventname": "test_event"
        }

        # Send POST request to the /process_event endpoint
        self.client.post("/process_event", json=event_data)

        # Assert only the execute query
        mock_conn.execute.assert_called_once_with(
            "INSERT INTO events (eventtimestamputc, userid, eventname) VALUES (?, ?, ?)",
            (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), "test_user", "test_event")
        )

    @patch("main.get_db_connection")
    def test_process_event_db_error(self, mock_get_db_connection):
        # Simulate an exception during database operation
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.side_effect = Exception("Database error")

        # Prepare test data
        event_data = {
            "userid": "test_user",
            "eventname": "test_event"
        }

        # Send POST request to the /process_event endpoint
        response = self.client.post("/process_event", json=event_data)

        # Assert only the error message
        self.assertEqual(response.json(), {"error": "Database error"})

    @patch("main.get_db_connection")
    def test_process_event_db_close(self, mock_get_db_connection):
        # Simulate an exception during database operation
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.execute.side_effect = Exception("Database error")

        # Prepare test data
        event_data = {
            "userid": "test_user",
            "eventname": "test_event"
        }

        # Send POST request to the /process_event endpoint
        self.client.post("/process_event", json=event_data)

        # Assert that the database connection was closed
        mock_conn.close.assert_called_once()

    @patch("main.get_db_connection")
    def test_process_event_missing_fields(self, mock_get_db_connection):
        # Prepare test data with missing fields
        event_data = {
            "userid": "test_user"
            # Missing "eventname"
        }

        # Send POST request to the /process_event endpoint
        response = self.client.post("/process_event", json=event_data)

        # Assert only the validation error for missing "eventname"
        self.assertIn("eventname", response.json()['detail'][0]['loc'])


if __name__ == "__main__":
    unittest.main()
