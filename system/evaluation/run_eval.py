import sys
import os
import re

PY_INTERPRETER = "python3"

def is_output_outdated(srcs, output):
    if not os.path.exists(output):
        return True
    
    src_modify_times = list(map(os.path.getmtime, srcs))
    output_modify_time = os.path.getmtime(output)

    if all([output_modify_time > src_time for src_time in src_modify_times]):
        return False
    return True

def run_processing_scripts(scripts, datasets):
    def get_output_path(file):
        search_res = re.search("^generate_(.+?).py$", os.path.basename(file))
        dir = os.path.dirname(file)
        return os.path.join(dir, f"{search_res.group(1)}.csv")
    
    outputs = [get_output_path(script) for script in processing_scripts]
    for script, dataset, output in zip(scripts, datasets, outputs):
        if not is_output_outdated([script, dataset], output):
            print(f"{output} is already up to date")
            continue

        status = os.system(f"{PY_INTERPRETER} {script} {dataset} {output}")
        if status != 0:
            print(f"{script} failed to run")
            sys.exit(1)
    return outputs

def run_comparsion_script(reference: str, prediction: str):
    def get_output_path(ref, pred):
        dir = os.path.dirname(ref)
        ref_base = os.path.basename(ref).removesuffix('.csv')
        pred_base = os.path.basename(pred).removesuffix('.csv')
        return os.path.join(dir, f"{ref_base}_vs_{pred_base}.csv")

    dir = os.path.dirname(reference)
    script = os.path.join(dir, "compare_recommendations.py")
    output = get_output_path(reference, prediction)

    if not is_output_outdated([script, reference, prediction], output):
        print(f"{output} is already up to date")
        return output

    status = os.system(f"{PY_INTERPRETER} {script} {reference} {prediction} {output}")
    if status != 0:
        print(f"{script} failed to run")
        sys.exit(1)
    return output

def run_calculation_script(comparision_result):
    dir = os.path.dirname(comparision_result)
    script = os.path.join(dir, "calculate_mean_overlap.py")
    status = os.system(f"{PY_INTERPRETER} {script} {comparision_result}")
    if status != 0:
        print(f"{script} failed to run")
        sys.exit(1)

# check cli argument
get_search_str = lambda s: f"^.*\/?generate_{s}_from_.+?\.py$"
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
cwd = os.path.join(dir, os.pardir)
os.chdir(cwd)
eval_dir = os.path.basename(dir)
processing_scripts = [os.path.join(eval_dir, os.path.basename(path)) for path in sys.argv[1:]]

dataset_dir = os.path.join("datasets", "original", "articles")
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