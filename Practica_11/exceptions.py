class ClinicError(Exception):
    pass


class NotFoundError(ClinicError):
    pass


class ValidationError(ClinicError):
    pass
