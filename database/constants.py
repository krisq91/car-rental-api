TABLE_CREATE_QUERY_MAP = ['''CREATE TABLE User (
                  Id INT AUTO_INCREMENT PRIMARY KEY,
                  name VARCHAR(255),
                  phoneNo VARCHAR(20),
                  address TEXT,
                  email VARCHAR(255),
                  idProof LONGBLOB,
                  drivingLicenceNo VARCHAR(20)
                );
            ''', '''CREATE TABLE VehicleCategory 
            ( Id INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(255) NOT NULL,Description TEXT );
            ''', '''CREATE TABLE Vehicle (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                mileage DECIMAL(10, 2),
                name VARCHAR(255),
                vehicleId VARCHAR(255),
                model VARCHAR(255),
                plateNo VARCHAR(20),
                pricePerHour DECIMAL(10, 2),
                isAvailable BOOLEAN,
                pickUpLocation VARCHAR(255),
                vehicleCategoryId INT, FOREIGN KEY (vehicleCategoryId) REFERENCES VehicleCategory(Id) ON DELETE CASCADE,
                userId INT, FOREIGN KEY (userId) REFERENCES User(Id) ON DELETE CASCADE
            );
            ''', '''CREATE TABLE Booking (
                    Id INT AUTO_INCREMENT PRIMARY KEY,
                    bookingStatus VARCHAR(255),
                    amount DECIMAL(10, 2),
                    pickupDateTime DATETIME,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    dropDateTime DATETIME,
                    vehicleId INT,
                    userId INT,
                    FOREIGN KEY (vehicleId) REFERENCES Vehicle(Id) ON DELETE CASCADE,
                    FOREIGN KEY (userId) REFERENCES User(Id) ON DELETE CASCADE
            );
            ''', '''CREATE TABLE PaymentRecord (
                    Id INT AUTO_INCREMENT PRIMARY KEY,
                    paymentMode VARCHAR(255),
                    status VARCHAR(255),
                    paymentTime DATETIME,
                    transactionId VARCHAR(255),
                    bookingId INT,
                    FOREIGN KEY (bookingId) REFERENCES Booking(Id) ON DELETE CASCADE
                );
            ''']

DROP_TABLES = ["PaymentRecord", "Booking", "Vehicle", "User", "VehicleCategory"]

