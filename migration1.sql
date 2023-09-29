-- create login for user
CREATE LOGIN testUser WITH PASSWORD = 'StrongPassword!123';

-- create user
CREATE USER testUser FOR LOGIN testUser;

-- set permissions
ALTER ROLE db_datareader ADD MEMBER testUser;
ALTER ROLE db_datawriter ADD MEMBER testUser;

-- Create table
CREATE TABLE dbo.country_detail (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Country NVARCHAR(255),
    Iso NVARCHAR(255)
);

-- Insert sample data / Not needed as user can use Frontend UI to fill in data.
-- INSERT INTO dbo.country_detail (Country, Iso) VALUES
-- ('Czech', 'cz'),
-- ('Cesko', 'cz'),
-- ('Tschechien', 'cz'),
-- ('Germany', 'de'),
-- ('Deutschland', 'de'),
-- ('Allemagne', 'de'),
-- ('Spain', 'es'),
-- ('España', 'es'),
-- ('Espagne', 'es'),
-- ('Italy', 'it'),
-- ('Italia', 'it'),
-- ('Italie', 'it'),
-- ('France', 'fr'),
-- ('United Kingdom', 'gb'),
-- ('Verenigd Koninkrijk', 'gb'),
-- ('Royaume-Uni', 'gb');
