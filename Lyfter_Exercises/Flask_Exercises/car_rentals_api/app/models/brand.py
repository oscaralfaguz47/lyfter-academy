

class Brand:
    def __init__(self, name, *, brand_id=None):
        self.name = name
        self.id = brand_id

    @classmethod
    def from_row(cls, row):
        return cls(
            row["name"],
            brand_id=row["id"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }