CREATE TABLE Makes(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE Models(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    MakeId INTEGER NOT NULL REFERENCES Makes(Id),
    UNIQUE(MakeId, Name)
);

CREATE TABLE Colors(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    HexCode TEXT NULL
);

CREATE TABLE Owners(
    Id INTEGER PRIMARY KEY,
    FullName TEXT NOT NULL,
    Phone TEXT NOT NULL
);

CREATE TABLE CompanyInsurances(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    Description TEXT
);

CREATE TABLE Cars(
    Id INTEGER PRIMARY KEY,
    VIN TEXT NOT NULL UNIQUE,
    ModelId INTEGER NOT NULL REFERENCES Models(Id),
    Year INTEGER NOT NULL,
    ColorId INTEGER NOT NULL REFERENCES Colors(Id)
);

CREATE TABLE CarOwners(
    Id INTEGER PRIMARY KEY,
    CarId INTEGER NOT NULL REFERENCES Cars(Id),
    OwnerId INTEGER NOT NULL REFERENCES Owners(Id),
    UNIQUE(CarId, OwnerId)
);

CREATE TABLE InsurancePolicies(
    Id INTEGER PRIMARY KEY,
    CarOwnerId INTEGER NOT NULL REFERENCES CarOwners(Id),
    InsuranceCompanyId INTEGER NOT NULL REFERENCES CompanyInsurances(Id),
    PolicyType TEXT NOT NULL,
    UNIQUE(CarOwnerId, InsuranceCompanyId, PolicyType)
);


-- Create indexes to improve performance
CREATE INDEX IX_Models_MakeId ON Models(MakeId);
CREATE INDEX IX_Cars_ModelId ON Cars(ModelId);
CREATE INDEX IX_Cars_ColorId ON Cars(ColorId);
CREATE INDEX IX_CarOwners_CarId ON CarOwners(CarId);
CREATE INDEX IX_CarOwners_OwnerId ON CarOwners(OwnerId);
CREATE INDEX IX_InsurancePolicies_InsuranceCompanyId ON InsurancePolicies(InsuranceCompanyId);
CREATE INDEX IX_InsurancePolicies_CarOwnerId ON InsurancePolicies(CarOwnerId);