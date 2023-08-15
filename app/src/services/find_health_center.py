from sqlalchemy import text


def find_health_center(session, pers_codigo):
    query = text(
        """SELECT
                UBI.ubicDescripcion,
                TURN.turnFecha,
                TURN.turnCodigo
            FROM 
                SanMiguel.dbo.Turno AS TURN
            LEFT JOIN SanMiguel.dbo.Ubicacion AS UBI 
                ON TURN.ubicCodigo = UBI.ubicCodigo
            INNER JOIN (
                SELECT 
                    ubicCodigo, 
                    MAX(turnCodigo) AS MaxTurnCodigo
                FROM 
                    SanMiguel.dbo.Turno
                WHERE 
                    paciCodigo = :persCodigo AND 
                    turnLlegada IS NOT NULL
                GROUP BY 
                    ubicCodigo
            ) AS GroupedTURN 
                ON TURN.ubicCodigo = GroupedTURN.ubicCodigo AND 
                TURN.turnCodigo = GroupedTURN.MaxTurnCodigo
            ORDER BY 
                TURN.turnCodigo DESC;"""
    )
    query_result = session.execute(
        query,
        {
            "persCodigo": pers_codigo,
        },
    ).all()
    session.commit()

    medical_centers = []
    for item in query_result:
        medical_centers.append(
            {
                "name": item[0],
                "lastTurn": item[1],
                "turnCodigo": item[2],
            }
        )
    return medical_centers
