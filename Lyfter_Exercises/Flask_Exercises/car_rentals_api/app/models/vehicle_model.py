from app.models.brand import Brand

class VehicleModel:
    def __init__(self, name, brand_id, *, model_id=None, brand=None):
        self.name = name
        self.brand_id = brand_id
        self.id = model_id
        self.brand = brand

    @classmethod
    def from_row(cls, row):
        brand = Brand(row["brand_name"], brand_id=row["brand_id"])
        return cls(
            row['name'],
            row["brand_id"],
            model_id=row["id"],
            brand=brand
        )

    def to_dict(self):
        return {
            "id":self.id,
            "name": self.name,
            "brand_id": self.brand.to_dict() if self.brand else self.brand_id
        }