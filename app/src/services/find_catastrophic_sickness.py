from sqlalchemy import text


def find_catastrophic_sickness(session, pers_codigo):
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
