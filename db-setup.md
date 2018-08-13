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

* Using the makefile suite, and specifying all the incomplete parts of the suite create a makefile in the folder that contains the code.

* Use ````make

