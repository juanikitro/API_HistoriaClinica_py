from sqlalchemy import text


def find_turns(session, pers_codigo):
    # TODO: Analizar si "suesDescripcion" y "turnFecha" estan OK
    query = text(
        """SELECT
                TURN.turnFechaAsignado,
                SUB.suesDescripcion,
                TURN.turnLlegada,
                TURN.turnReprogramar,
                TURN.turnFecha, 
                TURN.turnCodigo
            FROM
                SanMiguel.dbo.Turno AS TURN
            LEFT JOIN SanMiguel.dbo.SubEspecialidad AS SUB ON
                TURN.suesCodigo = SUB.suesCodigo
            WHERE
                TURN.paciCodigo = :persCodigo
            ORDER BY TURN.turnCodigo DESC;"""
    )
    query_result = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).all()
    session.commit()

    turns = []
    for item in query_result:
        turns.append(
            {
                "date": item[0],
                "specialty": item[1],
                "attend": bool(item[2]),
                "rescheduled": item[3],
                "rescheduledDate": item[4],
                "turnCodigo": item[5],
            }
        )

    return turns
