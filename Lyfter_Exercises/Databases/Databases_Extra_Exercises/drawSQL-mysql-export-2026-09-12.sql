CREATE TABLE `ShoppingCartProduct`(
    `ShoppingCartProductId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ShoppingCartId` INT UNSIGNED NOT NULL,
    `ProductId` INT UNSIGNED NOT NULL,
    `Quantity` INT NOT NULL
);

CREATE TABLE `ShoppingCart`(
    `ShoppingCartId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `UserId` INT UNSIGNED NOT NULL
);
ALTER TABLE
    `ShoppingCart` ADD INDEX `shoppingcart_userid_index`(`UserId`);
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
    `TotalAmount` DECIMAL(18, 2) NOT NULL,
    `UserId` INT UNSIGNED NOT NULL
);
ALTER TABLE
    `Invoices` ADD UNIQUE `invoices_invoicenumber_unique`(`InvoiceNumber`);
ALTER TABLE
    `Invoices` ADD INDEX `invoices_userid_index`(`UserId`);
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
CREATE TABLE `Users`(
    `UserId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `FullName` VARCHAR(100) NOT NULL,
    `Email` VARCHAR(100) NOT NULL,
    `RegistrationDate` DATETIME NOT NULL
);
ALTER TABLE
    `Users` ADD UNIQUE `users_email_unique`(`Email`);
CREATE TABLE `Reviews`(
    `ReviewId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ProductId` INT UNSIGNED NOT NULL,
    `Comment` TEXT NOT NULL,
    `Rating` TINYINT(1) UNSIGNED NOT NULL,
    `ReviewDate` DATETIME NOT NULL,
    `UserId` INT UNSIGNED NOT NULL
);
ALTER TABLE
    `Reviews` ADD INDEX `reviews_productid_index`(`ProductId`);
ALTER TABLE
    `Reviews` ADD INDEX `reviews_userid_index`(`UserId`);
CREATE TABLE `PaymentMethods`(
    `PaymentMethodId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `MethodTypeId` INT UNSIGNED NOT NULL,
    `BankName` VARCHAR(100) NULL
);
ALTER TABLE
    `PaymentMethods` ADD INDEX `paymentmethods_methodtypeid_index`(`MethodTypeId`);
CREATE TABLE `PaymentMethodTypes`(
    `MethodTypeId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(30) NOT NULL
);
CREATE TABLE `InvoicePaymentMethod`(
    `PaymentId` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `InvoiceId` INT UNSIGNED NOT NULL,
    `PaymentMethodId` INT UNSIGNED NOT NULL,
    `PaidAmount` DECIMAL(18, 2) NOT NULL,
    `PaidAt` DATETIME NOT NULL
);
ALTER TABLE
    `InvoicePaymentMethod` ADD INDEX `invoicepaymentmethod_invoiceid_index`(`InvoiceId`);
ALTER TABLE
    `InvoicePaymentMethod` ADD INDEX `invoicepaymentmethod_paymentmethodid_index`(`PaymentMethodId`);
ALTER TABLE
    `ShoppingCart` ADD CONSTRAINT `shoppingcart_userid_foreign` FOREIGN KEY(`UserId`) REFERENCES `Users`(`UserId`);
ALTER TABLE
    `ProductInvoice` ADD CONSTRAINT `productinvoice_invoiceid_foreign` FOREIGN KEY(`InvoiceId`) REFERENCES `Invoices`(`InvoiceId`);
ALTER TABLE
    `Reviews` ADD CONSTRAINT `reviews_userid_foreign` FOREIGN KEY(`UserId`) REFERENCES `Users`(`UserId`);
ALTER TABLE
    `Invoices` ADD CONSTRAINT `invoices_userid_foreign` FOREIGN KEY(`UserId`) REFERENCES `Users`(`UserId`);
ALTER TABLE
    `InvoicePaymentMethod` ADD CONSTRAINT `invoicepaymentmethod_paymentmethodid_foreign` FOREIGN KEY(`PaymentMethodId`) REFERENCES `PaymentMethods`(`PaymentMethodId`);
ALTER TABLE
    `ShoppingCartProduct` ADD CONSTRAINT `shoppingcartproduct_shoppingcartid_foreign` FOREIGN KEY(`ShoppingCartId`) REFERENCES `ShoppingCart`(`ShoppingCartId`);
ALTER TABLE
    `ShoppingCartProduct` ADD CONSTRAINT `shoppingcartproduct_productid_foreign` FOREIGN KEY(`ProductId`) REFERENCES `Products`(`ProductId`);
ALTER TABLE
    `ProductInvoice` ADD CONSTRAINT `productinvoice_productid_foreign` FOREIGN KEY(`ProductId`) REFERENCES `Products`(`ProductId`);
ALTER TABLE
    `Reviews` ADD CONSTRAINT `reviews_productid_foreign` FOREIGN KEY(`ProductId`) REFERENCES `Products`(`ProductId`);
ALTER TABLE
    `InvoicePaymentMethod` ADD CONSTRAINT `invoicepaymentmethod_invoiceid_foreign` FOREIGN KEY(`InvoiceId`) REFERENCES `Invoices`(`InvoiceId`);
ALTER TABLE
    `PaymentMethods` ADD CONSTRAINT `paymentmethods_methodtypeid_foreign` FOREIGN KEY(`MethodTypeId`) REFERENCES `PaymentMethodTypes`(`MethodTypeId`);