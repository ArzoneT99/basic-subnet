import asyncio
import unittest
from unittest.mock import MagicMock, patch
from socket_io_client import SocketIOClient

class TestSocketIOClient(unittest.IsolatedAsyncioTestCase):
    async def test_get_random_completion(self):
        with patch('socket_io_client.SocketIOClient.getRandomCompletion', new=AsyncMock()) as mock_get_random_completion:
            expected_response = {
                'id': 1,
                'prompt': "What is the capital of France?",
                'response': "The capital of France is Paris.",
                'created_at': "2023-06-08T10:00:00Z",
                'updated_at': "2023-06-08T10:00:00Z",
                'api_key_id': 123
            }
            mock_get_random_completion.return_value = expected_response

            response = await self.client.getRandomCompletion()
            self.assertEqual(response, expected_response)

    async def test_close(self):
        with patch('socket_io_client.SocketIOClient.close', new=AsyncMock()) as mock_close:
            await self.client.close()
            mock_close.assert_called_once()

if __name__ == '__main__':
    unittest.main()