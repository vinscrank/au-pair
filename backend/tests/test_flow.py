import unittest
import uuid

from fastapi.testclient import TestClient
from sqlalchemy import delete, or_, select

from app.contact_gate import allow_contact, contact_view
from app.database import SessionLocal
from app.main import app
from app.models import CandidateProfile, FamilyProfile, Match, Swipe, User

CANDIDATE_EMAIL = "flow-candidate@example.com"
FAMILY_EMAIL = "flow-family@example.com"
OTHER_EMAIL = "flow-other@example.com"


def wipe(emails: list[str]) -> None:
    db = SessionLocal()
    try:
        users = db.scalars(select(User).where(User.email.in_(emails))).all()
        ids = [user.id for user in users]
        if not ids:
            return
        db.execute(delete(Swipe).where(or_(Swipe.swiper_id.in_(ids), Swipe.target_id.in_(ids))))
        db.execute(delete(Match).where(or_(Match.user_low_id.in_(ids), Match.user_high_id.in_(ids))))
        db.execute(delete(CandidateProfile).where(CandidateProfile.user_id.in_(ids)))
        db.execute(delete(FamilyProfile).where(FamilyProfile.user_id.in_(ids)))
        db.execute(delete(User).where(User.id.in_(ids)))
        db.commit()
    finally:
        db.close()


def candidate_body() -> dict:
    return {
        "display_name": "Clare Keane",
        "whatsapp": "+353 87 555 0199",
        "photo_url": "/seed/aoife.jpg",
        "age": 29,
        "gender": "woman",
        "nationality": "Irish",
        "based_in": "Portobello, Dublin",
        "languages": [{"language": "English", "level": "native"}],
        "experience_years": 6,
        "experience_age_bands": ["2_5"],
        "experience_summary": "After-school care for two families in Dublin 8.",
        "qualification": "Paediatric first aid",
        "first_aid": True,
        "garda_vetting": True,
        "has_references": True,
        "smoker": False,
        "comfortable_with_pets": True,
        "has_driving_licence": False,
        "has_own_car": False,
        "eu_passport": True,
        "special_needs_experience": False,
        "duties": ["childcare", "homework"],
        "arrangement": "live_out",
        "areas": ["Portobello", "Rathmines"],
        "minds_in": ["family_home"],
        "days_available": ["monday", "tuesday"],
        "hours_per_week": 10,
        "schedule_notes": "After school on Monday and Tuesday, collection at 2.",
        "available_short_notice": False,
        "start_timing": "asap",
        "duration_months": None,
        "pay_basis": "hourly",
        "pay_min": 17,
        "pay_max": None,
        "pay_negotiable": False,
        "bio": "I'm Clare, in Portobello. I mind primary-school children after school and I can share references.",
    }


def family_body(name: str = "Walsh family") -> dict:
    return {
        "display_name": name,
        "whatsapp": "+353 86 555 0188",
        "photo_url": "/seed/brennan.jpg",
        "area": "Ranelagh",
        "children": [{"age_years": 4, "age_months": None}],
        "schedule_notes": "Monday to Thursday after school, collection from Ranelagh and dinner.",
        "days_needed": ["monday", "tuesday", "wednesday", "thursday"],
        "hours_per_week": 16,
        "care_windows": ["afternoons"],
        "start_timing": "asap",
        "duration_months": 6,
        "arrangement": "live_out",
        "duties": ["childcare", "homework", "cooking"],
        "languages_at_home": [{"language": "English", "level": "native"}],
        "household": "two_parents",
        "has_pets": False,
        "pet_notes": "",
        "own_room": False,
        "accommodation_notes": "",
        "pay_basis": "hourly",
        "pay_amount": 18,
        "pay_negotiable": False,
        "bio": "We're a two-parent family in Ranelagh and we need after-school cover four days a week.",
    }


class ContactGateTest(unittest.TestCase):
    def test_mutual_match_is_required(self):
        viewer = uuid.uuid4()
        self.assertFalse(allow_contact(is_mutual_match=False, viewer_id=viewer))
        self.assertFalse(allow_contact(is_mutual_match=True, viewer_id=None))
        self.assertTrue(allow_contact(is_mutual_match=True, viewer_id=viewer))
        hidden = contact_view(is_mutual_match=False, viewer_id=viewer, whatsapp="+353 87 000 0000")
        self.assertFalse(hidden["available"])
        self.assertIsNone(hidden["value"])


class ApiFlowTest(unittest.TestCase):
    def setUp(self):
        wipe([CANDIDATE_EMAIL, FAMILY_EMAIL, OTHER_EMAIL])
        self.client = TestClient(app)

    def tearDown(self):
        wipe([CANDIDATE_EMAIL, FAMILY_EMAIL, OTHER_EMAIL])

    def register(self, email: str, role: str) -> dict:
        response = self.client.post(
            "/api/auth/register",
            json={"email": email, "password": "dublin-demo", "role": role},
        )
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_match_reveals_whatsapp_and_discover_does_not(self):
        self.register(FAMILY_EMAIL, "family")
        saved = self.client.put("/api/profile", json=family_body())
        self.assertTrue(saved.json()["complete"], saved.text)
        family_id = saved.json()["card"]["user_id"]

        self.register(OTHER_EMAIL, "family")
        other = self.client.put("/api/profile", json=family_body("Doyle family"))
        self.assertTrue(other.json()["complete"], other.text)

        self.register(CANDIDATE_EMAIL, "candidate")
        blocked = self.client.get("/api/discover")
        self.assertEqual(blocked.status_code, 403)
        self.assertEqual(blocked.json()["detail"], "profile_incomplete")

        partial = self.client.put("/api/profile", json={"display_name": "Clare"})
        self.assertFalse(partial.json()["complete"])
        self.assertEqual(self.client.get("/api/discover").status_code, 403)

        finished = self.client.put("/api/profile", json=candidate_body())
        self.assertTrue(finished.json()["complete"], finished.text)
        feed = self.client.get("/api/discover")
        self.assertEqual(feed.status_code, 200, feed.text)
        body = feed.text
        self.assertNotIn("whatsapp", body.lower())
        self.assertNotIn("555 0188", body)
        ids = [card["user_id"] for card in feed.json()["cards"]]
        self.assertIn(family_id, ids)

        liked = self.client.post("/api/swipes", json={"target_id": family_id, "direction": "like"})
        self.assertEqual(liked.status_code, 200, liked.text)
        self.assertFalse(liked.json()["matched"])

        self.client.post("/api/auth/login", json={"email": FAMILY_EMAIL, "password": "dublin-demo"})
        family_feed = self.client.get("/api/discover").json()["cards"]
        candidate = next(card for card in family_feed if card["display_name"] == "Clare Keane")
        matched = self.client.post("/api/swipes", json={"target_id": candidate["user_id"], "direction": "like"})
        self.assertTrue(matched.json()["matched"], matched.text)
        self.assertTrue(matched.json()["match"]["contact"]["available"])
        self.assertEqual(matched.json()["match"]["contact"]["value"], "+353 87 555 0199")

        self.client.post("/api/auth/login", json={"email": CANDIDATE_EMAIL, "password": "dublin-demo"})
        matches = self.client.get("/api/matches")
        self.assertEqual(matches.status_code, 200, matches.text)
        contact = matches.json()["matches"][0]["contact"]
        self.assertTrue(contact["available"])
        self.assertEqual(contact["value"], "+353 86 555 0188")
        again = self.client.get("/api/discover").json()["cards"]
        self.assertNotIn(family_id, [card["user_id"] for card in again])

        passed = self.client.post("/api/swipes", json={"target_id": other.json()["card"]["user_id"], "direction": "pass"})
        self.assertFalse(passed.json()["matched"])
        self.assertIsNone(passed.json()["match"])
        after_pass = self.client.get("/api/discover").json()["cards"]
        self.assertNotIn(other.json()["card"]["user_id"], [card["user_id"] for card in after_pass])


if __name__ == "__main__":
    unittest.main()
