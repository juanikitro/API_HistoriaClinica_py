from sqlalchemy import text


def find_gynecological_controls(session, pers_codigo):
    """
    The function `find_gynecological_controls` retrieves information about gynecological controls for a
    given patient from a database.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter "pers_codigo" is the personal code of the patient for whom you
    want to find gynecological controls
    :return: a dictionary with the following keys and values:
    - "value": a boolean indicating if there are gynecological controls for the given person code.
    - "quantity": an integer indicating the number of gynecological controls for the given person code.
    - "lastTurn": a datetime indicating the date of the last gynecological control for the given person
    code.
    - "turnCodigo
    """
    codigo_ginecologica = 43
    
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
                SUB.espeCodigo = {codigo_ginecologica}
            ORDER BY TURN.turnCodigo DESC;
        """
    )
    gynecological_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()


    gynecological_controls = {
        "value": len(gynecological_controls) > 0 if gynecological_controls is not None else False,
        "quantity": len(gynecological_controls) if gynecological_controls is not None else 0,
        "lastTurn": gynecological_controls[0] if gynecological_controls is not None else None,
        "turnCodigo": gynecological_controls[1] if gynecological_controls is not None else None,    
    }

    return gynecological_controls
