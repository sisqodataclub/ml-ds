# Setting Up PostgreSQL on Windows: A Step-by-Step Guide  

PostgreSQL is a powerful, open-source relational database system. In this guide, we will walk through the process of setting up PostgreSQL on a Windows machine, creating a database, and running basic SQL commands.  

## Starting the PostgreSQL Server  

To start the PostgreSQL server, use the `pg_ctl.exe` command. Below is an example:  

```bash  
C:\Windows\System32>"C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" -D "C:\pgdata_test" -l "C:\pgdata_test\logfile.txt" start  
waiting for server to start.... done  
server started  
```  

This command initializes the PostgreSQL server using the specified data directory (`C:\pgdata_test`) and logs output to `logfile.txt`.  

## Accessing PostgreSQL with `psql`  

Once the server is running, you can connect to it using the `psql` command-line tool:  

```bash  
C:\Windows\System32>psql -U postgres  
psql (17.3)  
WARNING: Console code page (850) differs from Windows code page (1252)  
         8-bit characters might not work correctly. See psql reference  
         page "Notes for Windows users" for details.  
Type "help" for help.  
```  

The `-U postgres` flag specifies the username (`postgres` is the default superuser).  

## Changing the Default Password  

For security purposes, it is recommended to change the default password for the `postgres` user:  

```sql  
postgres=# ALTER USER postgres PASSWORD 'password';  
ALTER ROLE  
```  

Replace `'password'` with a strong password of your choice.  

## Creating a New Database  

To create a new database, use the `CREATE DATABASE` command:  

```sql  
postgres=# CREATE DATABASE mydatabase;  
CREATE DATABASE  
```  

You can verify the list of databases using the `\l` command:  

```sql  
postgres=# \l  
```  

This will display a list of all databases, including the newly created `mydatabase`.  

## Querying the Database List  

To query non-template databases, use the following SQL command:  

```sql  
postgres=# SELECT datname  
postgres-# FROM pg_database  
postgres-# WHERE datistemplate = false AND datname <> 'postgres';  
  datname  
------------  
 mydatabase  
(1 row)  
```  

This query filters out template databases and the default `postgres` database, showing only user-created databases.  

## Conclusion  

In this guide, we covered how to start the PostgreSQL server, connect using `psql`, change the default password, create a new database, and query the database list. PostgreSQL is now set up and ready for use on your Windows machine.  

Happy coding!  