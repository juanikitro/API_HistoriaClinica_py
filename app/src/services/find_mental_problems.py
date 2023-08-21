from sqlalchemy import text


def find_mental_problems(session, pers_codigo):
    """
    The function `find_mental_problems` retrieves the latest turn code for a given patient with a
    specific set of mental problem diagnosis codes.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter "pers_codigo" represents the personal code of a patient. It is
    used to identify the patient for whom we want to find any mental problems
    :return: The function `find_mental_problems` returns a dictionary with a single key-value pair. The
    key is "value" and the value is a boolean indicating whether there are any mental problems
    associated with the given `pers_codigo`.
    """
    diag_codigos_internos = [
        "F00",
        "F01",
        "F03",
        "F06",
        "F07",
        "F09",
        "F20",
        "F20.0",
        "F20.1",
        "F20.3",
        "F20.9",
        "F22",
        "F23",
        "F25",
        "F29",
        "F30",
        "F31",
        "F32",
        "F33",
        "F39",
        "F40",
        "F41",
        "F42",
        "F43.0",
        "F43.1",
        "F43.2",
        "F44",
        "F45",
        "F48",
        "F50",
        "F53",
        "F60.3",
        "F61",
        "F63",
        "F69",
        "F70",
        "F71",
        "F72",
        "F79",
        "F84.0",
        "F84.5",
        "F84.9",
        "F90.0",
        "F91",
        "F91.3",
        "F92",
        "F93",
        "F94",
        "F98",
        "F99",
    ]
    string_codigos = "', '".join(diag_codigos_internos)

    query = text(
        f"""SELECT TOP 1
                t.turnCodigo
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
    mental_problems = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()

    mental_problems = {
        "value": mental_problems is not None,
    }

    return mental_problems
