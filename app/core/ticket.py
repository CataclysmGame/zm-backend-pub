from app.settings import settings


def generate_ticket() -> str:
    """
    Generates an alphanumeric game ticket.
    Length of the ticket is specified in the server settings.
    The ticket is generated using a secure RNG.
    """
    import secrets
    return secrets.token_urlsafe(settings.GAME_TICKET_LEN)
