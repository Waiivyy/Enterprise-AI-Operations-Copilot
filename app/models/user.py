from pydantic import BaseModel, Field, field_validator


class UserProfile(BaseModel):
    display_name: str = Field(..., min_length=2)
    email: str
    department: str = "General"
    region: str = "Global"
    employment_type: str = "full-time"
    manager: str | None = None
    start_date: str | None = None
    end_date: str | None = None

    @field_validator("email")
    @classmethod
    def email_must_use_example_invalid(cls, value: str) -> str:
        if not value.endswith("@example.invalid"):
            raise ValueError("demo users must use example.invalid emails")
        return value

    @property
    def department_key(self) -> str:
        return self.department.strip().lower().replace(" ", "_")

    @property
    def region_key(self) -> str:
        return self.region.strip().lower().replace(" ", "_")
