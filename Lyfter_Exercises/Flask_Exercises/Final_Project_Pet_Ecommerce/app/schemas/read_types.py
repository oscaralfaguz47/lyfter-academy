from pydantic import PlainSerializer

from typing import TypeAlias, Annotated
from decimal import Decimal

# ---------- SERIALIZERS FOR READS ----------

Money: TypeAlias = Annotated[Decimal, PlainSerializer(lambda value: f"{value:.2f}", return_type=str)]
Quantity: TypeAlias = Annotated[Decimal, PlainSerializer(lambda value: f"{value:.3f}", return_type=str)]
