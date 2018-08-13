# Setting up the Microsoft SQL Server Database with data generated with TPC-H

## Context

These are the steps I followed to set-up MS SQL Server for an undergraduate research project and populated it with data from [TPC-H]((http://www.tpc.org/tpc_documents_current_versions/current_specifications.asp)) which is a standard for Database Benchmarking.

## Connecting to MS SQL Server and creating a database

1. If you have access to a remote desktop with MS SQL Server then all you have to do is download the Remote Desktop App for [Windows](https://www.microsoft.com/en-us/p/microsoft-remote-desktop/9wzdncrfj3ps) or [Mac](https://itunes.apple.com/au/app/microsoft-remote-desktop-8/id715768417?mt=12) and type in the afully-qualified name of the remote desktop, which in my case was **sqlserver.eng.unimelb.edu.au**.

2. Upon being prompted for your username you need to use the fully-qualified username. If you're using your staff account to login it will look like **unimelb\<user-name>** and if you are using your student account to login it should be **student\<user-name>**. You password should be your university/organisational password.

3. Once you have access to the remote desktop start up Microsoft SQL Server Management Studio.

4. To create a new database through the Object Explorer (the window on the left) by right-clicking on Database and then selecting the Database. This should mean that you have successfully created the database (WOOHOOO!) that you need to populate with data

## Generating the data

I don't think the tpc-h complies for macs (at least the makefile did not contain an option to compile for macs) so I decided to use this [github repo](https://github.com/electrum/tpch-dbgen) to generate the data. You can use the version straight off the website and the variation in your mileage should be minimal.

1. Using the makefile suite, and specifying all the incomplete parts of the suite create a makefile in the folder that contains the code.

2. Use `make` to compile the code. This should create the dbgen and qgen executable files.

3. Now use `./dbgen -s 1` to generate 1 GB of data (-s is the scale factor, -s 10 would create 10 gb of data).

4. This should have created 8 .tbl files in the smae directory as dbgen. Moving them to another location using the `mv` command is probably a good idea since the directory with all the code is already really cluttered.


## Moving data from your computer to the remote desktop

To be able to access data from your computer on the remote dektop all you need to do are these 2 short steps:

1. Go to *Remote Desktop* and right click on it. 

2. Click on the *Edit* option and use the *Local Resources* (that is what it is called on a Mac) to make the folder containing all the data available to the remote dektop.


## Create the tables in the DB and importing data.

1. To create the tables in the databse first type in and run the following command in a sql file:

```
USE [<db-name>]
GO
```

This line essentially tells the server to use the database with the name **<db-name>**.

2. Next type in the following commands to create all the required tables:

```
CREATE TABLE NATION  ( N_NATIONKEY  INTEGER NOT NULL,
                            N_NAME       CHAR(25) NOT NULL,
                            N_REGIONKEY  INTEGER NOT NULL,
                            N_COMMENT    VARCHAR(152));

CREATE TABLE REGION  ( R_REGIONKEY  INTEGER NOT NULL,
                            R_NAME       CHAR(25) NOT NULL,
                            R_COMMENT    VARCHAR(152));

CREATE TABLE PART  ( P_PARTKEY     INTEGER NOT NULL,
                          P_NAME        VARCHAR(55) NOT NULL,
                          P_MFGR        CHAR(25) NOT NULL,
                          P_BRAND       CHAR(10) NOT NULL,
                          P_TYPE        VARCHAR(25) NOT NULL,
                          P_SIZE        INTEGER NOT NULL,
                          P_CONTAINER   CHAR(10) NOT NULL,
                          P_RETAILPRICE DECIMAL(15,2) NOT NULL,
                          P_COMMENT     VARCHAR(23) NOT NULL );

CREATE TABLE SUPPLIER ( S_SUPPKEY     INTEGER NOT NULL,
                             S_NAME        CHAR(25) NOT NULL,
                             S_ADDRESS     VARCHAR(40) NOT NULL,
                             S_NATIONKEY   INTEGER NOT NULL,
                             S_PHONE       CHAR(15) NOT NULL,
                             S_ACCTBAL     DECIMAL(15,2) NOT NULL,
                             S_COMMENT     VARCHAR(101) NOT NULL);

CREATE TABLE PARTSUPP ( PS_PARTKEY     INTEGER NOT NULL,
                             PS_SUPPKEY     INTEGER NOT NULL,
                             PS_AVAILQTY    INTEGER NOT NULL,
                             PS_SUPPLYCOST  DECIMAL(15,2)  NOT NULL,
                             PS_COMMENT     VARCHAR(199) NOT NULL );

CREATE TABLE CUSTOMER ( C_CUSTKEY     INTEGER NOT NULL,
                             C_NAME        VARCHAR(25) NOT NULL,
                             C_ADDRESS     VARCHAR(40) NOT NULL,
                             C_NATIONKEY   INTEGER NOT NULL,
                             C_PHONE       CHAR(15) NOT NULL,
                             C_ACCTBAL     DECIMAL(15,2)   NOT NULL,
                             C_MKTSEGMENT  CHAR(10) NOT NULL,
                             C_COMMENT     VARCHAR(117) NOT NULL);

CREATE TABLE ORDERS  ( O_ORDERKEY       INTEGER NOT NULL,
                           O_CUSTKEY        INTEGER NOT NULL,
                           O_ORDERSTATUS    CHAR(1) NOT NULL,
                           O_TOTALPRICE     DECIMAL(15,2) NOT NULL,
                           O_ORDERDATE      DATE NOT NULL,
                           O_ORDERPRIORITY  CHAR(15) NOT NULL,
                           O_CLERK          CHAR(15) NOT NULL,
                           O_SHIPPRIORITY   INTEGER NOT NULL,
                           O_COMMENT        VARCHAR(79) NOT NULL);

CREATE TABLE LINEITEM ( L_ORDERKEY    INTEGER NOT NULL,
                             L_PARTKEY     INTEGER NOT NULL,
                             L_SUPPKEY     INTEGER NOT NULL,
                             L_LINENUMBER  INTEGER NOT NULL,
                             L_QUANTITY    DECIMAL(15,2) NOT NULL,
                             L_EXTENDEDPRICE  DECIMAL(15,2) NOT NULL,
                             L_DISCOUNT    DECIMAL(15,2) NOT NULL,
                             L_TAX         DECIMAL(15,2) NOT NULL,
                             L_RETURNFLAG  CHAR(1) NOT NULL,
                             L_LINESTATUS  CHAR(1) NOT NULL,
                             L_SHIPDATE    DATE NOT NULL,
                             L_COMMITDATE  DATE NOT NULL,
                             L_RECEIPTDATE DATE NOT NULL,
                             L_SHIPINSTRUCT CHAR(25) NOT NULL,
                             L_SHIPMODE     CHAR(10) NOT NULL,
                             L_COMMENT      VARCHAR(44) NOT NULL);

GO
```
This creates all the tables we need to store the data from TPC-H.

3. All that is left to actually import the data and the commands to do that are as follows:

```
BULK INSERT part FROM 'C:\\self-tuning-dbs\code\data\tables\part.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
BULK INSERT customer FROM 'C:\\self-tuning-dbs\code\data\tables\customer.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
BULK INSERT orders FROM 'C:\\self-tuning-dbs\code\data\tables\orders.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
BULK INSERT partsupp FROM 'C:\\self-tuning-dbs\code\data\tables\partsupp.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
BULK INSERT supplier FROM 'C:\\self-tuning-dbs\code\data\tables\supplier.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
BULK INSERT lineitem FROM 'C:\\self-tuning-dbs\code\data\tables\lineitem.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
BULK INSERT nation FROM 'C:\\self-tuning-dbs\code\data\tables\nation.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
BULK INSERT region FROM 'C:\\self-tuning-dbs\code\data\tables\region.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|', ROWTERMINATOR = '0x0a')
```

Aaaaaaaaaaaaaaaaaand we're done (hopefully) getting the database set up for the project.


## Generating Queries

TPC-H's **qgen** program contains 22 query templates and we wanted to have more than 22 queries to test our data on. So I wrote this short python script to generate n instances of each query template to allow us to be able to create multiple instances of queries and add them to a file.

```
import subprocess

def main():
    with open('queries.sql', 'w') as f:
        for i in range(1,11):
            result = subprocess.run(['./qgen', '-r', str(i)], stdout=subprocess.PIPE)
            f.write(result.stdout.decode('utf-8'))

if _name_ == '_main_':
    main()
```
