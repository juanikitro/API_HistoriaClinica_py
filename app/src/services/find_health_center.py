from sqlalchemy import text


def find_health_center(session, pers_codigo):
    """
    The function `find_health_center` retrieves the latest health center visits for a given person code.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter "pers_codigo" is the personal code of a person. It is used in the
    query to filter the results and find the health centers where the person has had the latest
    appointments
    :return: The function `find_health_center` returns a list of dictionaries. Each dictionary
    represents a medical center and contains the following information:
    - "name": The name of the medical center (from the column `ubicDescripcion` in the query result).
    - "lastTurn": The date of the last turn (from the column `turnFecha` in the query result).
    - "turnCodigo": The code of
    """
    query = text(
        """SELECT
                UBI.ubicDescripcion,
                TURN.turnFecha,
                TURN.turnCodigo
            FROM 
                SanMiguel.dbo.Turno AS TURN
            LEFT JOIN SanMiguel.dbo.Ubicacion AS UBI 
                ON TURN.ubicCodigo = UBI.ubicCodigo
            INNER JOIN (
                SELECT 
                    ubicCodigo, 
                    MAX(turnCodigo) AS MaxTurnCodigo
                FROM 
                    SanMiguel.dbo.Turno
                WHERE 
                    paciCodigo = :persCodigo AND 
                    turnLlegada IS NOT NULL
                GROUP BY 
                    ubicCodigo
            ) AS GroupedTURN 
                ON TURN.ubicCodigo = GroupedTURN.ubicCodigo AND 
                TURN.turnCodigo = GroupedTURN.MaxTurnCodigo
            ORDER BY 
                TURN.turnCodigo DESC;"""
    )
    query_result = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).all()
    session.commit()

    medical_centers = []
    for item in query_result:
        medical_centers.append(
            {
                "name": item[0],
                "lastTurn": item[1],
                "turnCodigo": item[2],
            }
        )
    return medical_centers
