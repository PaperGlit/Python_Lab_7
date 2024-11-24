import unittest
from unittest.mock import patch, Mock
from DAL.classes.api_repository import ApiRepository


class TestApiRepository(unittest.TestCase):
    def setUp(self):
        """Set up an instance of ApiRepository for testing."""
        self.base_url = "https://jsonplaceholder.typicode.com/posts"
        self.api_repo = ApiRepository(self.base_url)

    @patch("requests.get")
    def test_get_all(self, mock_get):
        """Test the get_all method."""
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: [
                {"id": 1, "title": "Post 1"},
                {"id": 2, "title": "Post 2"}
            ],
        )

        result = self.api_repo.get_all()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Post 1")
        mock_get.assert_called_once_with(self.base_url)

    @patch("requests.get")
    def test_get_by_id(self, mock_get):
        """Test the get_by_id method."""
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"id": 1, "title": "Post 1"}
        )

        result = self.api_repo.get_by_id(1)
        self.assertEqual(result["title"], "Post 1")
        mock_get.assert_called_once_with(f"{self.base_url}/1")

    @patch("requests.post")
    def test_add(self, mock_post):
        """Test the add method."""
        mock_post.return_value = Mock(
            status_code=201,
            json=lambda: {"id": 101, "title": "New Post"}
        )

        data = {"title": "New Post", "body": "Content of the post"}
        result = self.api_repo.add(data)

        self.assertEqual(result["id"], 101)
        self.assertEqual(result["title"], "New Post")
        mock_post.assert_called_once_with(self.base_url, json=data)

    @patch("requests.patch")
    def test_update(self, mock_patch):
        """Test the update method."""
        mock_patch.return_value = Mock(
            status_code=200,
            json=lambda: {"id": 1, "title": "Updated Post"}
        )

        data = {"title": "Updated Post"}
        result = self.api_repo.update(1, data)

        self.assertEqual(result["title"], "Updated Post")
        mock_patch.assert_called_once_with(f"{self.base_url}/1", json=data)

    @patch("requests.delete")
    def test_delete(self, mock_delete):
        """Test the delete method."""
        mock_delete.return_value = Mock(status_code=200)

        result = self.api_repo.delete(1)
        self.assertTrue(result)
        mock_delete.assert_called_once_with(f"{self.base_url}/1")