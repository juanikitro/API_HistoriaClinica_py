from sqlalchemy import text


def find_pregnancy(session, pers_codigo):
    diag_codigos_internos = [
        "",
    ]
    string_codigos = "', '".join(diag_codigos_internos)

    query = text(
        f"""SELECT 
            t.turnCodigo, 
            t.turnFechaAsignado,
            CASE 
                WHEN DATEADD(YEAR, 18, p.persFechaNacimiento) > GETDATE() THEN '1'
                ELSE '0'
            END as 'minor'
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

    print(pregnancy)

    pregnancy = {
        "value": pregnancy is not None and len(pregnancy) > 0,
        "minor": pregnancy[2] == "1" if len(pregnancy) > 0 else None,
        "risk": False,  # TODO: implementar RISK. No se de donde sale
        "numberOfControls": len(pregnancy),
        "lastTurn": pregnancy[1] if len(pregnancy) > 0 else None,
        "turnCodigo": pregnancy[0] if len(pregnancy) > 0 else None,
    }

    return pregnancy
