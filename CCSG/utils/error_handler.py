class StatementGeneratorError(Exception):
    """Base exception class for statement generator errors"""
    pass

class DatabaseError(StatementGeneratorError):
    """Exception raised for database errors"""
    pass

class DataProcessingError(StatementGeneratorError):
    """Exception raised for data processing errors"""
    pass

class TemplateError(StatementGeneratorError):
    """Exception raised for template errors"""
    pass

class PDFGenerationError(StatementGeneratorError):
    """Exception raised for PDF generation errors"""
    pass

class ValidationError(StatementGeneratorError):
    """Exception raised for validation errors"""
    pass

def handle_error(error, logger=None):
    """
    Handle and log errors
    
    Args:
        error: The error exception
        logger: Optional logger object
    
    Returns:
        Dictionary with error information
    """
    error_info = {
        'type': error.__class__.__name__,
        'message': str(error),
        'handled': True
    }
    
    if logger:
        logger.error(f"{error_info['type']}: {error_info['message']}")
    
    return error_info
