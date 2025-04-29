from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    user_id: str
    email: EmailStr | None = None
    display_name: str | None = None
    registered: bool = False
