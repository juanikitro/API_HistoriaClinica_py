from sqlalchemy import text


documentTypes = {
    1: "DNI",
    2: "CUIT",
    3: "CDI",
    4: "LE",
    5: "LC",
    6: "CI Ext.",
    7: "CUIL",
    8: "Pasaporte",
    9: "Otro",
    10: "Sin Documento",
    11: "Parto",
}


def find_pers_codigo(person, session):
    query = text(
        """SELECT TOP 1 persCodigo 
            FROM SanMiguel.dbo.Persona 
            WHERE persNroDocumento=:document_number 
            AND tdocCodigo=:document_type 
            AND persSexo=:gender 
            ORDER BY persCodigo DESC"""
    )
    pers_codigo = session.execute(
        query,
        {
            "document_number": person.document_number,
            "document_type": next(
                (
                    key
                    for key, value in documentTypes.items()
                    if value == person.document_type
                ),
                1,
            ),
            "gender": person.gender,
        },
    ).fetchone()
    session.commit()

    if not pers_codigo:
        return None

    return pers_codigo[0]
