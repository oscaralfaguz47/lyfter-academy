CREATE TABLE `ShoppingCartProduct`(
    `ShoppingCartProductId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ShoppingCartId` INT UNSIGNED NOT NULL,
    `ProductId` INT UNSIGNED NOT NULL,
    `Quantity` INT NOT NULL
);
CREATE TABLE `ShoppingCart`(
    `ShoppingCartId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `BuyerEmail` VARCHAR(100) NOT NULL
);
CREATE TABLE `ProductInvoice`(
    `ProductInvoiceId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ProductId` INT UNSIGNED NOT NULL,
    `InvoiceId` INT UNSIGNED NOT NULL,
    `Quantity` INT NOT NULL,
    `UnitPrice` DECIMAL(8, 2) NOT NULL,
    `TotalAmount` DECIMAL(18, 2) NOT NULL
);
ALTER TABLE
    `ProductInvoice` ADD INDEX `productinvoice_productid_index`(`ProductId`);
ALTER TABLE
    `ProductInvoice` ADD INDEX `productinvoice_invoiceid_index`(`InvoiceId`);
CREATE TABLE `Invoices`(
    `InvoiceId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `InvoiceNumber` VARCHAR(100) NOT NULL,
    `PurchaseDate` DATETIME NOT NULL,
    `BuyerEmail` VARCHAR(100) NOT NULL,
    `TotalAmount` DECIMAL(18, 2) NOT NULL
);
ALTER TABLE
    `Invoices` ADD UNIQUE `invoices_invoicenumber_unique`(`InvoiceNumber`);
CREATE TABLE `Products`(
    `ProductId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Code` VARCHAR(30) NOT NULL,
    `Name` VARCHAR(80) NOT NULL,
    `Price` DECIMAL(8, 2) NOT NULL,
    `EntryDate` DATETIME NOT NULL,
    `Brand` VARCHAR(80) NOT NULL,
    `StockAvailable` INT NOT NULL
);
ALTER TABLE
    `Products` ADD UNIQUE `products_code_unique`(`Code`);
ALTER TABLE
    `ProductInvoice` ADD CONSTRAINT `productinvoice_invoiceid_foreign` FOREIGN KEY(`InvoiceId`) REFERENCES `Invoices`(`InvoiceId`);
ALTER TABLE
    `ShoppingCartProduct` ADD CONSTRAINT `shoppingcartproduct_shoppingcartid_foreign` FOREIGN KEY(`ShoppingCartId`) REFERENCES `ShoppingCart`(`ShoppingCartId`);
ALTER TABLE
    `ShoppingCartProduct` ADD CONSTRAINT `shoppingcartproduct_productid_foreign` FOREIGN KEY(`ProductId`) REFERENCES `Products`(`ProductId`);
ALTER TABLE
    `ProductInvoice` ADD CONSTRAINT `productinvoice_productid_foreign` FOREIGN KEY(`ProductId`) REFERENCES `Products`(`ProductId`);