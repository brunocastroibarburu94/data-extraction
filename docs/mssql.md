# Setting up a MS SQL Database

Relevant links:
- [Environment Variables](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-configure-environment-variables?view=sql-server-ver16)

```bash
# Pull Image
docker pull mcr.microsoft.com/mssql/server:2022-latest
# Set up server
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Hello#123" -p 1433:1433 --name sql1 --hostname sql1 -d mcr.microsoft.com/mssql/server:2022-latest
# Debug
docker exec -t sql1 cat /var/opt/mssql/log/errorlog | grep connection
docker ps -a

# Prompt to change password 
docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd \
 -S localhost -U SA \
 -P "$(read -sp "Enter current SA password: "; echo "${REPLY}")" \
 -Q "ALTER LOGIN SA WITH PASSWORD=\"$(read -sp "Enter new SA password: "; echo "${REPLY}")\""

# Open console to MS SQL server
docker exec -it sql1 "bash"

# Once inside, connect locally with sqlcmd
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "Hello#123"

```
### Demo SQL Snippets

```sql
CREATE DATABASE TestDB;
SELECT Name from sys.databases;
GO; -- Run commands

-- Create table and insert data
USE TestDB;
CREATE TABLE Inventory (id INT, name NVARCHAR(50), quantity INT);
INSERT INTO Inventory VALUES (1, 'banana', 150); INSERT INTO Inventory VALUES (2, 'orange', 154);
GO;

-- Query
SELECT * FROM Inventory WHERE quantity > 152;
GO;

-- List all tables in the server
SET NOCOUNT ON
DECLARE @AllTables table (CompleteTableName nvarchar(4000))
INSERT INTO @AllTables (CompleteTableName)
    EXEC sp_msforeachdb 'select @@SERVERNAME+''.''+''?''+''.''+s.name+''.''+t.name from [?].sys.tables t inner join sys.schemas s on t.schema_id=s.schema_id'
SET NOCOUNT OFF
SELECT * FROM @AllTables ORDER BY 1;

-- Create schema and put a new table
CREATE SCHEMA test;
CREATE TABLE test.Inventory2 (id INT, name NVARCHAR(50), quantity INT);

```



```sql
SELECT @@SERVERNAME,
    SERVERPROPERTY('ComputerNamePhysicalNetBIOS'),
    SERVERPROPERTY('MachineName'),
    SERVERPROPERTY('ServerName');
```
### [Password Complexity](https://learn.microsoft.com/en-us/sql/relational-databases/security/password-policy?view=sql-server-ver16#password-complexity)
Password complexity policies are designed to deter brute force attacks by increasing the number of possible passwords. When password complexity policy is enforced, new passwords must meet the following guidelines:

- The password doesn't contain the account name of the user.
- The password is at least eight characters long.
- The password contains characters from three of the following four categories:
  - Latin uppercase letters (A through Z)
  - Latin lowercase letters (a through z)
  - Base 10 digits (0 through 9)
  - Non-alphanumeric characters such as: exclamation point (!), dollar sign ($), number sign (#), or percent (%).

Passwords can be up to 128 characters long. Use passwords that are as long and complex as possible.

### Persisting data
[Based on Nocentino post](https://www.nocentino.com/posts/2019-09-01-persisting-sql-server-data-in-docker-containers-part-1/).

When running SQL Server in a container will store data in `/var/opt/mssql` by default. When the container starts up for the first time it will put the system databases in that location and any user databases created will also be placed at this location by default. 
