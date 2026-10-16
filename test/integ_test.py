import unittest
import flow_draw.batch.batch as batch

import flow_draw.manual_operation as manuop

class Test_00000_manuop_test(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def test_00000(self):
        manuop.main()
        # batch_this = batch.Batch()
        # print("(・_・) Select an option.")
        # print(" 1: Generate a batch input form.")
        # print(" 2: Load the batch input form.")
        # print(" 3: Generate material data input form(s).")
        # print(" 4: Load the material data and generate process JSON Schema files.")
        # print(" 5: Load process input JSON files.")
        # print(' ☕ or "quit": Quit the programme.')

        # user_input = input("Your input:")
        # match user_input:
        #     case '1':
        #         batch_this.generate_outline_form()
        #     case '2':
        #         batch_this.load_outline()
        #     case '3':
        #         batch_this.generate_mats_form_for_ai()
        #     case '4':
        #         batch_this.load_material_data_for_ai()
        #         batch_this.generate_process_json()
        #     case '5':
        #         print('The input file names must be "<process-name>_proc.json"')
        #         _=input()
        #         batch_this.manual_load_json()
        #     case _:
        #         print(f'☕.')

        # print('------------------------')
        # print()

def suite_integ_test():
    suite = unittest.TestSuite()

    suite.addTest(Test_00000_manuop_test('test_00000'))
    #suite.addTest(Test_30000_json_proc_output('test_30000_json_uo'))

    return suite
            


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_integ_test())
