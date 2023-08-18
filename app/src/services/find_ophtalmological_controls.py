from sqlalchemy import text


def find_ophtalmological_controls(session, pers_codigo):
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
