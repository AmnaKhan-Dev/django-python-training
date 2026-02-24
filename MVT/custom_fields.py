from django.db import models  # Import Django's model module to create fields and models

# Define a custom field class from fields.CharField class that stores exactly 5-digit codes
class FiveDigitCodeField(models.CharField):
    description = "A field to store exactly 5 digit codes"  # Description of the field (useful for admin/docs)

    # Constructor for the field, called when you create it in a model
    def __init__(self, *args, **kwargs):  
        kwargs['max_length'] = 5  # Force max_length to 5 characters, overriding any user input
        super().__init__(*args, **kwargs)  # Call the parent CharField initializer with updated arguments(runs the CharField constructor with your new settings.)
    
    # This method tells Django how to serialize the field for migrations
    # Django needs to know how to recreate your field in the migration file.
    # For normal fields (like CharField), Django already knows the info (like max_length, null, default).
    # For custom fields, Django doesn’t know automatically, so it calls deconstruct() on your field.

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()  # Get the default deconstruction from CharField
        return name, path, args, kwargs  # Return info so migrations can recreate this field