from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import call, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1].joinpath("src")))
import app as app_module


class AppTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config["TESTING"] = True
        app_module.cache.clear()
        self.client = app_module.app.test_client()

    def tearDown(self):
        app_module.cache.clear()

    def test_health_and_allowed_origins(self):
        for origin in ("https://www.kk-67.com", "http://localhost:3000"):
            with self.subTest(origin=origin):
                response = self.client.get("/", headers={"Origin": origin})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.get_data(as_text=True),
                    "Flask server running on Python 3.12",
                )
                self.assertEqual(
                    response.headers["Access-Control-Allow-Origin"], origin
                )

    def test_disallowed_origin_has_no_cors_header(self):
        response = self.client.get(
            "/", headers={"Origin": "https://example.invalid"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Access-Control-Allow-Origin", response.headers)

    def test_preflight(self):
        response = self.client.options(
            "/posts/fb/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Access-Control-Allow-Origin"],
            "http://localhost:3000",
        )
        self.assertIn("GET", response.headers["Access-Control-Allow-Methods"])

    def test_first_pages_are_cached_and_paging_urls_are_removed(self):
        for route, loader_name, edge in (
            ("fb", "load_posts_from_facebook", "posts"),
            ("ig", "load_posts_from_instagram", "media"),
        ):
            with self.subTest(route=route):
                page = {
                    edge: {
                        "data": [],
                        "paging": {
                            "cursors": {"before": "first", "after": "last"},
                            "next": "https://example.invalid/?access_token=fixture",
                        },
                    }
                }
                with patch.object(
                    app_module, loader_name, return_value=deepcopy(page)
                ) as loader:
                    first = self.client.get(f"/posts/{route}/")
                    second = self.client.get(f"/posts/{route}/")
                self.assertEqual(first.status_code, 200)
                self.assertTrue(first.is_json)
                self.assertEqual(first.get_json(), second.get_json())
                self.assertEqual(
                    first.get_json()[edge]["paging"],
                    {"cursors": {"after": "last"}},
                )
                loader.assert_called_once_with(None)

    def test_pagination_is_not_cached(self):
        for route, loader_name, edge in (
            ("fb", "load_posts_from_facebook", "posts"),
            ("ig", "load_posts_from_instagram", "media"),
        ):
            with self.subTest(route=route):
                page = {edge: {"data": [], "paging": {"cursors": {}}}}
                with patch.object(
                    app_module, loader_name, return_value=page
                ) as loader:
                    for _ in range(2):
                        response = self.client.get(f"/posts/{route}/cursor")
                        self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    loader.call_args_list, [call("cursor"), call("cursor")]
                )


if __name__ == "__main__":
    unittest.main()
