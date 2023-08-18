from sqlalchemy import text


def find_pediatric_controls(session, pers_codigo):
    codigo_pediatria = 19
    
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
                SUB.espeCodigo = {codigo_pediatria}
            ORDER BY TURN.turnCodigo DESC;
        """
    )
    pediatric_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()


    pediatric_controls = {
        "value": len(pediatric_controls) > 0 if pediatric_controls is not None else False,
        "quantity": len(pediatric_controls) if pediatric_controls is not None else 0,
        "lastTurn": pediatric_controls[0] if pediatric_controls is not None else None,
        "turnCodigo": pediatric_controls[1] if pediatric_controls is not None else None,    
    }

    return pediatric_controls
