from medical.medical_enums import *
from medical.organs.brain import Brain
from medical.organs.genitalia import Genitalia
from medical.organs.heart import Heart
from medical.organs.kidney import Kidney
from medical.organs.liver import Liver
from medical.organs.lung import Lung
from medical.organs.stomach import Stomach
from prototype_system.organ import OrganPrototypeLoader


async def test_Organ(logger):
    try:
        standart_info = ["1", "name", "description", 500, 100, None]
        logger.debug(Brain(*standart_info))
        logger.debug(Heart(*standart_info))
        logger.debug(Kidney(*standart_info))
        logger.debug(Liver(*standart_info))
        logger.debug(Lung(*standart_info))
        logger.debug(Stomach(*standart_info, 54))
        logger.debug(Genitalia(*standart_info, GenderEnum.FEMALE))
    except Exception as err:
        logger.debug(f"Got exception in 'test_Organ': {err}")
        return False

    return True

async def test_OrganPrototype(logger):
    try:
        prototypes = OrganPrototypeLoader("for_tests")
        for proto in prototypes.prototypes:
            logger.debug(proto)
    except Exception as err:
        logger.debug(f"Got exception in 'test_OrganPrototype': {err}")
        return False
        
    return True
