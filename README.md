# ------- NewsLog -------

Author: Perla Jarillo

# ABOUT:
NewsLog is an example of an internal reporting tool that uses information from a database to discover what kind of articles posted in a  website are the most popular. It provides information about the top articles and authors, as well as the dates where more than 1% of requests lead to errors.

The tool provide the answers to this questions:

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

Example:

"Princess Shellfish Marries Prince Handsome" — 1201 views
"Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
"Political Scandal Ends In Political Scandal" — 553 views

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

Example:

Ursula La Multa — 2304 views
Rudolf von Treppenwitz — 1985 views
Markoff Chaney — 1723 views
Anonymous Contributor — 1023 views

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

Example:

July 29, 2016 — 2.5% errors

## How does it work?
The program first connect to the database and then a cursor is created and passed as argument to each of the functions that make a query of the views that contain the information required. At the end, the connection to the database is closed.

# DEPENDENCIES AND RESOURCES:

In order to run this program it is important for you to have the next dependencies and resources set in your computer.

## Linux machine.
If you don't want to install Linux in your computer you can install VirtualBox and Vagrant.
  - VirtualBox. Download from https://www.virtualbox.org/wiki/Downloads
    Here are the instalation instructions for Windows: https://www.virtualbox.org/manual/ch02.html#installation_windows
    Or if you have Mac OS X Hosts:https://www.virtualbox.org/manual/ch02.html#installation-mac

  - Vagrant. You can get it from https://www.vagrantup.com/downloads.html

It is recommended for you to create a directory to storage the newslog.py file and database.
Once you have VirtualBox and Vagrant installed, open a terminal and run the commands:


```mkdir newsdata ```

```cd newsdata```

```vagrant init ubuntu/trusty64```

```vagrant up```

```vagrant ssh ```


## Python 2.7 or superior.
As you will be working with a VM you may have already Python installed. But if you don't:

    a. Windows and Mac: Install it from python.org: https://www.python.org/downloads/
    b. Mac (with Homebrew): In the terminal, run brew install python3
    c. Debian/Ubuntu/Mint: In the terminal, run sudo apt-get install python3

## psycopg2 PostgreSQL database adapter.
To install type from your terminal: ``` pip install psycopg2 ```
More information is available on: http://initd.org/psycopg/docs/install.html

## Database
newsdata.sql is the database we will be using in this program, here is the link to download it: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

Unzip the directory and put the newsdata.sql file into the newsdata directory that you created previously.



# HOW TO USE newslog

## Step 1
The first thing you will need is to load the data into your local database. To do that cd into your newsdata directory using the terminal and use the command ``` psql -d news -f newsdata.sql ``` This will populate the database.

Once the database is populated run  ``` psql -d news ``` to connect to the database.

## Step 2
The program relies on 3 different views, before running the program you will need to create them as is described bellow.

a. top_articles: this view contains information about the most popular three articles of all time. To create it run:

CREATE VIEW top_articles AS SELECT a.title, COUNT(*) AS v FROM articles AS a, log WHERE log.path LIKE CONCAT('%',a.slug) GROUP BY a.title ORDER BY v DESC LIMIT 3;

b. top_authors: this view contains information about the most popular authors. To create top_authors run:

CREATE VIEW top_authors AS SELECT authors.name, SUM(articles_view.v) as views FROM authors LEFT JOIN articles ON (authors.id=articles.author) JOIN (SELECT a.title, COUNT(*) AS v FROM articles AS a, log WHERE log.path LIKE CONCAT('%',a.slug) GROUP BY a.title ORDER BY v
) as articles_view on (articles.title=articles_view.title) GROUP BY authors.name ORDER BY views desc;

c. request_errors: this view contains information about the dates when more than 1% of requests lead to errors. To create it run:


CREATE VIEW request_errors AS SELECT to_char(time, 'Mon DD, YYYY') as date, TRUNC((TRUNC(COUNT(*),2)/TRUNC(log_mirror.total_request,2)*100), 2) as pct FROM log, (SELECT to_char(time, 'Mon DD, YYYY') as date_mirror, COUNT(*) as total_request from log group by date_mirror) as log_mirror GROUP BY date, log_mirror.date_mirror, log_mirror.total_request, status HAVING log_mirror.date_mirror = to_char(log.time, 'Mon DD, YYYY') AND status NOT LIKE '200 OK' AND TRUNC((TRUNC(COUNT(*),2)/TRUNC(log_mirror.total_request,2)*100), 2) >= 1.00;

## Step 3.
Once you have created the views, use another terminal to cd into the directory, where you download the files. Run:
```
vagrant ssh
```

and then type:

```
python newslog.py
```

from your terminal.

You will be able to see the information required as follow:

---
vagrant@vagrant:/vagrant/LogAnalysis/newsdata$ python newslog.py

Most popular three articles of all time:

Candidate is jerk, alleges rival - 338647 views
Bears love berries, alleges bear - 253801 views
Bad things gone, say good people - 170098 views

Most popular article authors of all time:

Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views

Days when more than 1% of requests lead to errors:

Jul 17, 2016 - 2.26 errors

---