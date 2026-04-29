import unittest
import os
import flow_draw.definitions as defs
import flow_draw.data_io.process_io as proc_io
import flow_draw.project.process.unit_operations as uos
import flow_draw.project.process.unit_operations.charging as charging



class TestIO(unittest.TestCase):
    def setUp(self):
        self.test_proc_io = proc_io.ProcessIO(project_name="test_project", process_name="test_process", num_unit_op=1)
        self.test_proc_io.generate_proc_summary_form(uos.unit_operation.list_unit_ops)
        self.test_proc_io.generate_mats_form()
        self.test_proc_io.save_form()
        return super().setUp()
    
    def test_01_input_generation(self):
        print("expected filename: ", "test_project"+defs.inputfile_base_name+".xlsx")
        self.assertTrue(os.path.isfile("test_project"+defs.inputfile_base_name+".xlsx"))
    
    def test_02_uo_deriv_registr(self):
        self.assertIn(member=charging.Charging, container=uos.unit_operation.registry_uo_cls.values())

    def test_03_summary_form(self):
        pass


if __name__=="__main__":
    unittest.main()
