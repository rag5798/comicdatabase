# Overview

I did this project to understand mor eabout interacting with a database outside of MYSQL Workbench, specifically Python.

I made a terminal interface that uses python to connect to the sqlite database. 

I wanted to make this to keep track of my comic collection easier. Eventually I want to make it a website that I can access anywhere.

[Software Demo Video](https://www.youtube.com/watch?v=QNnDwvxN4eI)

# Relational Database

I used SQLite database to hold my data.

I made a user table to hold my username and passsword. A comic table to hold all the comic data. The comic has the series in a differnt table that links to them. I also have a series table that holds the name and foriegn keys linking publisher name and volume number.

# Development Environment

I used VScode as my environment and github to store my data.

I used SQL queries to make the database and python for interacting with the user.

# Useful Websites

- [W3Schools SQL Tutorials](https://www.w3schools.com/mysql/default.asp)
- [SQLite in Python Tutorial](https://codefather.tech/blog/sqlite-database-python/)

# Future Work

- Make a GUI Interface
- Make a Website Interface
- Fix Structure to include things I need in the future
