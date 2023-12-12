from flask import Flask, render_template
from neo4j import GraphDatabase

URI = "neo4j+s://24b0e9a6.databases.neo4j.io"
AUTH = ("neo4j", "L04tzXcUCk17ek-6YtE0BheidkaSIXV0G_YqrSArtXA")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

app = Flask(__name__)

@app.route("/")
def hello_world():  
  return render_template('Default.html')

@app.route("/customers")
def customers():
  records, summary, keys = driver.execute_query(
    "MATCH (a:Customer) RETURN a.name AS name, a.age AS age, a.email AS email",
    database_="neo4j",
  )
  info = "The query `{query}` returned {records_count} records.".format(
    query=summary.query, records_count=len(records),
  ) 
  return render_template('Customers.html', info=info, records=records)

@app.route("/tickets")
def tickets():
  records, summary, keys = driver.execute_query(
    "MATCH (a:Ticket) RETURN a.title AS title, a.price AS price, a.availability AS availability, a.shippability AS shippability",
    database_="neo4j",
  )
  info = "The query `{query}` returned {records_count} records.".format(
    query=summary.query, records_count=len(records),
  ) 
  return render_template('Tickets.html', info=info, records=records)

@app.route("/concerts")
def concerts():
  records, summary, keys = driver.execute_query(
    """
      MATCH (a:Ticket)
        -[:IS_IN]->(:Category {title: 'Concert Tickets'}) 
      RETURN 
        a.title AS title, 
        a.price AS price, 
        a.availability AS availability, 
        a.shippability AS shippability;
    """,
    database_="neo4j",
  )
  info = "The query `{query}` returned {records_count} records.".format(
    query=summary.query, records_count=len(records),
  ) 
  return render_template('Tickets.html', info=info, records=records)

@app.route("/wishlists")
def wishlists():
  records, summary, keys = driver.execute_query(
    """
      MATCH (customer:Customer)-[:ADDED_TO_WISH_LIST]->(ticket:Ticket)
      RETURN customer.name AS name, ticket.title AS title;
    """,
    database_="neo4j",
  )
  info = "The query `{query}` returned {records_count} records.".format(
    query=summary.query, records_count=len(records),
  ) 
  return render_template('Customer-Ticket.html', info=info, records=records)

@app.route("/available")
def available():
  records, summary, keys = driver.execute_query(
    """
      MATCH (a:Ticket {availability: true, shippability: true})
      RETURN 
        a.title AS title, 
        a.price AS price, 
        a.availability AS availability, 
        a.shippability AS shippability;
    """,
    database_="neo4j",
  )
  info = "The query `{query}` returned {records_count} records.".format(
    query=summary.query, records_count=len(records),
  ) 
  return render_template('Tickets.html', info=info, records=records)

@app.route("/expensive")
def expensive():
  records, summary, keys = driver.execute_query(
    """
      MATCH (a:Ticket)
      WHERE a.price > 300.00
      RETURN a.title AS title, a.price AS price, a.availability AS availability, a.shippability AS shippability;
    """,
    database_="neo4j",
  )
  info = "The query `{query}` returned {records_count} records.".format(
    query=summary.query, records_count=len(records),
  ) 
  return render_template('Tickets.html', info=info, records=records)

@app.route("/martin")
def martin():
  records, summary, keys = driver.execute_query(
    """
      MATCH (customer:Customer {name: 'George Martin'})-[:BOUGHT]->(ticket:Ticket)
      RETURN customer.name AS name, ticket.title AS title;
    """,
    database_="neo4j",
  )
  info = "The query `{query}` returned {records_count} records.".format(
    query=summary.query, records_count=len(records),
  ) 
  return render_template('Customer-Ticket.html', info=info, records=records)


@app.route("/ticketC")
def ticketC():
  return render_template('Default.html')
@app.route("/ticketR")
def ticketR():
  return render_template('Default.html')
@app.route("/ticketU")
def ticketU():
  return render_template('Default.html')
@app.route("/ticketD")
def ticketD():
  return render_template('Default.html')
