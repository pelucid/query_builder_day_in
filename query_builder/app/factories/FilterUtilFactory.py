from query_builder.app.utils.RangeFilterUtil import RangeFilterUtil

class FilterUtilFactory(object):
    filter_map = {
        "number-range": RangeFilterUtil
    }

    def get_util(self, filter_type):
        util_class = self.filter_map.get(filter_type)
        return util_class()

