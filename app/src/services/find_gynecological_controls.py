from sqlalchemy import text


def find_gynecological_controls(session, pers_codigo):
    codigo_ginecologica = 43
    
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
                SUB.espeCodigo = {codigo_ginecologica}
            ORDER BY TURN.turnCodigo DESC;
        """
    )
    gynecological_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()


    gynecological_controls = {
        "value": len(gynecological_controls) > 0 if gynecological_controls is not None else False,
        "quantity": len(gynecological_controls) if gynecological_controls is not None else 0,
        "lastTurn": gynecological_controls[0] if gynecological_controls is not None else None,
        "turnCodigo": gynecological_controls[1] if gynecological_controls is not None else None,    
    }

    return gynecological_controls
