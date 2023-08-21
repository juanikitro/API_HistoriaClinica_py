from sqlalchemy import text


def find_catastrophic_sickness(session, pers_codigo):
    """
    The function `find_catastrophic_sickness` retrieves the latest turn code for a patient with a
    specific diagnosis code from the database.
    
    :param session: The "session" parameter is an instance of a database session. It is used to execute
    the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter "pers_codigo" is the personal code of a patient. It is used to
    identify the patient for whom we want to find if they have a catastrophic sickness
    :return: a dictionary with a single key-value pair. The key is "value" and the value is a boolean
    indicating whether a catastrophic sickness was found.
    """
    diag_codigos_internos = [
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
    catastrophic_sickness = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()

    catastrophic_sickness = {
        "value": catastrophic_sickness is not None,
    }

    return catastrophic_sickness
