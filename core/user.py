class User:
    email: str
    subject: str  # keycloak database id
    session_id: str

    def __init__(self, email: str, subject: str = "", session_id: str = ""):
        self.email = email
        self.subject = subject
        self.session_id = session_id

    def get_user_id(self) -> str:
        return self.email
