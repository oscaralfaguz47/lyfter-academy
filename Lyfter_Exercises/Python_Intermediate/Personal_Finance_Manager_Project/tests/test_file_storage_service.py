import pytest
from services.file_storage_service import save_data_to_csv, get_data_from_csv


class FakeRecord:
    FIELD_NAMES = ["id", "name"]

    def __init__(self, record_id, name):
        self.record_id = record_id
        self.name = name

    def to_dict(self):
        return {"id": self.record_id, "name": self.name}

    @classmethod
    def from_dict(cls, row):
        return cls(record_id=row["id"], name=row["name"])


def test_save_creates_file_with_header(tmp_path):
    save_data_to_csv(FakeRecord("1", "Food"), "test.csv", FakeRecord.FIELD_NAMES, data_dir=tmp_path)

    content = (tmp_path / "test.csv").read_text(encoding="utf-8")
    assert content.startswith("id,name")


def test_save_appends_without_overwriting(tmp_path):
    save_data_to_csv(FakeRecord("1", "Food"), "test.csv", FakeRecord.FIELD_NAMES, data_dir=tmp_path)
    save_data_to_csv(FakeRecord("2", "Transport"), "test.csv", FakeRecord.FIELD_NAMES, data_dir=tmp_path)

    lines = (tmp_path / "test.csv").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3


def test_save_writes_header_only_once(tmp_path):
    save_data_to_csv(FakeRecord("1", "Food"), "test.csv", FakeRecord.FIELD_NAMES, data_dir=tmp_path)
    save_data_to_csv(FakeRecord("2", "Transport"), "test.csv", FakeRecord.FIELD_NAMES, data_dir=tmp_path)

    content = (tmp_path / "test.csv").read_text(encoding="utf-8")
    assert content.count("id,name") == 1


def test_get_returns_empty_list_when_file_does_not_exist(tmp_path):
    assert get_data_from_csv("missing.csv", FakeRecord, data_dir=tmp_path) == []


def test_get_returns_saved_records(tmp_path):
    save_data_to_csv(FakeRecord("1", "Food"), "test.csv", FakeRecord.FIELD_NAMES, data_dir=tmp_path)
    save_data_to_csv(FakeRecord("2", "Transport"), "test.csv", FakeRecord.FIELD_NAMES, data_dir=tmp_path)

    records = get_data_from_csv("test.csv", FakeRecord, data_dir=tmp_path)

    assert len(records) == 2
    assert records[0].name == "Food"
    assert records[1].name == "Transport"


def test_get_returns_empty_list_when_file_has_only_header(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("id,name\n", encoding="utf-8")

    assert get_data_from_csv("empty.csv", FakeRecord, data_dir=tmp_path) == []