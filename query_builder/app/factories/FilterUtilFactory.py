from query_builder.app.utils.RangeFilterUtil import RangeFilterUtil

class FilterUtilFactory(object):
    _filter_map = {
        "number-range": RangeFilterUtil
    }

    def get_util(self, filter_type):
        util_class = self._filter_map.get(filter_type)


        return util_class()

