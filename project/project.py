from flow_draw.project.process import process as proc

class Project:
    def __init__(self):
        self.list_proc: list[proc.Process]=[]

    #TODO please implement me!
    def load_process_summary(self):
        """
        Lets each process constituting the project load the summary data from a ProcessIO object.

        Parameters
        ------------
        None

        Returns
        ------------
        None
        """
        for proc in self.list_proc:
            proc.load_uo_summary()


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