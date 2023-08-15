from sqlalchemy import text


def find_substance_use(session, pers_codigo):
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
