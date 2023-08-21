from sqlalchemy import text


def find_substance_use(session, pers_codigo):
    """
    The `find_substance_use` function retrieves information about the last turn and whether a patient
    has a substance use diagnosis based on their personal code.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter `pers_codigo` represents the personal code of a patient
    :return: a dictionary with the following keys and values:
    - "value": a boolean value indicating whether the patient has a substance use diagnosis (True if
    they have, False if they don't).
    - "lastTurn": the date of the last assigned turn for the patient with a substance use diagnosis
    (None if there is no diagnosis).
    - "turnCodigo": the code of the last assigned
    """
    diag_codigos_internos = [
        "F10",
        "F11",
        "F12",
        "F13",
        "F14",
        "F15",
        "F16",
        "F17",
        "F18",
        "F19",
    ]
    string_codigos = "', '".join(diag_codigos_internos)

    query = text(
        f"""SELECT TOP 1
                t.turnCodigo, 
                t.turnFechaAsignado
            FROM 
                SanMiguel.dbo.Turno AS t
            INNER JOIN 
                SanMiguel.dbo.PacienteNomenclador AS pn ON t.paciCodigo = pn.paciCodigo 
            INNER JOIN 
                SanMiguel.dbo.Diagnostico AS d ON pn.diagCodigo = d.diagCodigo 
            WHERE 
                d.diagCodigoInterno IN ('{string_codigos}')
                AND 
                t.paciCodigo = :persCodigo
            ORDER BY t.turnCodigo DESC;"""
    )
    substance_use = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()

    substance_use = {
        "value": substance_use[0] is not None if substance_use is not None else False,
        "lastTurn": substance_use[1] if substance_use is not None else None,
        "turnCodigo": substance_use[0] if substance_use is not None else None,
    }

    return substance_use
