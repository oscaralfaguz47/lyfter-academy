from pydantic import PlainSerializer

from typing import TypeAlias, Annotated
from decimal import Decimal

# Serializers for reads

Money: TypeAlias = Annotated[Decimal, PlainSerializer(lambda value: f"{value:.2f}", return_type=str)]
Quantity: TypeAlias = Annotated[Decimal, PlainSerializer(lambda value: f"{value:.3f}", return_type=str)]

