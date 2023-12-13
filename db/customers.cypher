// Customers
CREATE (michael:  Customer {name: 'Michael Jackson', email: 'mj@example.com', age: 31})
CREATE (jason:    Customer {name: 'Jason Statham', email: 'js@example.com', age: 23})
CREATE (alex:     Customer {name: 'Alex Kava', email: 'ak@example.com', age: 42})
CREATE (george:   Customer {name: 'George Martin', email: 'gm@example.com', age: 54})

MERGE (michael)-[:VIEWED {views_count: 15}]->(rammstein)
MERGE (michael)-[:ADDED_TO_WISH_LIST]->(otello)
MERGE (michael)-[:BOUGHT]->(don_giovanni)

MERGE(jason)-[:VIEWED {views_count: 10}]->(king_lear)
MERGE(jason)-[:VIEWED {views_count: 20}]->(macbeth)
MERGE(jason)-[:ADDED_TO_WISH_LIST]->(romeo_and_juliet)

MERGE(alex)-[:VIEWED {views_count: 20}]->(lana_del_rey)
MERGE(alex)-[:ADDED_TO_WISH_LIST]->(taylor_swift)
MERGE(alex)-[:ADDED_TO_WISH_LIST]->(miley_cyrus)
MERGE(alex)-[:BOUGHT]->(nickelback)

MERGE(george)-[:ADDED_TO_WISH_LIST]->(macbeth)
MERGE(george)-[:ADDED_TO_WISH_LIST]->(eminem)
MERGE(george)-[:BOUGHT]->(eminem)
MERGE(george)-[:BOUGHT]->(carmen);