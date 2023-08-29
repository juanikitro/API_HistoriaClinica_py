# Correr API con docker-compose
Para construir la API y correrla en localhost:3000 (por defecto), utilizando la red del servidor (para evitar problemas de VPN con la DB)
```bash
docker-compose up -d --build
```

---

# .env
```
PORT = int
AUTH_USER = string
AUTH_PASS = string
TOKEN_EXPIRES = int
ALGORITHM = string
SECRET_KEY = string
DATABASE_URL = string
```

---

# Modificaciones
## Codigos CIE10
Para modificar los codigos que referencian a cada caso de diagnostico, se deben modificar en sus respectivos arrays. Para esto se deben seguir los siguientes pasos:
1. Encontrar el archivo que construya el diagnostico a modificar (suele llamarse igual a la key de la response con el prefijo "find", por ejemplo "pregnancy" se debera modificar en "find_pregnancy.py")
2. Al entrar al archivo deseado se debe encontrar el array que referencia los codigos CIE10. Siguiendo el ejemplo de pregnancy, el array es `diag_codigos_internos` para los codigos de embarazo y `diag_codigos_riesgo` para los codigos de embarazo de riesgo
3. Una vez identificado el array, este se puede modificar con total libertad, respetando que siempre debe ser un array de strings, por ejemplo: 
```py
    diag_codigos_internos = ["O21.2", "P01.4"]
```

## Codigos de especialidad
En otros casos, se buscan los turnos cuya subespecialidad este referenciando a la especialidad deseada, por ejemplo pediatria. Para modificar el codigo con el que se relaciona la especialidad, se deben seguir los siguientes pasos:
1. Encontrar el archivo que construya el diagnostico a modificar (suele llamarse igual a la key de la response con el prefijo "find", por ejemplo "pediatric_controls" se debera modificar en "find_pediatric_controls.py")
2. Al entrar al archivo deseado se debe encontrar la variable que referencie al codigo de especialidad. Siguiendo el ejemplo de pediatric_controls, la variable es llamada `codigo_pediatria`
3. Una vez identificada la variable, se puede modificar siempre y cuando siga siendo un int, por ejemplo:
```py
    codigo_pediatria = 19
```

---

# Endpoints
## GET /v1/auth
### Request example
```json
{
    "user": "D3f4ultUs3r",
    "password": "D3f4ultP4ssw0rd"
}
```

### Response example
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJEM2Y0dWx0VXMzciIsImV4cCI6MTc1MjM3NzI4OX0.PmzJD1odHQDdjyMeDiKUg0zEcTQTLjhAQoEvoGvDhdo",
    "token_type": "bearer"
}
```

## GET /v1/person
### Request example
```json
{
    "document_type":"DNI",
    "document_number": "37057692",
    "gender": "F"
}
```

### Response example
```json
{
    "person": {
        "document_number": "37057692",
        "document_type": "DNI",
        "gender": "F",
        "persCodigo": 145132
    },
    "indicators": {
        "substanceUse": {
            "value": false,
            "lastTurn": null,
            "turnCodigo": null
        },
        "mentalProblems": {
            "value": false
        },
        "catastrophicSickness": {
            "value": false
        },
        "medicalControls": {
            "quantity": 57,
            "lastTurn": "2023-04-17T09:39:50.637000",
            "turnCodigo": 94201762
        },
        "medicalCenters": [
            {
                "name": "CAP DRA. MARTA ANTONIAZZI",
                "lastTurn": "2023-04-17T00:00:00",
                "turnCodigo": 94201762
            },
            {
                "name": "CAP SAN MIGUEL OESTE",
                "lastTurn": "2023-02-14T00:00:00",
                "turnCodigo": 75266969
            },
            {
                "name": "CAP DR. LUIS SUÁREZ PARÍS",
                "lastTurn": "2022-11-25T00:00:00",
                "turnCodigo": 55173838
            },
            {
                "name": "HOSPITAL MUNICIPAL DR. RAUL LARCADE",
                "lastTurn": "2022-11-04T00:00:00",
                "turnCodigo": 50334709
            },
            {
                "name": "CAP DR. ALBERTO SABÍN",
                "lastTurn": "2022-10-17T00:00:00",
                "turnCodigo": 47016589
            },
            {
                "name": "HOSPITAL SANTA MARIA",
                "lastTurn": "2022-05-19T00:00:00",
                "turnCodigo": 20770467
            },
            {
                "name": "HOSPITAL OFTALMOLÓGICO MONSEÑOR BARBICH",
                "lastTurn": "2020-11-24T00:00:00",
                "turnCodigo": 8408057
            },
            {
                "name": "CAP 20 DE JULIO ",
                "lastTurn": "2020-01-20T00:00:00",
                "turnCodigo": 8023655
            }
        ],
        "turns": [
            {
                "date": "2023-04-17T09:39:50.637000",
                "specialty": "CLINICA MEDICA",
                "attend": true,
                "rescheduled": false,
                "rescheduledDate": "2023-04-17T00:00:00",
                "turnCodigo": 94201762
            },
            {
                "date": "2023-02-14T10:45:03.857000",
                "specialty": null,
                "attend": true,
                "rescheduled": false,
                "rescheduledDate": "2023-02-14T00:00:00",
                "turnCodigo": 75266969
            },
            {
                "date": "2023-01-06T11:07:32.637000",
                "specialty": "OBSTETRICA",
                "attend": false,
                "rescheduled": false,
                "rescheduledDate": "2023-01-20T00:00:00",
                "turnCodigo": 65106366
            },
            {
                "date": "2022-11-25T12:51:21.863000",
                "specialty": "OBSTETRICA",
                "attend": true,
                "rescheduled": false,
                "rescheduledDate": "2022-11-25T00:00:00",
                "turnCodigo": 55173838
            },
            {
                "date": "2022-11-18T11:57:32.817000",
                "specialty": "OBSTETRICA",
                "attend": false,
                "rescheduled": false,
                "rescheduledDate": "2022-11-29T00:00:00",
                "turnCodigo": 53345928
            },
            {
                "date": "2022-11-04T22:42:07.927000",
                "specialty": null,
                "attend": true,
                "rescheduled": false,
                "rescheduledDate": "2022-11-04T00:00:00",
                "turnCodigo": 50334709
            },
            {
                "date": "2022-11-04T10:43:59.767000",
                "specialty": null,
                "attend": true,
                "rescheduled": false,
                "rescheduledDate": "2022-11-04T00:00:00",
                "turnCodigo": 50332418
            },
            {
                "date": "2022-11-04T10:43:32.920000",
                "specialty": "OBSTETRICA",
                "attend": true,
                "rescheduled": false,
                "rescheduledDate": "2022-11-04T00:00:00",
                "turnCodigo": 50332414
            },
            {
                "date": "2022-10-30T00:21:29.930000",
                "specialty": null,
                "attend": true,
                "rescheduled": false,
                "rescheduledDate": "2022-10-30T00:00:00",
                "turnCodigo": 50312049
            },
        ],
        "pregnancy": {
            "value": false,
            "minor": null,
            "risk": null,
            "numberOfControls": 0,
            "lastTurn": null,
            "turnCodigo": null
        },
        "pediatricControls": {
            "value": false,
            "quantity": 0,
            "lastTurn": null,
            "turnCodigo": null
        },
        "dentalControls": {
            "value": true,
            "quantity": 2,
            "lastTurn": "2021-10-27T10:15:47.300000",
            "turnCodigo": 6430258
        },
        "ophthalmologicalControls": {
            "value": true,
            "quantity": 2,
            "lastTurn": "2022-01-27T13:48:07.257000",
            "turnCodigo": 12404598
        },
        "gynecologicalControls": {
            "value": true,
            "quantity": 2,
            "lastTurn": "2019-06-18T14:34:37.707000",
            "turnCodigo": 7158507
        }
    }
}
```
