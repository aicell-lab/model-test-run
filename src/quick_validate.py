from bioimageio.spec import validate_format, ValidationContext
from dataclasses import dataclass

@dataclass
class ValidationResult:
    success: bool
    details: str

def validate_rdf(rdf_dict, context=None):
    ctx = ValidationContext(perform_io_checks=False)
    summary = validate_format(rdf_dict, context=ctx)
    return ValidationResult(
        success=summary.status == "passed",
        details=summary.format()
    )