from query_builder.app.handlers.company_query_builder import CompanyQueryBuilder



ROUTES = [
    (r"/v1/company_query_builder[/]?", CompanyQueryBuilder)
]
