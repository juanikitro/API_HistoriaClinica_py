from sqlalchemy import text


def find_ophtalmological_controls(session, pers_codigo):
    """
    The function `find_ophtalmological_controls` retrieves information about ophthalmological controls
    for a specific patient.
    
    :param session: The `session` parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter "pers_codigo" is the personal code of the patient for whom we want
    to find ophthalmological controls
    :return: a dictionary with the following keys and values:
    - "value": a boolean indicating whether there are ophthalmological controls for the given person
    code.
    - "quantity": an integer indicating the number of ophthalmological controls for the given person
    code.
    - "lastTurn": a datetime object indicating the date of the last ophthalmological control.
    - "turnCodigo": an integer indicating
    """
    codigo_oftalmologia = 16
    
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
                SUB.espeCodigo = {codigo_oftalmologia}
            ORDER BY TURN.turnCodigo DESC;
        """
    )
    ophtalmological_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()


    ophtalmological_controls = {
        "value": len(ophtalmological_controls) > 0 if ophtalmological_controls is not None else False,
        "quantity": len(ophtalmological_controls) if ophtalmological_controls is not None else 0,
        "lastTurn": ophtalmological_controls[0] if ophtalmological_controls is not None else None,
        "turnCodigo": ophtalmological_controls[1] if ophtalmological_controls is not None else None,    
    }

    return ophtalmological_controls
