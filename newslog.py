#!/usr/bin/python
# Python 2.7
# Author: Perla Jarillo

import psycopg2

try:
    db = psycopg2.connect(database="news")
except psycopg2.Error as e:
    print("Unable to connect to the database: "+e)


def create_cursor():
    c = db.cursor()
    return c


def three_popular_articles(c):
    c.execute("SELECT * FROM top_articles")
    articles = c.fetchall()
    return articles


def popular_authors(c):
    c.execute(
        "SELECT * FROM top_authors")
    authors = c.fetchall()
    return authors


def error(c):
    c.execute("SELECT * FROM request_errors")
    errors = c.fetchall()
    return errors


c = create_cursor()
print("\nMost popular three articles of all time:\n")
articles = three_popular_articles(c)
for a in articles:
    print(a[0] + ' - ' + str(a[1]) + " views")


print("\nMost popular article authors of all time:\n")
authors = popular_authors(c)
for auth in authors:
    print(auth[0] + ' - ' + str(auth[1]) + " views")

print("\nDays when more than 1% of requests lead to errors:\n")
errors = error(c)
for e in errors:
    print(e[0] + ' - ' + str(e[1]) + " errors")

db.close()
