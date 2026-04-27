from flow_draw.project.process.process import Process

class Project:
    def __init__(self):
        self.list_proc: list[Process]=[]

    #TODO please implement me!
    def load_process_summary(self):



    def load_process_details(self):
        """
        Just trigger load_unitop_detail() of all items in the list self.list_proc.

        Parameters
        ---------
        None

        Returns
        ---------
        None
        """
        for p in self.list_proc:
            p.load_unitop_detail()