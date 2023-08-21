from sqlalchemy import text


def find_medical_controls(session, pers_codigo):
    """
    The function `find_medical_controls` retrieves the quantity, last turn date, and turn code of
    medical controls for a given person code from a database.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter "pers_codigo" is the personal code of a patient. It is used to
    filter the medical controls based on the patient's code
    :return: a dictionary with the following keys:
    - "quantity": the number of medical controls found
    - "lastTurn": the date and time of the last medical control (if any)
    - "turnCodigo": the code of the last medical control (if any)
    """
    query = text(
        """SELECT
                TURN.turnCodigo,
                TURN.turnFechaAsignado
            FROM
                SanMiguel.dbo.Turno AS TURN
            LEFT JOIN SanMiguel.dbo.SubEspecialidad AS SUES ON
                TURN.suesCodigo = SUES.suesCodigo
            WHERE
                TURN.paciCodigo = :persCodigo AND
                TURN.turnLlegada IS NOT NULL
            ORDER BY TURN.turnCodigo DESC;"""
    )
    medical_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).all()
    session.commit()

    medical_controls = {
        "quantity": len(medical_controls),
        "lastTurn": medical_controls[0][1] if len(medical_controls) > 0 else None,
        "turnCodigo": medical_controls[0][0] if len(medical_controls) > 0 else None,
    }

    return medical_controls
