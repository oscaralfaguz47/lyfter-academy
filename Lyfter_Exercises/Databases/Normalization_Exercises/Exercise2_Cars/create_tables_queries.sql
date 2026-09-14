CREATE TABLE Makes(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE Models(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE Colors(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    HexCode TEXT NOT NULL
);

CREATE TABLE Owners(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Phone TEXT NOT NULL
);

CREATE TABLE CompanyInsurances(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    Description NOT NULL
);

CREATE TABLE InsurancePolicies(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE Cars(
    Id INTEGER PRIMARY KEY,
    MakeId INTEGER NOT NULL REFERENCES Makes(Id),
    ModelId INTEGER NOT NULL REFERENCES Models(Id),
    Year TEXT NOT NULL,
    ColorId INTEGER NOT NULL REFERENCES Colors(Id),
    OwnerId INTEGER NOT NULL REFERENCES Owners(Id),
    CompanyInsuranceId INTEGER NOT NULL REFERENCES CompanyInsurances(Id),
    InsurancePolicyId INTEGER NOT NULL REFERENCES InsurancePolicies(Id)
);

-- Create indexes to improve performance
CREATE INDEX IX_Cars_MakeId ON Cars(MakeId);
CREATE INDEX IX_Cars_ModelId ON Cars(ModelId);
CREATE INDEX IX_Cars_ColorId ON Cars(ColorId);
CREATE INDEX IX_Cars_OwnerId ON Cars(OwnerId);
CREATE INDEX IX_Cars_CompanyInsuranceId ON Cars(CompanyInsuranceId);
CREATE INDEX IX_Cars_InsurancePolicyId ON Cars(InsurancePolicyId);