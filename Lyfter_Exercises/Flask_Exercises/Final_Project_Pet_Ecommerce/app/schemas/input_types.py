from pydantic import Field, StringConstraints, EmailStr, AfterValidator

from typing import TypeAlias, Annotated
from decimal import Decimal

# ---------- GLOBAL INPUTS ----------

PhoneNumberInput: TypeAlias = Annotated[str, Field(min_length=1, max_length=20)]
PriceInput: TypeAlias = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
NormalizedEmailInput: TypeAlias = Annotated[EmailStr, AfterValidator(str.lower), Field(max_length=120)]
QuantityInput: TypeAlias = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=3)]
