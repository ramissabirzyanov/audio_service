from pydantic import BaseModel


class Token(BaseModel):
    my_token: str
    token_type: str

class AuthResponse(Token):
    user_id: int
    user_email: str
