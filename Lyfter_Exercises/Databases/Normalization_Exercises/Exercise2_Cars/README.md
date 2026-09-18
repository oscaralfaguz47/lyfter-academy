## CARS TABLE

**Notes:**
    - Models table: One Make can have multiple models, thats why I separated Makes and Models.
    - There are a lot of different colors, also they can have code like HexCode, that why I created a separate table.
    - CarOwners table: One car can have multiple owners and an owner can have multiple cars.
    - InsuranceCompanies: Each company is registered once.
    - InsurancePolicies: Catalog of policies offered by each company (e.g. Fire & Theft, Full Cover). Each policy is registered only once and can be sold to many customers.
    - CarOwnerPolicies: Assigns a policy to a specific owner of a specific car. This allows the same policy to be applied to many vehicles, and each owner of the same car to have a different policy.
