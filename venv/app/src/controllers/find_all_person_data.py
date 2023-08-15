from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from ..services.find_pers_codigo import find_pers_codigo
from ..services.find_substance_use import find_substance_use
from ..services.find_mental_problems import find_mental_problems
from ..services.find_medical_controls import find_medical_controls
from ..services.find_health_center import find_health_center
from ..services.find_turns import find_turns
from ..services.find_pregnancy import find_pregnancy

from ..models.PersonData import PersonData


def find_all_person_data(person: PersonData):
    engine = create_engine(os.getenv("DATABASE_URL"))
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    try:
        pers_codigo = find_pers_codigo(person, session)
        if not pers_codigo:
            return HTTPException(
                status_code=404,
                detail="Person not found",
            )

        all_person_data = {
            "person": {
                "document_number": person.document_number,
                "document_type": person.document_type,
                "gender": person.gender,
                "persCodigo": pers_codigo,
            },
            "indicators": {
                "substanceUse": find_substance_use(session, pers_codigo),
                "mentalProblems": find_mental_problems(session, pers_codigo),
                "recurrentOrChronicSickness": {
                    "value": "ELIAS",
                },
                "catastrophicSickness": {
                    "value": "ELIAS",
                },
                "disability": {
                    "value": "ELIAS",
                    "type": "ELIAS",
                },
                "medicalControls": find_medical_controls(session, pers_codigo),
                "therapeuticTreatment": {
                    "value": "ELIAS",
                    "type": "ELIAS",
                },
                "medicalCenters": find_health_center(session, pers_codigo),
                "turns": find_turns(session, pers_codigo),
                "pregnancy": find_pregnancy(session, pers_codigo),
                "pediatricControls": {
                    "value": "boolean",
                    "quantity": "integer",
                    "lastTurn": "date",
                    "turnCodigo": "integer",
                },
                "dentalControls": {
                    "value": "boolean",
                    "lastTurn": "date",
                    "turnCodigo": "integer",
                },
                "ophthalmologicalControls": {
                    "value": "boolean",
                    "lastTurn": "date",
                    "turnCodigo": "integer",
                },
                "gynecologicalControls": {
                    "value": "boolean",
                    "lastTurn": "date",
                    "turnCodigo": "integer",
                },
            },
            "alerts": {
                "pregnantMinor": "boolean",
                "pregnantWithoutControls": "boolean",
                "lackOfHygiene": "boolean",
                "lackOfCares": "boolean",
                "sexualAbuse": "boolean",
                "childAbuse": "boolean",
                "withoutFamilySupport": "boolean",
                "dysfunctionalFamily": "boolean",
                "withoutAdherence": "boolean",
                "chronicPalliative": "boolean",
                "domesticAccident": "boolean",
                "withoutDNI": "boolean",
                "probableConsumption": "boolean",
                "probablyPsychiatric": "boolean",
                "attemptedSuicide": "boolean",
                "foodTreatment": "boolean",
                "conductDisorder": "boolean",
                "posttraumaticStress": "boolean",
                "autolyticBehaviors": "boolean",
                "disability": "boolean",
                "absentFather": "boolean",
                "scarceSymbolicResources": "boolean",
                "abandonment": "boolean",
                "genderViolence": "boolean",
                "migrants": "boolean",
                "withoutTreatmentAdherence": "boolean",
                "lowLevelAlarms": "boolean",
                "housingProblem": "boolean",
                "insufficientFinancialResources": "boolean",
                "lawConflicts": "boolean",
                "familyDisorganization": "boolean",
                "littleNeonatologyPresence": "boolean",
                "teenageMother": "boolean",
                "streetSituation": "boolean",
                "deadFetus": "boolean",
                "deceasedBaby": "boolean",
            },
        }

        return all_person_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
