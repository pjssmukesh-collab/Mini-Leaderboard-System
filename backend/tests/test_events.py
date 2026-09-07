# tests/test_events.py
# ──────────────────────────────────────────────
# Event Management Module Test Suite
# ──────────────────────────────────────────────

import unittest
from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.testclient import TestClient

from app.database.database import init_db, drop_db
from app.main import app


class TestEventManagement(unittest.TestCase):
    """Test suite for Event CRUD endpoints, validation, filters, and authorization."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        drop_db()
        init_db()

        # Register users for testing
        # 1. Creator A (owner of event A)
        self.client.post(
            "/auth/register",
            json={"name": "Creator Alice", "email": "alice@event.com", "password": "Password123!", "role": "creator"},
        )
        self.alice_token = self.client.post(
            "/auth/login",
            json={"email": "alice@event.com", "password": "Password123!"},
        ).json()["access_token"]
        self.alice_headers = {"Authorization": f"Bearer {self.alice_token}"}

        # 2. Creator B (non-owner)
        self.client.post(
            "/auth/register",
            json={"name": "Creator Bob", "email": "bob@event.com", "password": "Password123!", "role": "creator"},
        )
        self.bob_token = self.client.post(
            "/auth/login",
            json={"email": "bob@event.com", "password": "Password123!"},
        ).json()["access_token"]
        self.bob_headers = {"Authorization": f"Bearer {self.bob_token}"}

        # 3. Admin
        self.client.post(
            "/auth/register",
            json={"name": "Admin Super", "email": "admin@event.com", "password": "Password123!", "role": "admin"},
        )
        self.admin_token = self.client.post(
            "/auth/login",
            json={"email": "admin@event.com", "password": "Password123!"},
        ).json()["access_token"]
        self.admin_headers = {"Authorization": f"Bearer {self.admin_token}"}

        # 4. Player
        self.client.post(
            "/auth/register",
            json={"name": "Player Peter", "email": "peter@event.com", "password": "Password123!", "role": "player"},
        )
        self.player_token = self.client.post(
            "/auth/login",
            json={"email": "peter@event.com", "password": "Password123!"},
        ).json()["access_token"]
        self.player_headers = {"Authorization": f"Bearer {self.player_token}"}

    def tearDown(self):
        drop_db()

    # ──────────────────────────────────────────
    # 1. POST /events Tests (Creation & Authorization)
    # ──────────────────────────────────────────
    def test_01_create_event_by_creator(self):
        """Test that a Tournament Creator can create events across multiple event types."""
        now = datetime.now(timezone.utc)
        payload = {
            "name": "Summer Gaming Cup 2026",
            "event_type": "gaming",
            "description": "Squad battle royale competition.",
            "start_date": now.isoformat(),
            "end_date": (now + timedelta(days=3)).isoformat(),
            "participant_limit": 64,
            "status": "draft",
        }
        res = self.client.post("/events", json=payload, headers=self.alice_headers)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.json()
        self.assertEqual(data["name"], "Summer Gaming Cup 2026")
        self.assertEqual(data["event_type"], "gaming")
        self.assertEqual(data["participant_limit"], 64)
        self.assertEqual(data["status"], "draft")
        self.assertIsNotNone(data["id"])

    def test_02_create_event_by_admin(self):
        """Test that an Admin can create events."""
        payload = {
            "name": "Grandmaster Chess Blitz",
            "event_type": "chess",
            "description": "Rapid Swiss format tournament",
            "participant_limit": 32,
            "status": "active",
        }
        res = self.client.post("/events", json=payload, headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()["name"], "Grandmaster Chess Blitz")

    def test_03_create_event_by_player_forbidden(self):
        """Test that a Player cannot create an event (HTTP 403 Forbidden)."""
        payload = {
            "name": "Unauthorized Player Tournament",
            "event_type": "coding",
            "status": "draft",
        }
        res = self.client.post("/events", json=payload, headers=self.player_headers)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_04_create_event_unauthenticated_unauthorized(self):
        """Test unauthenticated POST /events returns HTTP 401."""
        payload = {"name": "No Token Cup", "event_type": "quiz", "status": "draft"}
        res = self.client.post("/events", json=payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_05_date_validation_failure(self):
        """Test that end_date prior to start_date raises validation error (HTTP 422)."""
        now = datetime.now(timezone.utc)
        payload = {
            "name": "Time Machine Contest",
            "event_type": "quiz",
            "start_date": now.isoformat(),
            "end_date": (now - timedelta(days=2)).isoformat(),  # Invalid end date
            "status": "draft",
        }
        res = self.client.post("/events", json=payload, headers=self.alice_headers)
        self.assertEqual(res.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # ──────────────────────────────────────────
    # 2. GET /events & GET /events/{id} Tests
    # ──────────────────────────────────────────
    def test_06_list_and_filter_events(self):
        """Test event listing, type filtering, status filtering, search, and pagination."""
        # Create multiple events
        self.client.post(
            "/events",
            json={"name": "Cyber Coding Hackathon", "event_type": "coding", "status": "active"},
            headers=self.alice_headers,
        )
        self.client.post(
            "/events",
            json={"name": "Trivia Night Quiz", "event_type": "quiz", "status": "draft"},
            headers=self.alice_headers,
        )
        self.client.post(
            "/events",
            json={"name": "Inter-City Sports Marathon", "event_type": "sports", "status": "completed"},
            headers=self.admin_headers,
        )

        # 1. List all
        res_all = self.client.get("/events")
        self.assertEqual(res_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_all.json()), 3)

        # 2. Filter by event_type
        res_type = self.client.get("/events?event_type=coding")
        self.assertEqual(res_type.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_type.json()), 1)
        self.assertEqual(res_type.json()[0]["name"], "Cyber Coding Hackathon")

        # 3. Filter by status
        res_status = self.client.get("/events?status=completed")
        self.assertEqual(res_status.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_status.json()), 1)
        self.assertEqual(res_status.json()[0]["event_type"], "sports")

        # 4. Search by keyword
        res_search = self.client.get("/events?search=Hackathon")
        self.assertEqual(res_search.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_search.json()), 1)

        # 5. Pagination
        res_page = self.client.get("/events?skip=1&limit=1")
        self.assertEqual(res_page.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_page.json()), 1)

    def test_07_get_event_by_id(self):
        """Test retrieving event by ID and 404 for non-existent event."""
        create_res = self.client.post(
            "/events",
            json={"name": "Single Event Check", "event_type": "other", "description": "Details testing", "status": "draft"},
            headers=self.alice_headers,
        )
        event_id = create_res.json()["id"]

        # Valid ID
        res = self.client.get(f"/events/{event_id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()["name"], "Single Event Check")

        # Invalid ID (404)
        res_404 = self.client.get("/events/999999")
        self.assertEqual(res_404.status_code, status.HTTP_404_NOT_FOUND)

    # ──────────────────────────────────────────
    # 3. PUT /events/{id} Tests (Update & Ownership)
    # ──────────────────────────────────────────
    def test_08_update_event_ownership_rules(self):
        """
        Verify update authorization:
        - Owner Creator can update.
        - Admin can update any event.
        - Non-owner Creator is forbidden (403).
        - Player is forbidden (403).
        """
        create_res = self.client.post(
            "/events",
            json={"name": "Alice's Exclusive Cup", "event_type": "gaming", "status": "draft"},
            headers=self.alice_headers,
        )
        event_id = create_res.json()["id"]

        # 1. Non-owner Creator (Bob) tries to update -> 403
        res_bob = self.client.put(
            f"/events/{event_id}",
            json={"name": "Bob's Hijack Attempt"},
            headers=self.bob_headers,
        )
        self.assertEqual(res_bob.status_code, status.HTTP_403_FORBIDDEN)

        # 2. Player (Peter) tries to update -> 403
        res_peter = self.client.put(
            f"/events/{event_id}",
            json={"name": "Peter's Hack Attempt"},
            headers=self.player_headers,
        )
        self.assertEqual(res_peter.status_code, status.HTTP_403_FORBIDDEN)

        # 3. Owner Creator (Alice) updates -> 200
        res_alice = self.client.put(
            f"/events/{event_id}",
            json={"name": "Alice's Official Tournament", "status": "active", "participant_limit": 128},
            headers=self.alice_headers,
        )
        self.assertEqual(res_alice.status_code, status.HTTP_200_OK)
        self.assertEqual(res_alice.json()["name"], "Alice's Official Tournament")
        self.assertEqual(res_alice.json()["status"], "active")
        self.assertEqual(res_alice.json()["participant_limit"], 128)

        # 4. Admin updates -> 200
        res_admin = self.client.put(
            f"/events/{event_id}",
            json={"status": "completed"},
            headers=self.admin_headers,
        )
        self.assertEqual(res_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(res_admin.json()["status"], "completed")

    # ──────────────────────────────────────────
    # 4. DELETE /events/{id} Tests
    # ──────────────────────────────────────────
    def test_09_delete_event_ownership_rules(self):
        """
        Verify deletion authorization:
        - Non-owner Creator cannot delete (403).
        - Player cannot delete (403).
        - Owner Creator can delete (204).
        - Admin can delete (204).
        """
        # Event 1: deleted by owner
        event1_id = self.client.post(
            "/events",
            json={"name": "To Be Deleted by Alice", "event_type": "chess"},
            headers=self.alice_headers,
        ).json()["id"]

        # Bob attempt -> 403
        self.assertEqual(
            self.client.delete(f"/events/{event1_id}", headers=self.bob_headers).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Player attempt -> 403
        self.assertEqual(
            self.client.delete(f"/events/{event1_id}", headers=self.player_headers).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Alice (owner) deletes -> 204
        self.assertEqual(
            self.client.delete(f"/events/{event1_id}", headers=self.alice_headers).status_code,
            status.HTTP_204_NO_CONTENT,
        )

        # Verify it no longer exists
        self.assertEqual(self.client.get(f"/events/{event1_id}").status_code, status.HTTP_404_NOT_FOUND)

        # Event 2: deleted by Admin
        event2_id = self.client.post(
            "/events",
            json={"name": "To Be Deleted by Admin", "event_type": "coding"},
            headers=self.alice_headers,
        ).json()["id"]

        # Admin deletes -> 204
        self.assertEqual(
            self.client.delete(f"/events/{event2_id}", headers=self.admin_headers).status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(self.client.get(f"/events/{event2_id}").status_code, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
