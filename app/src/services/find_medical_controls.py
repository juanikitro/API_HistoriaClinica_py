from sqlalchemy import text


def find_medical_controls(session, pers_codigo):
    query = text(
        """SELECT
                TURN.turnCodigo,
                TURN.turnFechaAsignado
            FROM
                SanMiguel.dbo.Turno AS TURN
            LEFT JOIN SanMiguel.dbo.SubEspecialidad AS SUES ON
                TURN.suesCodigo = SUES.suesCodigo
            WHERE
                TURN.paciCodigo = :persCodigo AND
                TURN.turnLlegada IS NOT NULL
            ORDER BY TURN.turnCodigo DESC;"""
    )
    medical_controls = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).all()
    session.commit()

    medical_controls = {
        "quantity": len(medical_controls),
        "lastTurn": medical_controls[0][1] if len(medical_controls) > 0 else None,
        "turnCodigo": medical_controls[0][0] if len(medical_controls) > 0 else None,
    }

    return medical_controls
