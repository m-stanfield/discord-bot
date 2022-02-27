from logger import Logger


if __name__ == "__main__":
    logger = Logger(__name__)



    logger.info("Start reading Database")
    records = {"john": 55, "tom": 66}
    logger.debug("Records: %s", records)
    logger.info("Updating records ...")
    logger.info("Finish updating records")
    logger.error("Error Test")
