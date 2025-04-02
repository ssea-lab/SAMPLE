class GetPrompts():
    def __init__(self):
        self.prompt_task = ("Design a scoring function to evaluate the pre-deployed microservices for each edge server.\
        In each step, the edge server deploys the microservice with the highest score.\
        The final goal is to let the edge servers handle as many corresponding tasks as possible.")
        self.prompt_func_name = "score"
        self.prompt_func_inputs = ['ES', 'PDM']
        self.prompt_func_outputs = ['PDMS']
        self.prompt_inout_inf = ("'ES' represents the detailed information of the edge server stored of dictionary type,\
        including the geographical 'location'(includes the longitude and the latitude in a list type), 'radius'(indicates the coverage radius in floating-point type), 'resource'(represents existing resources in a list type, which includes three elements), and 'ADM'(includes the indices of already-deployed microservices in a list type).\
        'PDM' represents the pre-deployed microservices of above edge server of list type, of list type, and it contains data in dictionary type\
        which includes 'location'(longitude and latitude of user request), 'M'(microservice index in a integer type), 'A'(pending assignment index in a integer type), and 'MC'(the consumpution of microservices in a list type).\
        'PDMS' represents the sequence obtained by sorting 'PDM' in descending order of scores.")
        self.prompt_other_inf = "The novel function should be sufficiently complex in order to achieve better performance. It is important to ensure self-consistency."

    def get_task(self):
        return self.prompt_task
    
    def get_func_name(self):
        return self.prompt_func_name
    
    def get_func_inputs(self):
        return self.prompt_func_inputs
    
    def get_func_outputs(self):
        return self.prompt_func_outputs
    
    def get_inout_inf(self):
        return self.prompt_inout_inf

    def get_other_inf(self):
        return self.prompt_other_inf

