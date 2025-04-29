from pydantic import BaseModel, EmailStr, validator

class SignupSchema(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None

    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
