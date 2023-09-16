from pydantic import BaseModel, Field, ValidationError, validator
import re


class Tags(BaseModel):
    """
    pydantic model for medical form
    """
    medicare_id: str | None = Field(description="Medicare Number")
    full_name: str | None = Field(description="(Last Name, First Name, Middle Name")
    mail_address: str | None = Field(description="Mailing Address (Number and Street, P.O. Box, or Route)")
    city: str | None = Field(description="city")
    state: str | None = Field(description="state: 2 characters")
    zipcode: str | None = Field(description="5-digits code")
    phone_number: str | None = Field(description="10 digits phone number")

    @validator("zipcode")
    def ensure_length(cls, v):
        if not re.match("\d{5}$", v):
            raise ValueError("must be 5 digits")
        return v

    @validator("phone_number")
    def ensure_format(cls, v):
        """
        https://stackabuse.com/python-regular-expressions-validate-phone-numbers/
        :param v:
        :return:
        """
        if not re.match(r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$', v):
            raise ValueError("must be 10 digits")
        return v
