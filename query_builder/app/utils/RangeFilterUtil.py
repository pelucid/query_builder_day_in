import re

from query_builder import exceptions

class RangeFilterUtil(object):
    # Potentially make static
    def parse_arg(self, arg_name, arg_value):
        """Parser for arguments that are numerical range types.

                Takes the argument to check as an input (e.g. revenue).
                Expect an argument of the format: n-N
                Returns lower and upper bounds. Negative values are permitted.
                Returns None if parsing failed."""

        if arg_value:
            exp = re.compile("^(\-?[0-9]+)?\-(\-?[0-9]+)?$")
            m = re.search(exp, arg_value)
            if not m:
                raise exceptions.ParameterValueError(key=arg_name, value=arg_value)

            lbound, ubound = None, None
            # Parse lower bound
            if m.group(1):
                try:
                    lbound = int(m.group(1))
                except ValueError:
                    raise exceptions.ParameterValueError(key=arg_name, value=arg_value)

            # Parse upper bound
            if m.group(2):
                try:
                    ubound = int(m.group(2))
                except ValueError:
                    raise exceptions.ParameterValueError(key=arg_name, value=arg_value)

            if lbound is not None and ubound is not None and lbound > ubound:
                raise exceptions.ParameterValueError(key=arg_name, value=arg_value)

            return {"gte": lbound, "lte": ubound}
        else:
            return {}