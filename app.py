from flask import Flask, render_template
from neo4j import GraphDatabase
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

URI = "neo4j+s://24b0e9a6.databases.neo4j.io"
AUTH = ("neo4j", "L04tzXcUCk17ek-6YtE0BheidkaSIXV0G_YqrSArtXA")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

class TitleForm(FlaskForm):
    title = StringField('Ticket title', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField('Submit')
    
class CreateForm(FlaskForm):
    title = StringField('Ticket title', validators=[DataRequired(), Length(1, 100)])
    price = StringField('Ticket price', validators=[DataRequired(), Length(1, 100)])
    availability = BooleanField('Ticket availability', validators=[])
    shippability = BooleanField('Ticket shippability', validators=[])
    submit = SubmitField('Submit')

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

@app.route('/ticketC', methods=['GET', 'POST'])
def ticketC_form():
    form = CreateForm()
    if form.validate_on_submit():
        title = form.title.data
        price = form.price.data
        availability = str(form.availability.data)
        shippability = str(form.shippability.data)
        records, summary, keys = driver.execute_query(
        """
          CREATE (a:Ticket {title: $title, price: $price, shippability: $shippability, availability: $availability}) 
          RETURN 
            a.title AS title, 
            a.price AS price, 
            a.availability AS availability, 
            a.shippability AS shippability;
        """,
        parameters_={"title": title, "price": price, "shippability": shippability, "availability": availability},
        database_="neo4j",
        )
        info = "The query `{query}` returned {records_count} records.".format(
          query=summary.query, records_count=len(records),
        ) 
        return render_template('Tickets.html', info=info, records=records)
    return render_template('Create.html', method='Create', form=form)


@app.route('/ticketR', methods=['GET', 'POST'])
def ticketR_form():
    form = TitleForm()
    if form.validate_on_submit():
        title = form.title.data
        records, summary, keys = driver.execute_query(
        """
          MATCH (a:Ticket {title: $title})     
          RETURN 
            a.title AS title, 
            a.price AS price, 
            a.availability AS availability, 
            a.shippability AS shippability;
        """,
        parameters_={"title": title},
        database_="neo4j",
        )
        info = "The query `{query}` returned {records_count} records.".format(
          query=summary.query, records_count=len(records),
        ) 
        return render_template('Tickets.html', info=info, records=records)
    return render_template('Create.html', method='Read', form=form)

@app.route('/ticketU', methods=['GET', 'POST'])
def ticketU_form():
    form = CreateForm()
    if form.validate_on_submit():
        title = form.title.data
        price = form.price.data
        availability = str(form.availability.data)
        shippability = str(form.shippability.data)
        records, summary, keys = driver.execute_query(
        """
          MATCH (a:Ticket {title: $title}) 
          SET 
            a.price = $price, 
            a.availability = $availability,
            a.shippability = $shippability 
          RETURN 
            a.title AS title, 
            a.price AS price, 
            a.availability AS availability, 
            a.shippability AS shippability;
        """,
        parameters_={"title": title, "price": price, "shippability": shippability, "availability": availability},
        database_="neo4j",
        )
        info = "The query `{query}` returned {records_count} records.".format(
          query=summary.query, records_count=len(records),
        ) 
        return render_template('Tickets.html', info=info, records=records)
    return render_template('Create.html', method='Update', form=form)

@app.route('/ticketD', methods=['GET', 'POST'])
def ticketD_form():
    form = TitleForm()
    if form.validate_on_submit():
        title = form.title.data
        records, summary, keys = driver.execute_query(
        """
          MATCH (ticket:Ticket {title: $title}) 
          DETACH DELETE ticket;
        """,
        parameters_={"title": title},
        database_="neo4j",
        )
        info = "The query `{query}` returned {records_count} records.".format(
          query=summary.query, records_count=len(records),
        )
        return render_template('Tickets.html', info=info, records=records)
    return render_template('Create.html', method='Delete', form=form)
