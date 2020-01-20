class electronic_mail:
    def __init__(self, subject, body, recipients):
        self.Subject = subject
        self.Body = body
        self.Recipients = recipients
        # self.Event_id = 0 May be needed 

    def convert_to_dic(self):
    # A function takes in a custom object and returns a dictionary representation of the object.
  
    # Create the dictionary object 
        obj_dict = {}
  
    # Populate the dictionary with object properties
        obj_dict.update(self.__dict__)
  
        return obj_dict
