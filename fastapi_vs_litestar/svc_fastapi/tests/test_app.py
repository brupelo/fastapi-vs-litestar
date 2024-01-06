import unittest

from fastapi import status
from fastapi_vs_litestar.svc_fastapi.app import app
from httpx import AsyncClient


class AppTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncClient(app=app, base_url="http://testserver-fastapi.local")

    async def test_show_item(self):
        client = self.client

        response = await client.post(
            "/item", json={"name": "John Doe", "email": "johndoe@example.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_item_id = response.json().get("id")
        self.assertIsNotNone(created_item_id)

        response = await client.get(f"/item/{created_item_id}")


if __name__ == "__main__":
    unittest.main()
