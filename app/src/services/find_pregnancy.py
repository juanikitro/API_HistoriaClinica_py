from sqlalchemy import text


def find_pregnancy(session, pers_codigo):
    """
    The `find_pregnancy` function retrieves information about a patient's pregnancy status, including
    whether they are pregnant, if they are a minor, if there are any pregnancy-related risks, the number
    of controls, and the details of the last turn.
    
    :param session: The `session` parameter is an object representing the database session. It is used
    to execute the SQL query and commit any changes made to the database
    :param pers_codigo: The parameter `pers_codigo` is the personal code of the patient for whom you
    want to find pregnancy information
    :return: a dictionary with the following keys and values:
    """
    diag_codigos_internos = [
        "O21.2",
        "P01.4",
        "Z64.0",
        "Z34.9",
        "Z34.8",
        "Z34.0",
        "O48",
        "Z35.3",
        "Z35.7",
        "Z35.3",
        "Z35.9",
        "Z35.7",
        "Z35.8",
        "Z35.4",
        "Z35.1",
        "Z35.3",
        "Z35.3",
        "Z35.0",
        "Z35.2",
        "Z35.1",
        "Z35.2",
        "Z35.2",
        "Z35.2",
        "Z35.3",
        "Z35.5",
        "Z35.6",
    ]
    diag_codigos_riesgo = [
        "Z35.3",
        "Z35.7",
        "Z35.3",
        "Z35.9",
        "Z35.7",
        "Z35.8",
        "Z35.4",
        "Z35.1",
        "Z35.3",
        "Z35.3",
        "Z35.0",
        "Z35.2",
        "Z35.1",
        "Z35.2",
        "Z35.2",
        "Z35.2",
        "Z35.3",
        "Z35.5",
        "Z35.6",
    ]

    string_codigos = "', '".join(diag_codigos_internos)
    string_riesgo = "', '".join(diag_codigos_riesgo)

    query = text(
        f"""SELECT 
                t.turnCodigo, 
                t.turnFechaAsignado,
                CASE 
                    WHEN DATEADD(YEAR, 18, p.persFechaNacimiento) > GETDATE() THEN '1'
                    ELSE '0'
                END as 'minor',
                CASE
                    WHEN d.diagCodigoInterno IN ('{string_riesgo}') THEN 'true'
                    ELSE 'false'
                END as 'risk'
            FROM 
                SanMiguel.dbo.Turno AS t
            INNER JOIN 
                SanMiguel.dbo.PacienteNomenclador AS pn ON t.paciCodigo = pn.paciCodigo 
            INNER JOIN 
                SanMiguel.dbo.Diagnostico AS d ON pn.diagCodigo = d.diagCodigo 
            INNER JOIN
                SanMiguel.dbo.Persona AS p ON t.paciCodigo = p.persCodigo
            WHERE 
                d.diagCodigoInterno IN ('{string_codigos}')
                AND 
                t.paciCodigo = :persCodigo
                AND t.turnFechaAsignado >= DATEADD(MONTH, -9, GETDATE())
            ORDER BY t.turnCodigo DESC;"""
    )

    pregnancy = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).all()
    session.commit()

    pregnancy = {
        "value": pregnancy is not None and len(pregnancy) > 0,
        "minor": pregnancy[2] == "1" if len(pregnancy) > 0 else None,
        "risk": pregnancy[3] == "true" if len(pregnancy) > 0 else None,
        "numberOfControls": len(pregnancy) if len(pregnancy) > 0 else 0,
        "lastTurn": pregnancy[1] if len(pregnancy) > 0 else None,
        "turnCodigo": pregnancy[0] if len(pregnancy) > 0 else None,
    }

    return pregnancy
