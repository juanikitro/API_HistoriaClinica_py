from sqlalchemy import text


def find_pediatric_controls(session, pers_codigo):
    """
    The function `find_pediatric_controls` retrieves information about pediatric controls for a given
    patient from a database.
    
    :param session: The `session` parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter `pers_codigo` is the personal code of a patient
    :return: a dictionary with the following keys and values:
    - "value": a boolean indicating whether there are pediatric controls for the given person code.
    - "quantity": an integer indicating the number of pediatric controls for the given person code.
    - "lastTurn": a datetime object indicating the date and time of the last pediatric control for the
    given person code.
    - "turnCodigo": an integer
    """
    codigo_pediatria = 19
    
    query = text(
        f"""SELECT
                TURN.turnFechaAsignado,
                TURN.turnCodigo
            FROM
                SanMiguel.dbo.Turno AS TURN
            LEFT JOIN SanMiguel.dbo.SubEspecialidad AS SUB ON
                TURN.suesCodigo = SUB.suesCodigo
            WHERE
                TURN.paciCodigo = :persCodigo AND
                SUB.espeCodigo = {codigo_pediatria}
            ORDER BY TURN.turnCodigo DESC;
        """
    )
    pediatric_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()


    pediatric_controls = {
        "value": len(pediatric_controls) > 0 if pediatric_controls is not None else False,
        "quantity": len(pediatric_controls) if pediatric_controls is not None else 0,
        "lastTurn": pediatric_controls[0] if pediatric_controls is not None else None,
        "turnCodigo": pediatric_controls[1] if pediatric_controls is not None else None,    
    }

    return pediatric_controls
