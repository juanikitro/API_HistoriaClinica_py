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
        "E08",
        "E09",
        "E10",
        "E11",
        "E13",
        "I20",
        "I21",
        "I22",
        "I23",
        "I24",
        "I25",
        "I30",
        "I31",
        "I32",
        "I33",
        "I34",
        "I35",
        "I36",
        "I37",
        "I38",
        "I39",
        "I40",
        "I41",
        "I42",
        "I43",
        "I44",
        "I45",
        "I46",
        "I47",
        "I48",
        "I49",
        "I50",
        "I51",
        "I52",
        "I70",
        "I71",
        "I72",
        "I73",
        "I74",
        "I75",
        "I76",
        "I77",
        "I78",
        "I79",
        "I10",
        "I11",
        "I12",
        "I13",
        "I14",
        "I15",
        "I16",
        "J44",
        "J45",
        "A15",
        "I26",
        "J47",
        "C34",
        "C50",
        "C61",
        "C18",
        "C19",
        "C20",
        "C16",
        "C53",
        "C56",
        "C43",
        "C73",
        "C25",
        "C67",
        "C64",
        "B20",
        "B21",
        "B22",
        "B23",
        "B24"
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
