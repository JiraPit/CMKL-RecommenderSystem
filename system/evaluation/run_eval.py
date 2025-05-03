import sys
import os
import re

PY_INTERPRETER = "python3"

def run_processing_scripts(scripts, datasets):
    def get_output_path(file):
        search_res = re.search("^generate_(.+?).py$", os.path.basename(file))
        dir = os.path.dirname(file)
        return os.path.join(dir, f"{search_res.group(1)}.csv")
    
    outputs = [get_output_path(script) for script in processing_scripts]
    for script, dataset, output in zip(scripts, datasets, outputs):
        if os.system(f"{PY_INTERPRETER} {script} {dataset} {output}") != 0:
            print(f"{script} failed to run")
            sys.exit(1)
    return outputs

def run_comparsion_script(reference: str, prediction: str):
    def get_output_path(ref, pred):
        dir = os.path.dirname(ref)
        ref_base = os.path.basename(ref).removesuffix('.csv')
        pred_base = os.path.basename(pred).removesuffix('.csv')
        return os.path.join(dir, f"{ref_base}_vs_{pred_base}.csv")

    compare_script = "compare_recommendations.py"
    output = get_output_path(reference, prediction)
    if os.system(f"{PY_INTERPRETER} {compare_script} {reference} {prediction} {output}") != 0:
        print(f"{compare_script} failed to run")
        sys.exit(1)
    return output

def run_calculation_script(comparision_result):
    calc_script = "calculate_mean_overlap.py"
    if os.system(f"{PY_INTERPRETER} {calc_script} {comparision_result}") != 0:
        print(f"{calc_script} failed to run")
        sys.exit(1)

# check cli argument
get_search_str = lambda s: f"^generate_{s}_from_.+?\.py$"
script_types = ["ref", "pred"]
if len(sys.argv) != 3:
    print(f"{__file__} <generate_ref_file> <generate_pred_file>")
    sys.exit(1)
for file, type in zip(sys.argv[1:], script_types):
    if not os.path.exists(file):
        print(f"file {file} not found")
        sys.exit(1)
    if not re.search(get_search_str(type), file):
        print(f"file {file} has to have format {get_search_str(type)}")
        sys.exit(1)

dir = os.path.dirname(sys.argv[0])
processing_scripts = [os.path.join(dir, script) for script in sys.argv[1:]]

# print(os.getcwd(), __file__, dir)

dataset_dir = os.path.join(os.pardir, "datasets", "original", "articles")
dataset_filenames = ["user-item-interactions.csv", "articles_community.csv"]
dataset_paths = [os.path.join(dataset_dir, f) for f in dataset_filenames]

# Check if datasets exist
for path in dataset_paths:
    if not os.path.exists(path):
        print(f"file {path} not found")

# Run processing files and check if failed
res = run_processing_scripts(processing_scripts, dataset_paths)
res = run_comparsion_script(*res)
run_calculation_script(res)




