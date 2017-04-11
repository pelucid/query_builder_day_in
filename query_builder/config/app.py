class AppSettings(object):

    def __init__(self):
        self.app_settings = dict()
        self.SECTOR_ES_FIELD = 'sector.id'

        self.COMPANIES_FILTERS = [
            "revenue",
            "sector_context",
            "ecommerce",
            "limit",
            "offset",
            "cid",
            "exclude_tps",
            "cash",
            "aggregate",
            "trading_activity",
        ]

        self.app_settings["version"] = "2.19"

        # High level constants
        self.app_settings["results_limit_default"] = 500
        self.app_settings["page_size_default"] = 50

    
settings = AppSettings()
