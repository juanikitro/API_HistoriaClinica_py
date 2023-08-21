from sqlalchemy import text


def find_turns(session, pers_codigo):
    """
    The `find_turns` function retrieves a list of turns for a given person code from a database and
    returns the turns as a list of dictionaries.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter "pers_codigo" is the personal code of a person. It is used in the
    SQL query to filter the results and retrieve the turns associated with that person
    :return: a list of dictionaries, where each dictionary represents a turn. Each dictionary contains
    the following information:
    - "date": the date the turn was assigned
    - "specialty": the description of the specialty
    - "attend": a boolean indicating if the turn was attended or not
    - "rescheduled": the reason for rescheduling the turn
    - "rescheduledDate": the
    """
    query = text(
        """SELECT
            TURN.turnFechaAsignado,
            ESPE.espeDescripcion,
            TURN.turnLlegada,
            TURN.turnReprogramar,
            TURN.turnFecha, 
            TURN.turnCodigo
        FROM
            SanMiguel.dbo.Turno AS TURN
        LEFT JOIN SanMiguel.dbo.SubEspecialidad AS SUB ON
            TURN.suesCodigo = SUB.suesCodigo
        LEFT JOIN SanMiguel.dbo.Especialidad AS ESPE ON
            SUB.espeCodigo = ESPE.espeCodigo
        WHERE
            TURN.paciCodigo = :persCodigo
        ORDER BY TURN.turnCodigo DESC;"""
    )
    query_result = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).all()
    session.commit()

    turns = []
    for item in query_result:
        turns.append(
            {
                "date": item[0],
                "specialty": item[1],
                "attend": bool(item[2]),
                "rescheduled": item[3],
                "rescheduledDate": item[4],
                "turnCodigo": item[5],
            }
        )

    return turns
