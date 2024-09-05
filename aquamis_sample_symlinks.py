import os

def get_symlink_target(input_dir):
    if not os.path.exists(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist.")
        return None

    symlink_targets = {}
    for file in os.listdir(input_dir):
        if file.endswith(".fastq.gz"):
            full_path = os.path.join(input_dir, file)
            # Check if it's a symlink, if not, treat as a regular file
            orig_path = os.readlink(full_path) if os.path.islink(full_path) else full_path
            base_name = file.rsplit('_', 1)[0]
            if base_name not in symlink_targets:
                symlink_targets[base_name] = os.path.dirname(orig_path)o
    
    return symlink_targets

def write_output(symlink_targets, output_file):
    if symlink_targets is None:
        return 0

    processed_files_count = 0
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure the output directory exists
    with open(output_file, 'w') as f:
        f.write("sample\tfq1\tfq2\n")
        for sample, dir_path in symlink_targets.items():
            fq1 = os.path.join(dir_path, f"{sample}_1.fastq.gz")
            fq2 = os.path.join(dir_path, f"{sample}_2.fastq.gz")
            if os.path.exists(fq1) and os.path.exists(fq2):
                f.write(f"{sample}\t{fq1}\t{fq2}\n")
                processed_files_count += 1
    return processed_files_count

if __name__ == "__main__":
    input_dir = input("Enter the input directory path: ").strip()
    if not input_dir:
        print("No input directory provided. Exiting.")
        exit(1)

    output_dir = "/home/jmg/aquamis/samples"
    
    last_dir_name = os.path.basename(input_dir)  # Gets the last directory name
    output_filename = f"{last_dir_name}_samples.tsv"  # Use only the last directory name
    output_file = os.path.join(output_dir, output_filename)
    
    symlink_targets = get_symlink_target(input_dir)
    if symlink_targets:
        processed_files_count = write_output(symlink_targets, output_file)
        print(f"Output written to {output_file}. Successfully processed {processed_files_count} file pairs.")
    else:
        print("No .fastq.gz files found or input directory does not exist.")
