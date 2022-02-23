class NotAllowedtoChangeAttributeValueError(Exception):
    """ To handle improperly attribute change attempts.
    """


class InvalidAttributeValueError(Exception):
    """ To handle invalid attribute values.
    """


class InvalidValueForOrderError(Exception):
    """ To handle invalid order values.
    """


class SPSLoadToXMLError(Exception):
    """ Generic error during SPS Package loading.
    """


class SHA1Error(Exception):
    """ To handle invalid SHA1 value.
    """


class SPSDownloadXMLError(Exception):
    """ To handle XML file download failures. 
    """


class SPSXMLLinkError(Exception):
    """ To handle invalid XML links.
    """


class SPSXMLFileError(Exception):
    """ To handle invalid XML files. 
    """


class SPSAssetOrRenditionFileError(Exception):
    """ To handle invalid Asset or Rendition files.
    """


class SPSMakePackageFromPathsMissingKeyError(Exception):
    """ To handle missing paths.
    """
