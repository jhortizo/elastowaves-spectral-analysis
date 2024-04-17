def parse_solution_identifier(geometry_type, params):
    "Returnss strign associated with run parameters"

    params_str = [
        str(this_key) + "_" + str(this_value).replace(".", "")
        for this_key, this_value in params.items()
    ]  # TODO: if value is 1.0, it is left as 10, which may be confusing later...

    filename = geometry_type + "-" + "-".join(params_str)

    return filename
