import unittest

from fastapi_vs_litestar.svc_litestar.app import app
from litestar import status_codes as status
from litestar.testing import TestClient


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_show_item(self):
        client = self.client

        response = client.post(
            "/item", json={"name": "John Doe", "email": "johndoe@example.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_item_id = response.json().get("id")
        self.assertIsNotNone(created_item_id)

        response = client.get(f"/item/{created_item_id}")


if __name__ == "__main__":
    unittest.main()
