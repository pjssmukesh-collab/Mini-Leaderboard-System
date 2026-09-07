# tests/test_database.py
# ──────────────────────────────────────────────
# Database and Models Verification Suite
# ──────────────────────────────────────────────

import unittest
from datetime import datetime, timezone
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app.database.database import Base, engine, SessionLocal, init_db, drop_db
from app.models import (
    User,
    Event,
    EventRule,
    Participant,
    ResultUpload,
    RawResult,
    PlayerResult,
    PlayerScore,
    Ranking,
    UploadLog,
)


class TestDatabaseSetup(unittest.TestCase):
    """Test suite for SQLite database setup and all 10 SQLAlchemy models."""

    def setUp(self):
        """Prepare fresh tables and a session before each test."""
        drop_db()
        init_db()
        self.db = SessionLocal()

    def tearDown(self):
        """Clean up session and drop tables after each test."""
        self.db.rollback()
        self.db.close()
        drop_db()

    def test_01_all_tables_created(self):
        """Verify all 10 model tables exist in SQLite schema."""
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())

        expected_tables = {
            "users",
            "events",
            "event_rules",
            "participants",
            "result_uploads",
            "raw_results",
            "player_results",
            "player_scores",
            "rankings",
            "upload_logs",
        }

        self.assertTrue(
            expected_tables.issubset(table_names),
            f"Missing tables: {expected_tables - table_names}",
        )

    def test_02_user_model_and_constraints(self):
        """Verify User model creation, indexing, and email uniqueness constraint."""
        user = User(
            name="Alice Admin",
            email="alice@example.com",
            password_hash="pbkdf2:sha256:hashed_string",
            role="admin",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        self.assertIsNotNone(user.id)
        self.assertEqual(user.name, "Alice Admin")
        self.assertEqual(user.role, "admin")
        self.assertIsNotNone(user.created_at)

        # Duplicate email test
        duplicate_user = User(
            name="Alice Copy",
            email="alice@example.com",
            password_hash="different_hash",
            role="player",
        )
        self.db.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            self.db.commit()
        self.db.rollback()

    def test_03_full_event_ecosystem_and_relationships(self):
        """
        Verify end-to-end entity creation across all 10 models with:
        - Foreign keys
        - Bidirectional relationships
        - JSON storage for raw data and player metrics
        - Scores and rankings
        - Audit upload logs
        """
        # 1. Create Organizer and Player Users
        organizer = User(
            name="Tournament Host",
            email="host@tourney.com",
            password_hash="hash1",
            role="creator",
        )
        player = User(
            name="Pro Gamer",
            email="player@tourney.com",
            password_hash="hash2",
            role="player",
        )
        self.db.add_all([organizer, player])
        self.db.commit()

        # 2. Create Event
        event = Event(
            creator_id=organizer.id,
            name="Free Fire Battle Royale Cup",
            event_type="free_fire",
            description="Battle royale match with custom kill and placement point rules",
            participant_limit=100,
            status="active",
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        self.assertEqual(event.creator.name, "Tournament Host")
        self.assertEqual(len(organizer.created_events), 1)

        # 3. Create EventRules
        rule_kill = EventRule(
            event_id=event.id,
            metric="kills",
            condition="Each kill awards 2 points",
            operator=">=",
            value=1.0,
            points=2.0,
            priority=1,
        )
        rule_placement = EventRule(
            event_id=event.id,
            metric="placement",
            condition="1st place awards 15 points",
            operator="==",
            value=1.0,
            points=15.0,
            priority=2,
        )
        self.db.add_all([rule_kill, rule_placement])
        self.db.commit()

        self.assertEqual(len(event.rules), 2)

        # 4. Create Participant
        participant = Participant(
            event_id=event.id,
            user_id=player.id,
            external_player_id="FF_CHAMP_99",
            status="confirmed",
        )
        self.db.add(participant)
        self.db.commit()
        self.db.refresh(participant)

        self.assertEqual(participant.event.name, event.name)
        self.assertEqual(participant.user.email, player.email)
        self.assertEqual(len(player.participations), 1)

        # 5. Create ResultUpload
        upload = ResultUpload(
            event_id=event.id,
            uploaded_by=organizer.id,
            filename="match_day_1_results.csv",
            file_type="csv",
            status="completed",
        )
        self.db.add(upload)
        self.db.commit()
        self.db.refresh(upload)

        self.assertEqual(upload.uploader.name, organizer.name)
        self.assertEqual(len(organizer.uploads), 1)

        # 6. Create UploadLog
        log = UploadLog(
            upload_id=upload.id,
            action="PARSE_COMPLETED",
            message="Parsed 25 rows successfully without validation errors.",
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        self.assertEqual(len(upload.logs), 1)
        self.assertEqual(upload.logs[0].action, "PARSE_COMPLETED")

        # 7. Create RawResult with JSON data
        raw_result = RawResult(
            upload_id=upload.id,
            event_id=event.id,
            raw_data={
                "row_num": 1,
                "player_tag": "FF_CHAMP_99",
                "kills": 7,
                "placement": 1,
                "headshots": 4,
                "damage": 2100,
            },
        )
        self.db.add(raw_result)
        self.db.commit()
        self.db.refresh(raw_result)

        self.assertEqual(raw_result.raw_data["kills"], 7)
        self.assertEqual(raw_result.raw_data["headshots"], 4)
        self.assertEqual(len(upload.raw_results), 1)

        # 8. Create PlayerResult with flexible JSON metrics
        player_result = PlayerResult(
            event_id=event.id,
            participant_id=participant.id,
            match_id="round_1",
            metrics={
                "kills": 7,
                "placement": 1,
                "damage": 2100,
                "survival_time_sec": 840,
            },
            validation_status="valid",
        )
        self.db.add(player_result)
        self.db.commit()
        self.db.refresh(player_result)

        self.assertEqual(player_result.metrics["survival_time_sec"], 840)
        self.assertEqual(len(participant.player_results), 1)
        self.assertEqual(len(event.player_results), 1)

        # 9. Create PlayerScore
        total_score = 7 * 2.0 + 15.0  # 29 points
        player_score = PlayerScore(
            event_id=event.id,
            participant_id=participant.id,
            score=total_score,
        )
        self.db.add(player_score)
        self.db.commit()
        self.db.refresh(player_score)

        self.assertEqual(participant.player_score.score, 29.0)
        self.assertEqual(len(event.player_scores), 1)

        # 10. Create Ranking
        ranking = Ranking(
            event_id=event.id,
            participant_id=participant.id,
            rank=1,
            score=total_score,
        )
        self.db.add(ranking)
        self.db.commit()
        self.db.refresh(ranking)

        self.assertEqual(participant.ranking.rank, 1)
        self.assertEqual(participant.ranking.score, 29.0)
        self.assertEqual(len(event.rankings), 1)

    def test_04_cascade_deletion(self):
        """Verify cascade deletion deletes child records when parent Event is removed."""
        user = User(name="Host", email="host_cascade@example.com", password_hash="pw", role="creator")
        self.db.add(user)
        self.db.commit()

        event = Event(creator_id=user.id, name="Cascade Test Event", event_type="chess", status="active")
        self.db.add(event)
        self.db.commit()

        rule = EventRule(event_id=event.id, metric="win", condition="Win", operator="==", value=1.0, points=3.0)
        participant = Participant(event_id=event.id, external_player_id="player_c1")
        self.db.add_all([rule, participant])
        self.db.commit()

        self.assertEqual(self.db.query(EventRule).filter_by(event_id=event.id).count(), 1)
        self.assertEqual(self.db.query(Participant).filter_by(event_id=event.id).count(), 1)

        # Delete parent event
        self.db.delete(event)
        self.db.commit()

        # Child records must be deleted
        self.assertEqual(self.db.query(EventRule).filter_by(event_id=event.id).count(), 0)
        self.assertEqual(self.db.query(Participant).filter_by(event_id=event.id).count(), 0)


if __name__ == "__main__":
    unittest.main()
