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
    """
    The function `find_pers_codigo` retrieves the most recent `persCodigo` from the `Persona` table in
    the `SanMiguel.dbo` database based on the provided `person` object's document number, document type,
    and gender.
    
    :param person: The "person" parameter is an object that represents a person. It likely has
    attributes such as "document_number" (the person's document number), "document_type" (the type of
    document, such as passport or ID card), and "gender" (the person's gender)
    :param session: The "session" parameter is an object that represents a connection to a database. It
    is used to execute SQL queries and interact with the database
    :return: the value of the persCodigo column from the first row of the query result.
    """
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
