CREATE_ROUNDS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rounds (id SERIAL NOT NULL PRIMARY KEY, date DATE, results TEXT[]);"
)

GET_ALL_ROUNDS = (
    "SELECT * FROM rounds order by id"
)

INSERT_ROUND = (
    "INSERT INTO rounds (date, results) VALUES (%s, %s)"
)

DELETE_ROUND = (
    "DELETE FROM rounds WHERE id = %s"
)

GET_ROUND_BY_ID = (
    "SELECT * FROM rounds WHERE id = %s"
)

UPDATE_ROUND = (
    "UPDATE rounds SET date = %s, results = %s WHERE id = %s"
)
