# tests/test_auth.py
# ──────────────────────────────────────────────
# Authentication & Role-Based Access Control (RBAC) Test Suite
# ──────────────────────────────────────────────

import unittest
from fastapi import FastAPI, Depends, status
from fastapi.testclient import TestClient

from app.core.deps import (
    get_current_user,
    require_admin,
    require_creator,
    require_score_manager,
    require_roles,
)
from app.core.security import UserRole
from app.database.database import SessionLocal, init_db, drop_db
from app.main import app
from app.models.user import User

# Add sample role-protected test endpoints to the app for testing authorization rules
test_app = FastAPI()
# Include the actual auth router
test_app.include_router(app.router)

# 1. Admin-only endpoint (manage users, events, results, leaderboards)
@test_app.get("/test/admin-only")
def admin_only_endpoint(user: User = Depends(require_admin)):
    return {"message": "Welcome Admin", "user_id": user.id}

# 2. Creator endpoint (manage events and scoring rules)
@test_app.post("/test/creator-rules")
def creator_endpoint(user: User = Depends(require_creator)):
    return {"message": "Rules updated", "user_id": user.id}

# 3. Score management endpoint (Creators & Admins allowed; Players forbidden)
@test_app.post("/test/modify-scores")
def score_manager_endpoint(user: User = Depends(require_score_manager)):
    return {"message": "Scores modified", "user_id": user.id}

# 4. Player/Participant browse endpoint
@test_app.get("/test/browse-events")
def player_browse_endpoint(user: User = Depends(get_current_user)):
    return {"message": "Browse allowed", "role": user.role}


class TestAuthAndRBAC(unittest.TestCase):
    """Test suite for authentication endpoints, JWT tokens, and RBAC rules."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(test_app)

    def setUp(self):
        drop_db()
        init_db()

    def tearDown(self):
        drop_db()

    # ──────────────────────────────────────────
    # 1. Registration Tests
    # ──────────────────────────────────────────
    def test_01_user_registration_success(self):
        """Test successful registration with different roles."""
        # Register Player
        res_player = self.client.post(
            "/auth/register",
            json={
                "name": "Player One",
                "email": "player1@test.com",
                "password": "Password123!",
                "role": "player",
            },
        )
        self.assertEqual(res_player.status_code, status.HTTP_201_CREATED)
        data = res_player.json()
        self.assertEqual(data["name"], "Player One")
        self.assertEqual(data["email"], "player1@test.com")
        self.assertEqual(data["role"], "player")
        self.assertIn("id", data)

        # Register Creator
        res_creator = self.client.post(
            "/auth/register",
            json={
                "name": "Creator Alice",
                "email": "creator@test.com",
                "password": "Password123!",
                "role": "creator",
            },
        )
        self.assertEqual(res_creator.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_creator.json()["role"], "creator")

        # Register Admin
        res_admin = self.client.post(
            "/auth/register",
            json={
                "name": "Admin Bob",
                "email": "admin@test.com",
                "password": "Password123!",
                "role": "admin",
            },
        )
        self.assertEqual(res_admin.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_admin.json()["role"], "admin")

    def test_02_duplicate_email_registration_fails(self):
        """Test that registering with an existing email returns HTTP 400."""
        payload = {
            "name": "First User",
            "email": "duplicate@test.com",
            "password": "Password123!",
            "role": "player",
        }
        res1 = self.client.post("/auth/register", json=payload)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Attempt to register again with same email
        res2 = self.client.post("/auth/register", json=payload)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already exists", res2.json()["detail"])

    # ──────────────────────────────────────────
    # 2. Login Tests
    # ──────────────────────────────────────────
    def test_03_login_success(self):
        """Test successful login returns JWT access token and user info."""
        self.client.post(
            "/auth/register",
            json={
                "name": "Login User",
                "email": "login@test.com",
                "password": "SecretPassword123",
                "role": "player",
            },
        )

        res = self.client.post(
            "/auth/login",
            json={"email": "login@test.com", "password": "SecretPassword123"},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")
        self.assertEqual(data["user"]["email"], "login@test.com")
        self.assertEqual(data["user"]["role"], "player")

    def test_04_login_wrong_password_fails(self):
        """Test that login with incorrect password returns HTTP 401."""
        self.client.post(
            "/auth/register",
            json={
                "name": "User",
                "email": "wrongpw@test.com",
                "password": "CorrectPassword123",
                "role": "player",
            },
        )

        # Wrong password
        res = self.client.post(
            "/auth/login",
            json={"email": "wrongpw@test.com", "password": "IncorrectPassword"},
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid email or password", res.json()["detail"])

        # Non-existent email
        res_nonexistent = self.client.post(
            "/auth/login",
            json={"email": "nobody@test.com", "password": "AnyPassword"},
        )
        self.assertEqual(res_nonexistent.status_code, status.HTTP_401_UNAUTHORIZED)

    # ──────────────────────────────────────────
    # 3. Protected Endpoint Tests (/auth/me)
    # ──────────────────────────────────────────
    def test_05_auth_me_protected_endpoint(self):
        """Test GET /auth/me returns 401 without token, and 200 with valid token."""
        # Unauthenticated request
        res_unauth = self.client.get("/auth/me")
        self.assertEqual(res_unauth.status_code, status.HTTP_401_UNAUTHORIZED)

        # Invalid token
        res_invalid = self.client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid.jwt.token"},
        )
        self.assertEqual(res_invalid.status_code, status.HTTP_401_UNAUTHORIZED)

        # Register and Login
        self.client.post(
            "/auth/register",
            json={
                "name": "Profile Owner",
                "email": "me@test.com",
                "password": "Password123!",
                "role": "creator",
            },
        )
        login_res = self.client.post(
            "/auth/login",
            json={"email": "me@test.com", "password": "Password123!"},
        )
        token = login_res.json()["access_token"]

        # Authenticated request with Bearer token
        res_auth = self.client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(res_auth.status_code, status.HTTP_200_OK)
        user_data = res_auth.json()
        self.assertEqual(user_data["name"], "Profile Owner")
        self.assertEqual(user_data["email"], "me@test.com")
        self.assertEqual(user_data["role"], "creator")

    # ──────────────────────────────────────────
    # 4. Role-Based Access Control (RBAC) Tests
    # ──────────────────────────────────────────
    def test_06_role_restrictions(self):
        """
        Verify role-based access rules:
        - Admin can access admin endpoints; Creator & Player are forbidden (403)
        - Creator & Admin can manage scoring rules; Player is forbidden (403)
        - Creator & Admin can modify scores; Players are forbidden from modifying scores (403)
        - All authenticated roles can access player/browse endpoints
        """
        # Register 3 users with different roles
        self.client.post(
            "/auth/register",
            json={"name": "Player 1", "email": "p@test.com", "password": "Password123!", "role": "player"},
        )
        self.client.post(
            "/auth/register",
            json={"name": "Creator 1", "email": "c@test.com", "password": "Password123!", "role": "creator"},
        )
        self.client.post(
            "/auth/register",
            json={"name": "Admin 1", "email": "a@test.com", "password": "Password123!", "role": "admin"},
        )

        p_token = self.client.post("/auth/login", json={"email": "p@test.com", "password": "Password123!"}).json()["access_token"]
        c_token = self.client.post("/auth/login", json={"email": "c@test.com", "password": "Password123!"}).json()["access_token"]
        a_token = self.client.post("/auth/login", json={"email": "a@test.com", "password": "Password123!"}).json()["access_token"]


        p_headers = {"Authorization": f"Bearer {p_token}"}
        c_headers = {"Authorization": f"Bearer {c_token}"}
        a_headers = {"Authorization": f"Bearer {a_token}"}

        # --- Test 1: Admin-only endpoint ---
        # Admin: 200 OK
        self.assertEqual(self.client.get("/test/admin-only", headers=a_headers).status_code, status.HTTP_200_OK)
        # Creator: 403 Forbidden
        self.assertEqual(self.client.get("/test/admin-only", headers=c_headers).status_code, status.HTTP_403_FORBIDDEN)
        # Player: 403 Forbidden
        self.assertEqual(self.client.get("/test/admin-only", headers=p_headers).status_code, status.HTTP_403_FORBIDDEN)

        # --- Test 2: Creator & Admin scoring rules endpoint ---
        # Admin: 200 OK
        self.assertEqual(self.client.post("/test/creator-rules", headers=a_headers).status_code, status.HTTP_200_OK)
        # Creator: 200 OK
        self.assertEqual(self.client.post("/test/creator-rules", headers=c_headers).status_code, status.HTTP_200_OK)
        # Player: 403 Forbidden
        self.assertEqual(self.client.post("/test/creator-rules", headers=p_headers).status_code, status.HTTP_403_FORBIDDEN)

        # --- Test 3: Score modification (Players strictly forbidden) ---
        # Admin: 200 OK
        self.assertEqual(self.client.post("/test/modify-scores", headers=a_headers).status_code, status.HTTP_200_OK)
        # Creator: 200 OK
        self.assertEqual(self.client.post("/test/modify-scores", headers=c_headers).status_code, status.HTTP_200_OK)
        # Player: 403 Forbidden
        self.assertEqual(self.client.post("/test/modify-scores", headers=p_headers).status_code, status.HTTP_403_FORBIDDEN)

        # --- Test 4: General authenticated / browse endpoint ---
        # Player: 200 OK
        self.assertEqual(self.client.get("/test/browse-events", headers=p_headers).status_code, status.HTTP_200_OK)
        # Creator: 200 OK
        self.assertEqual(self.client.get("/test/browse-events", headers=c_headers).status_code, status.HTTP_200_OK)
        # Admin: 200 OK
        self.assertEqual(self.client.get("/test/browse-events", headers=a_headers).status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
