from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, or_, select

from app.database import SessionLocal
from app.models import CandidateProfile, FamilyProfile, Match, Swipe, User
from app.profiles import apply_profile, missing_for
from app.schemas import CandidateIn, FamilyIn
from app.security import hash_password

DEMO_PASSWORD = "dublin-demo"


def person(email: str, role: str, profile: dict, hours_ago: int) -> dict:
    return {
        "email": email,
        "role": role,
        "profile": profile,
        "updated_at": datetime(2026, 10, 1, tzinfo=timezone.utc) + timedelta(hours=hours_ago),
    }


PEOPLE = [
    person(
        "sofia.rossi@demo.aupair.ie",
        "candidate",
        {
            "display_name": "Sofia Rossi",
            "whatsapp": "+353 87 555 0148",
            "photo_url": "/seed/sofia.jpg",
            "age": 23,
            "gender": "woman",
            "nationality": "Italian",
            "based_in": "Bologna, can be in Dublin within a week",
            "languages": [
                {"language": "Italian", "level": "native"},
                {"language": "English", "level": "fluent"},
                {"language": "Spanish", "level": "intermediate"},
            ],
            "experience_years": 4,
            "experience_age_bands": ["2_5", "5_plus"],
            "experience_summary": "I have looked after cousins in Bologna since I was 16, and I spent a summer with a family of two in Dublin 6.",
            "qualification": "Paediatric first aid course, Italy",
            "first_aid": True,
            "garda_vetting": False,
            "has_references": True,
            "smoker": False,
            "comfortable_with_pets": True,
            "has_driving_licence": True,
            "has_own_car": False,
            "eu_passport": True,
            "special_needs_experience": False,
            "duties": ["childcare", "school_runs", "cooking", "bedtime", "light_housework"],
            "arrangement": "live_in",
            "areas": ["Rathmines", "Ranelagh", "Rathgar", "Portobello"],
            "minds_in": ["family_home"],
            "days_available": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "hours_per_week": 30,
            "schedule_notes": "Weekday mornings and afternoons. I can do the school run and be home for bedtime. I would like two evenings free for an English class.",
            "available_short_notice": False,
            "start_timing": "asap",
            "duration_months": 10,
            "pay_basis": "weekly",
            "pay_min": 170,
            "pay_max": 200,
            "pay_negotiable": False,
            "bio": "I'm Sofia, 23, from Bologna. I have looked after children since I was 16, mostly toddlers and primary-school age, including a summer with a family in Dublin 6. I like calm routines, time in the park, and cooking a simple dinner. I'm looking for a live-in family around Rathmines or Rathgar, about 30 hours a week, and I want to keep going with my English. Non-smoker, EU driving licence, and references from my last family.",
        },
        1,
    ),
    person(
        "aoife.nolan@demo.aupair.ie",
        "candidate",
        {
            "display_name": "Aoife Nolan",
            "whatsapp": "+353 86 555 0194",
            "photo_url": "/seed/aoife.jpg",
            "age": 31,
            "gender": "woman",
            "nationality": "Irish",
            "based_in": "Drumcondra, Dublin",
            "languages": [
                {"language": "English", "level": "native"},
                {"language": "Irish", "level": "intermediate"},
            ],
            "experience_years": 12,
            "experience_age_bands": ["newborn", "0_6_months", "6_months_2", "2_5", "5_plus"],
            "experience_summary": "Twelve years in creches and with families, from newborns through primary school. I follow the routine you already have.",
            "qualification": "QQI Level 6 Early Childhood Care and Education",
            "first_aid": True,
            "garda_vetting": True,
            "has_references": True,
            "smoker": False,
            "comfortable_with_pets": True,
            "has_driving_licence": True,
            "has_own_car": True,
            "eu_passport": True,
            "special_needs_experience": True,
            "duties": ["childcare", "bedtime", "evening_babysitting", "homework", "cooking"],
            "arrangement": "live_out",
            "areas": ["Drumcondra", "Glasnevin", "Phibsborough", "Clontarf", "Dublin 9"],
            "minds_in": ["family_home"],
            "days_available": ["tuesday", "wednesday", "thursday", "saturday"],
            "hours_per_week": 12,
            "schedule_notes": "Evenings after 6 and Saturday daytime. I work in a creche on Monday and Friday, so I am not free then.",
            "available_short_notice": True,
            "start_timing": "few_weeks",
            "duration_months": None,
            "pay_basis": "hourly",
            "pay_min": 18,
            "pay_max": 20,
            "pay_negotiable": False,
            "bio": "I'm Aoife, based in Drumcondra. I have 12 years in childcare, from newborns up, and I hold a QQI Level 6 in Early Childhood Care and Education. I'm Garda vetted, paediatric first aid trained, and I have a full licence and a car. I'm free for evening babysitting and Saturdays on the northside. I follow the family's routine and I'm happy to send an update when you get home.",
        },
        2,
    ),
    person(
        "mateusz.kowal@demo.aupair.ie",
        "candidate",
        {
            "display_name": "Mateusz Kowal",
            "whatsapp": "+353 85 555 0177",
            "photo_url": "/seed/mateusz.jpg",
            "age": 27,
            "gender": "man",
            "nationality": "Polish",
            "based_in": "Castleknock, Dublin",
            "languages": [
                {"language": "Polish", "level": "native"},
                {"language": "English", "level": "fluent"},
            ],
            "experience_years": 5,
            "experience_age_bands": ["2_5", "5_plus", "teenagers"],
            "experience_summary": "Five years with primary-school children, including school runs, homework and weekend sports.",
            "qualification": "Sports coaching certificate",
            "first_aid": True,
            "garda_vetting": False,
            "has_references": True,
            "smoker": False,
            "comfortable_with_pets": True,
            "has_driving_licence": True,
            "has_own_car": True,
            "eu_passport": True,
            "special_needs_experience": False,
            "duties": ["childcare", "school_runs", "homework", "evening_babysitting", "pet_care"],
            "arrangement": "either",
            "areas": ["Dublin 15", "Blanchardstown", "Castleknock", "Ashtown"],
            "minds_in": ["family_home"],
            "days_available": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "hours_per_week": 25,
            "schedule_notes": "I can do school runs in the car and stay through homework. Weekends off, unless we agree a Saturday in advance.",
            "available_short_notice": False,
            "start_timing": "asap",
            "duration_months": 12,
            "pay_basis": "weekly",
            "pay_min": 200,
            "pay_max": None,
            "pay_negotiable": True,
            "bio": "I'm Mateusz, 27, from Krakow, living near Castleknock. I have five years of experience with primary-school children, including school runs and homework. I have a full EU licence and a car, which helps around Dublin 15. I'm easy-going, sporty, and fine with a family dog. I can live in or live out, weekdays only, and I can start as soon as you need someone.",
        },
        3,
    ),
    person(
        "ines.moreau@demo.aupair.ie",
        "candidate",
        {
            "display_name": "Inès Moreau",
            "whatsapp": "+353 87 555 0162",
            "photo_url": "/seed/ines.jpg",
            "age": 22,
            "gender": "woman",
            "nationality": "French",
            "based_in": "Lyon, ready to move",
            "languages": [
                {"language": "French", "level": "native"},
                {"language": "English", "level": "intermediate"},
                {"language": "Spanish", "level": "basic"},
            ],
            "experience_years": 2,
            "experience_age_bands": ["6_months_2", "2_5"],
            "experience_summary": "Two summers as a nanny for a toddler, plus regular evenings with my younger cousins.",
            "qualification": "",
            "first_aid": False,
            "garda_vetting": False,
            "has_references": True,
            "smoker": False,
            "comfortable_with_pets": False,
            "has_driving_licence": False,
            "has_own_car": False,
            "eu_passport": True,
            "special_needs_experience": False,
            "duties": ["childcare", "light_housework", "laundry", "cooking", "bedtime"],
            "arrangement": "live_in",
            "areas": ["Blackrock", "Dun Laoghaire", "Dalkey", "Booterstown", "Sandycove"],
            "minds_in": ["family_home"],
            "days_available": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "hours_per_week": 28,
            "schedule_notes": "Happy to help with breakfast, the creche drop-off and the afternoon. I would like Sunday and one weekday evening free.",
            "available_short_notice": False,
            "start_timing": "few_weeks",
            "duration_months": 9,
            "pay_basis": "weekly",
            "pay_min": 160,
            "pay_max": None,
            "pay_negotiable": True,
            "bio": "I'm Inès, 22, from Lyon. I have two years of experience with babies and toddlers, mostly as a summer nanny and with my younger cousins. My English is intermediate and getting better. I'm looking for a live-in family on the south coast, Blackrock to Dalkey, and I can help with meals, laundry and bedtime. I'm a non-smoker, I don't drive, and I'm glad to share references.",
        },
        4,
    ),
    person(
        "niamh.brennan@demo.aupair.ie",
        "family",
        {
            "display_name": "Brennan family",
            "whatsapp": "+353 87 555 0114",
            "photo_url": "/seed/brennan.jpg",
            "area": "Rathgar",
            "children": [
                {"age_years": 3, "age_months": None},
                {"age_years": 6, "age_months": None},
            ],
            "schedule_notes": "Monday to Friday. Breakfast from 7:15, school run to a primary school in Rathgar, pickup around 2, then play and dinner. We are usually home by 6.",
            "days_needed": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "hours_per_week": 30,
            "care_windows": ["mornings", "school_hours", "afternoons"],
            "start_timing": "asap",
            "duration_months": 12,
            "arrangement": "live_in",
            "duties": ["childcare", "school_runs", "light_housework", "cooking", "bedtime"],
            "languages_at_home": [{"language": "English", "level": "native"}],
            "household": "two_parents",
            "has_pets": True,
            "pet_notes": "A quiet Labrador who is used to children.",
            "own_room": True,
            "accommodation_notes": "Own double room at the back of the house, with a desk, and a bathroom shared with the children. About ten minutes on foot to Rathmines.",
            "pay_basis": "weekly",
            "pay_amount": 180,
            "pay_negotiable": False,
            "bio": "We're Niamh and Cillian in Rathgar, with a 3-year-old and a 6-year-old. We need a live-in au pair on weekdays, around 30 hours: breakfast, the school run, pickup and dinner. There is a private room at the back of the house. We speak English at home and we're happy to support an English course. Pocket money is €180 a week plus full board.",
        },
        5,
    ),
    person(
        "ada.okonkwo@demo.aupair.ie",
        "family",
        {
            "display_name": "Okonkwo family",
            "whatsapp": "+353 86 555 0128",
            "photo_url": "/seed/okonkwo.jpg",
            "area": "Blanchardstown",
            "children": [
                {"age_years": 2, "age_months": None},
                {"age_years": 8, "age_months": None},
                {"age_years": 11, "age_months": None},
            ],
            "schedule_notes": "Monday to Friday, about 28 hours. Mornings are the busy part: lunchboxes, the younger child to creche, the older two to the school bus. Light tidy-up of the kitchen and playroom. No weekends.",
            "days_needed": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "hours_per_week": 28,
            "care_windows": ["mornings", "school_hours"],
            "start_timing": "few_weeks",
            "duration_months": 12,
            "arrangement": "live_in",
            "duties": ["childcare", "cooking", "light_housework", "laundry", "homework"],
            "languages_at_home": [{"language": "English", "level": "native"}],
            "household": "two_parents",
            "has_pets": False,
            "pet_notes": "",
            "own_room": True,
            "accommodation_notes": "Own room and bathroom on the first floor. Blanchardstown shopping centre and the train are a short walk, and the bus into town is nearby.",
            "pay_basis": "weekly",
            "pay_amount": 230,
            "pay_negotiable": False,
            "bio": "We're Ada and Chidi in Blanchardstown. Our children are 2, 8 and 11. Both of us work in healthcare, so weekday mornings are the crunch: lunchboxes, creche and the school bus. We want a live-in au pair for about 28 hours, Monday to Friday, with light housework only. You would have your own room and bathroom. We speak English at home. Pocket money is €230 a week plus board, and we can start within a few weeks.",
        },
        6,
    ),
    person(
        "orla.byrne@demo.aupair.ie",
        "family",
        {
            "display_name": "Byrne family",
            "whatsapp": "+353 85 555 0133",
            "photo_url": "/seed/byrne.jpg",
            "area": "Clontarf",
            "children": [{"age_years": 1, "age_months": 2}],
            "schedule_notes": "Two evenings a week, usually Tuesday and Thursday, 6pm to 9:30pm, and the occasional Saturday afternoon. This is babysitting, not a live-in post.",
            "days_needed": ["tuesday", "thursday", "saturday"],
            "hours_per_week": 8,
            "care_windows": ["evenings", "weekends"],
            "start_timing": "exploring",
            "duration_months": None,
            "arrangement": "live_out",
            "duties": ["childcare", "bedtime"],
            "languages_at_home": [{"language": "English", "level": "native"}],
            "household": "two_parents",
            "has_pets": False,
            "pet_notes": "",
            "own_room": False,
            "accommodation_notes": "",
            "pay_basis": "hourly",
            "pay_amount": 18,
            "pay_negotiable": False,
            "bio": "We're Orla and Mark in Clontarf. Our son is 14 months. We are not looking for a live-in au pair. We want a reliable babysitter two evenings a week and the odd Saturday, someone comfortable with a toddler bedtime. We pay €18 an hour. References and first aid would be a plus. We're just exploring options and would like to meet the right person before we commit to set nights.",
        },
        7,
    ),
    person(
        "ciara.murphy@demo.aupair.ie",
        "family",
        {
            "display_name": "Murphy family",
            "whatsapp": "+353 87 555 0140",
            "photo_url": "/seed/murphy.jpg",
            "area": "Blackrock",
            "children": [
                {"age_years": 4, "age_months": None},
                {"age_years": 9, "age_months": None},
            ],
            "schedule_notes": "After school Monday to Thursday, 2pm to 6:30pm. Homework, activities around Blackrock, and a simple dinner. Live-in or live-out both work.",
            "days_needed": ["monday", "tuesday", "wednesday", "thursday"],
            "hours_per_week": 18,
            "care_windows": ["afternoons", "school_hours"],
            "start_timing": "asap",
            "duration_months": 10,
            "arrangement": "either",
            "duties": ["childcare", "school_runs", "homework", "cooking", "light_housework"],
            "languages_at_home": [{"language": "English", "level": "native"}],
            "household": "two_parents",
            "has_pets": True,
            "pet_notes": "A small cat.",
            "own_room": True,
            "accommodation_notes": "If you live in, there is a single room with a garden view. Live-out is also fine if you can reach Blackrock for 2pm.",
            "pay_basis": "weekly",
            "pay_amount": 200,
            "pay_negotiable": True,
            "bio": "We're Ciara and Paul in Blackrock, with a 4-year-old and a 9-year-old. We need after-school cover Monday to Thursday: homework, a lift to activities, and dinner. Live-in or live-out both work. Live-in comes with a single room and €200 a week plus board. If you live out, we can agree the same hours at an hourly rate. We have a small cat. We would like to start as soon as possible.",
        },
        8,
    ),
]


def reset_demo(db) -> None:
    emails = [item["email"] for item in PEOPLE]
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


def load_demo(db) -> None:
    for item in PEOPLE:
        user = User(
            email=item["email"],
            password_hash=hash_password(DEMO_PASSWORD),
            role=item["role"],
        )
        db.add(user)
        db.flush()
        if item["role"] == "candidate":
            row = CandidateProfile(user_id=user.id)
            data = CandidateIn.model_validate(item["profile"])
        else:
            row = FamilyProfile(user_id=user.id)
            data = FamilyIn.model_validate(item["profile"])
        apply_profile(user, row, data)
        if not row.is_complete:
            raise RuntimeError(f"{item['email']} is incomplete: {missing_for(user, row)}")
        row.updated_at = item["updated_at"]
        db.add(row)
    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        reset_demo(db)
        load_demo(db)
    finally:
        db.close()
    print(f"Seeded {len(PEOPLE)} Dublin demo profiles. Password: {DEMO_PASSWORD}")


if __name__ == "__main__":
    main()
