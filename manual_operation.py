import flow_draw.batch.batch as batch

def main():
    batch_this = batch.Batch()
    while True:
        print("(・_・) Select an option.")
        print(" 1: Generate a batch input form.")
        print(" 2: Load the batch input form.")
        print(" 3: Generate material data input form(s).")
        print(" 4: Load the material data and generate process JSON Schema files.")
        print(" 5: Load process input JSON files.")
        print(" ☕: Quit the programme (not the company).")

        user_input = input("Your input:")
        match user_input:
            case '1':
                batch_this.generate_outline_form()
            case '2':
                batch_this.load_outline()
            case '3':
                batch_this.generate_mats_form_for_ai()
            case '4':
                batch_this.load_material_data_for_ai()
                batch_this.generate_process_json()
            case '5':
                print('The input file names must be "<process-name>_proc.json"')
                _=input()
                batch_this.manual_load_json()
            case '☕':
                break
            case _:
                print(f'Invalid input "{user_input}".')

        print('------------------------')
        print()



if __name__=='__main__':
    main()