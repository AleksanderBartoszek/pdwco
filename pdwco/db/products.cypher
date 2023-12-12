CREATE 
  (concert:   Category {title: 'Concert Tickets'}), 
  (theater:   Category {title: 'Theater Tickets'}), 
  (opera:     Category {title: 'Opera Tickets'})

// Concerts
CREATE (rammstein:    Ticket {title: 'Rammstein', price: 365.00, shippability: true, availability: true})
CREATE (miley_cyrus:  Ticket {title: 'Miley Cyrus', price: 384.00, shippability: true, availability: true})
CREATE (taylor_swift: Ticket {title: 'Taylor Swift', price: 229.50, shippability: true, availability: false})
CREATE (lana_del_rey: Ticket {title: 'Lana Del Rey', price: 374.20, shippability: true, availability: false})
CREATE (nickelback:   Ticket {title: 'Nickelback', price: 420.87, shippability: true, availability: true})
CREATE (eminem:       Ticket {title: 'Eminem', price: 191.00, shippability: true, availability: true})

MERGE (rammstein)     -[:IS_IN]->(concert)
MERGE (miley_cyrus)   -[:IS_IN]->(concert)
MERGE (taylor_swift)  -[:IS_IN]->(concert)
MERGE (lana_del_rey)  -[:IS_IN]->(concert)
MERGE (nickelback)    -[:IS_IN]->(concert)
MERGE (eminem)        -[:IS_IN]->(concert)

// Theater
CREATE (macbeth:          Ticket {title: 'Macbeth', price: 195.00, shippability: true, availability: false})
CREATE (otello:           Ticket {title: 'Otello', price: 171.30, shippability: true, availability: true})
CREATE (romeo_and_juliet: Ticket {title: 'Romeo & Juliet', price: 247.50, shippability: true, availability: true})
CREATE (king_lear:        Ticket {title: 'King Lear', price: 129.00, shippability: false, availability: true})

MERGE (macbeth)           -[:IS_IN]->(theater)
MERGE (otello)            -[:IS_IN]->(theater)
MERGE (romeo_and_juliet)  -[:IS_IN]->(theater)
MERGE (king_lear)         -[:IS_IN]->(theater)

// Opera
CREATE (carmen:       Ticket {title: 'Carmen', price: 294.00, shippability: true, availability: false})
CREATE (don_giovanni: Ticket {title: 'Don Giovanni', price: 312.35, shippability: true, availability: true})

MERGE (carmen)        -[:IS_IN]->(opera)
MERGE (don_giovanni)  -[:IS_IN]->(opera)