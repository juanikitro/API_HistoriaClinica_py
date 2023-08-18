from sqlalchemy import text


def find_dental_controls(session, pers_codigo):
    codigo_odontologia = 15
    
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
                SUB.espeCodigo = {codigo_odontologia}
            ORDER BY TURN.turnCodigo DESC;
        """
    )
    dental_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).fetchone()
    session.commit()

    dental_controls = {
        "value": len(dental_controls) > 0 if dental_controls is not None else False,
        "quantity": len(dental_controls) if dental_controls is not None else 0,
        "lastTurn": dental_controls[0] if dental_controls is not None else None,
        "turnCodigo": dental_controls[1] if dental_controls is not None else None,    
    }

    return dental_controls
