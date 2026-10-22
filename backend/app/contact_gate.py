import uuid


def allow_contact(*, is_mutual_match: bool, viewer_id: uuid.UUID | None = None) -> bool:
    """Only place that may reveal another person's WhatsApp.

    A mutual match is required. A later payment or subscription check belongs
    in this function and can use viewer_id. Routers must not reveal a number
    on their own; they hide WhatsApp whenever this returns false.
    """
    if not is_mutual_match:
        return False
    if viewer_id is None:
        return False
    return True


def contact_view(*, is_mutual_match: bool, viewer_id: uuid.UUID | None, whatsapp: str | None) -> dict:
    number = (whatsapp or "").strip()
    if allow_contact(is_mutual_match=is_mutual_match, viewer_id=viewer_id) and number:
        return {"channel": "whatsapp", "available": True, "value": number}
    return {"channel": "whatsapp", "available": False, "value": None}
