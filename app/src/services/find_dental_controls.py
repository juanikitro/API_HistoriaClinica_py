from sqlalchemy import text


def find_dental_controls(session, pers_codigo):
    """
    The function `find_dental_controls` retrieves dental controls for a specific patient from a
    database.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter `pers_codigo` is the personal code of the patient for whom we want
    to find dental controls
    :return: a dictionary with the following keys and values:
    """
    codigo_odontologia = 15
    
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
                SUB.espeCodigo = {codigo_odontologia}
            ORDER BY TURN.turnCodigo DESC;
        """
    )
    dental_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()

    dental_controls = {
        "value": len(dental_controls) > 0 if dental_controls is not None else False,
        "quantity": len(dental_controls) if dental_controls is not None else 0,
        "lastTurn": dental_controls[0] if dental_controls is not None else None,
        "turnCodigo": dental_controls[1] if dental_controls is not None else None,    
    }

    return dental_controls
