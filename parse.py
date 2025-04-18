import subprocess
import sys
import os

def install_if_missing(package_name, import_name=None):
    import_name = import_name or package_name
    try:
        __import__(import_name)
    except ImportError:
        print(f"📦 Installing missing package: {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Install required packages if missing
install_if_missing("pandas")
install_if_missing("prosodic")
install_if_missing("re")
install_if_missing("collections")

import pandas as pd
import prosodic
import re
from collections import defaultdict

ALL_CONSTRAINTS = [
    "w_stress",
    "s_unstress",
    "unres_within",
    "unres_across",
    "w_peak",
    "s_trough",
    "foot_size"
]

# Function to read and process settings.txt
def read_input_file(filename):
    settings = {}
    constraints = []

    constraint_keys = {
        "w_stress", "s_unstress", "unres_within", "foot_size", "unres_across", "s_trough", "w_peak"
    }

    int_keys = {"max_s", "max_w", "min_syllables", "max_syllables"}
    bool_keys = {
        "exhaustive", "resolve_optionality", "verse", "pentameter",
        "include_sums", "MU", "MTS", "collapse_parses", "include_norms", *constraint_keys
    }
    str_keys = {"text", "input_file", "window", "output_file", "meter"}

    valid_window_values = {"beginning", "middle", "end"}
    all_keys = int_keys | bool_keys | str_keys

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()

        if not line or line.startswith("#"):
            i += 1
            continue

        if line.startswith("text ="):
            text_value = raw_line.partition("text =")[2].lstrip()
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if any(next_line.startswith(k + " =") for k in all_keys):
                    break
                text_value += lines[i]
                i += 1
            text_value = text_value.rstrip("\n")
            settings["text"] = None if text_value.strip().lower() == "none" else text_value
            continue

        if "=" not in line:
            raise ValueError(f"[Line {i+1}] Missing '=' in line: {raw_line.strip()}")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key not in all_keys:
            raise ValueError(f"[Line {i+1}] Unrecognized key '{key}'. Check for typos or unsupported setting.")

        if key in settings:
            raise ValueError(f"[Line {i+1}] Duplicate key '{key}' found. Each setting should be defined only once.")

        if key in bool_keys:
            if value.lower() not in ("true", "false"):
                raise ValueError(f"[Line {i+1}] Value for '{key}' must be True or False.")
            value_bool = value.lower() == "true"
            if key in constraint_keys and value_bool:
                constraints.append(key)
            value = value_bool

        elif key in int_keys:
            if not value.isdigit():
                raise ValueError(f"[Line {i+1}] Value for '{key}' must be an integer.")
            value = int(value)

        elif key in str_keys:
            value = None if value.lower() == "none" else value.strip()
            if key == "window" and value and value not in valid_window_values:
                raise ValueError(f"[Line {i+1}] Invalid value for 'window': '{value}'. Must be one of: beginning, middle, end.")

        settings[key] = value
        i += 1

    settings["constraints"] = tuple(constraints)
    return settings


def process_text(settings):
    text = settings.get("text")
    file_path = settings.get("input_file")

    min_syllables = settings.get("min_syllables", 0)
    max_syllables = settings.get("max_syllables", None)
    window = settings.get("window", "beginning")

    def split_into_sentences(text_block):
        if settings.get("verse", False):
            split_pattern = r'[\n]+'
        else:
            split_pattern = r'[.?!;\[\]]+'
        lines = re.split(split_pattern, text_block)
        return [line.strip() for line in lines if line.strip()]

    # --- Load lines_to_parse ---
    if text:
        lines_to_parse = split_into_sentences(text)

    elif file_path:
        _, ext = os.path.splitext(file_path)

        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            lines_to_parse = split_into_sentences(raw_text)

        elif ext in [".csv", ".xlsx"]:
            df = pd.read_csv(file_path) if ext == ".csv" else pd.read_excel(file_path)
            first_col_texts = df.iloc[:, 0].dropna().astype(str).tolist()
            lines_to_parse = []
            for cell in first_col_texts:
                lines_to_parse.extend(split_into_sentences(cell))

        else:
            raise ValueError(f"Unsupported file format: {ext}")

    else:
        raise ValueError("❌ Both 'text' and 'file' are None. Please provide input in settings.txt.")

    processed_lines = []
    skipped_count = 0
    for line in lines_to_parse:
        print(line)

    for i, original_line_text in enumerate(lines_to_parse):
        # Tokenize the line into words (alphanumeric + apostrophes)
        word_tokens = re.findall(r"\b[\w’']+\b", original_line_text)

        # Create a TextModel for each word and get syllable counts
        syllable_counts = []
        skip_line = False

        for word in word_tokens:
            if word.lower() in {"http", "https", "www"}:
                continue
            try:
                model = prosodic.TextModel(txt=word).wordtype1
                if model.num_sylls is None:
                    skip_line = True
                    print(f"⚠️ Skipping line due to unknown word (no syllables): '{word}' in → {original_line_text}")
                    break
                syllable_counts.append(model.num_sylls)
            except Exception as e:
                print(f"⚠️ Skipping line due to error with word '{word}': {e} → {original_line_text}")
                skip_line = True
                break

        if skip_line:
            skipped_count += 1
            continue
        syllable_count = sum(syllable_counts)

        if syllable_count < min_syllables:
            skipped_count += 1
            continue

        if max_syllables and syllable_count > max_syllables:
            # Use syllable_counts and word_tokens directly — both in sync
            def get_window_indices(counts, max_sylls, mode):
                if mode == "beginning":
                    end_idx = 0
                    syll_sum = 0
                    while end_idx < len(counts) and syll_sum < max_sylls:
                        syll_sum += counts[end_idx]
                        end_idx += 1
                    return 0, end_idx

                elif mode == "end":
                    start_idx = len(counts)
                    syll_sum = 0
                    while start_idx > 0:
                        start_idx -= 1
                        syll_sum += counts[start_idx]
                        if syll_sum >= max_sylls:
                            break
                    return start_idx, len(counts)

                elif mode == "middle":
                    total = sum(counts)
                    mid_target = total // 2
                    start = 0
                    accum = 0
                    while start < len(counts) and accum + counts[start] <= mid_target:
                        accum += counts[start]
                        start += 1
                    left = start
                    right = start
                    syll_sum = 0
                    while (left > 0 or right < len(counts)):
                        if left > 0:
                            left -= 1
                            syll_sum += counts[left]
                        if syll_sum >= max_sylls:
                            break
                        if right < len(counts):
                            syll_sum += counts[right]
                            right += 1
                        if syll_sum >= max_sylls:
                            break
                    return left, right

                else:
                    raise ValueError("Invalid window setting. Options are beginning, middle, or end.")

            start_idx, end_idx = get_window_indices(syllable_counts, max_syllables, window)
            selected_words = word_tokens[start_idx:end_idx]
            new_line_text = ' '.join(selected_words)
        else:
            new_line_text = ' '.join(word_tokens)
        
        processed_lines.append((i + 1, original_line_text, new_line_text))

    if not processed_lines:
        raise ValueError("❌ No lines met the max and min syllable criteria. Adjust min_syllables or check input text.")

    return processed_lines, skipped_count


def run_parse(settings, output_csv):
    lines_to_parse, skipped_count = process_text(settings)
    all_rows = []
    meter_filter = settings.get("meter", None)
    pentameter = settings.get("pentameter", False)

    for input_index, original_line, processed_line in lines_to_parse:
        text_obj = prosodic.TextModel(processed_line)
        if not settings.get("exhaustive", False):
            try:
                parsed_obj = text_obj.parse(
                    max_s=settings.get("max_s", 2),
                    max_w=settings.get("max_w", 2),
                    constraints=settings.get("constraints", ()),
                    resolve_optionality=settings.get("resolve_optionality", True),
                    exhaustive=settings.get("exhaustive", False)
                )
            except AssertionError:
                print(f"⚠️ Skipping line due to empty parse: {processed_line}")
                continue
        else:
            meter = prosodic.Meter(
                max_s=settings.get("max_s", 2),
                max_w=settings.get("max_w", 2),
                constraints=settings.get("constraints", ()),
                resolve_optionality=settings.get("resolve_optionality", True)
            )
            try:
                parsed_obj = [meter.parse_exhaustive(text_obj)]
            except Exception as e:
                print(f"⚠️ Skipping line (exhaustive parse error): {processed_line} → {e}")
                continue

        for parselist in parsed_obj:
            for parse in parselist:
                # 🛑 Skip if meter is set and parse doesn't match
                if meter_filter and parse.foot_type != meter_filter:
                    continue
                
                if pentameter and parse.num_peaks != 5:
                    continue

                parsed_line = parse.line or prosodic.Line(processed_line)
                resd = parse.stats_d()
                # html = parsed_line.to_html(parse=parse, blockquote=False, as_str=True, tooltip=True)

                row = [
                    input_index,
                    getattr(getattr(parsed_line, "stanza", None), "num", ""),
                    getattr(parsed_line, "num", ""),
                    original_line,
                    parse.parse_rank,
                    parse.txt,
                    parse.meter_str,
                    parse.stress_str,
                    round(resd.get("*total", -1), 1),
                    int(sum(v for k, v in resd.items() if k.startswith("*"))),
                    round(resd.get("ambig", 0), 1),
                    parse.num_sylls,
                    len(parse.wordtokens),
                ] + [
                    int(resd.get(f"*{c}", 0)) for c in ALL_CONSTRAINTS
                ] + [
                    round(resd.get(f"*{c}_norm", 0), 2) for c in ALL_CONSTRAINTS
                ] + [
                    processed_line
                ]

                row = ['' if x is None else x for x in row]
                all_rows.append(row)

    # Header construction
    base_cols = [
        "input_index", "stanza_num", "line_num", "line_txt", "parse_rank",
        "parse_txt", "parse_meter", "parse_stress",
        "parse_score", "parse_num_viols",
        "parse_ambig", "parse_num_sylls", "parse_num_words"
    ]
    constraint_cols = [f"*{c}" for c in ALL_CONSTRAINTS]
    norm_constraint_cols = [f"{c}_norm" for c in constraint_cols]
    header = base_cols + constraint_cols + norm_constraint_cols + ["source_text"]

    final_df = pd.DataFrame(all_rows, columns=header)

    # Get unique line_texts that contributed to parses
    parsed_lines_count = len(set(row[-1] for row in all_rows))

    print(f"✅ Parsed {parsed_lines_count} line(s) → {len(all_rows)} parse(s) total, skipped {skipped_count} line(s).")
    return final_df



def process_output(df, settings):
    from collections import defaultdict

    df = df.copy()
    constraint_cols = [col for col in df.columns if col.startswith("*")]

    # --- MU (number of parses) ---
    if settings.get("MU"):
        df["MU"] = df.groupby("source_text")["input_index"].transform("count")

    # --- MTS (sum of all violations) ---
    if settings.get("MTS"):
        df["MTS"] = df.groupby("input_index")["parse_score"].transform("sum").astype(int)
    
    
    # --- collapse_parses (keep only best parse per sentence) ---
    if settings.get("collapse_parses"):
        # Collapse to the best-ranked parse (lowest parse_rank)
        df = df.loc[df.groupby("input_index")["parse_rank"].idxmin()].reset_index(drop=True)

        # Assign parse_id = input_index (as string, 1-indexed)
        df["parse_id"] = (df["input_index"]).astype(str)

        # Drop parse_rank column (no longer meaningful post-collapse)
        df = df.drop(columns=["parse_rank"], errors="ignore")

    else:
        # parse_id = input_index + .1, .2, .3 etc.
        df["parse_id"] = df["input_index"].astype(str) + "." + df["parse_rank"].astype(str)

    # --- include_sums ---
    if settings.get("include_sums"):
        for col in constraint_cols:
            sum_col = f"{col}_sum"
            df[sum_col] = df.groupby("source_text")[col].transform("sum")

        # --- Reorder *_sum columns next to their base columns ---
        cols = df.columns.tolist()
        new_col_order = []
        sum_cols = [col for col in df.columns if col.endswith("_sum")]

        for col in cols:
            if col.endswith("_sum"):
                continue  # we will place it next to its base column
            new_col_order.append(col)
            sum_col = f"{col}_sum"
            if sum_col in sum_cols:
                new_col_order.append(sum_col)
                sum_cols.remove(sum_col)

        # Append any leftover columns
        for col in cols:
            if col not in new_col_order:
                new_col_order.append(col)

        df = df[new_col_order]

    # --- Remove unwanted columns ---
    cols_to_remove = [
        "stanza_num", "line_num", "parse_ambig", "parse_is_bounded",
        "*total_sylls", "*total_sylls_sum", "*total", "*total_sum", 
        "*total_sylls_norm", "source_text", "*total_sylls_norm_sum", 
        "*total_norm", "*total_norm_sum", "*foot_size", "*foot_size_sum"
    ]
    df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors="ignore")

    # --- Remove *_norm and *_norm_sum columns if include_norms is False ---
    if not settings.get("include_norms", True):  # Default to True if not specified
        norm_cols_to_remove = [
            "*w_stress_norm", "*w_stress_norm_sum",
            "*s_unstress_norm", "*s_unstress_norm_sum",
            "*unres_within_norm", "*unres_within_norm_sum",
            "*foot_size_norm", "*foot_size_norm_sum",
            "*unres_across_norm", "*unres_across_norm_sum",
            "*w_peak_norm", "*w_peak_norm_sum",
            "*s_trough_norm", "*s_trough_norm_sum"
        ]
        df = df.drop(columns=[col for col in norm_cols_to_remove if col in df.columns], errors="ignore")

    # --- Reorder so parse_id is the first column ---
    if "parse_id" in df.columns:
        cols = df.columns.tolist()
        cols.insert(0, cols.pop(cols.index("parse_id")))
        df = df[cols]

    if "parse_id" in df.columns:
        # Split parse_id into two numeric parts (even if collapsed, it works)
        parse_parts = df["parse_id"].str.split(".", expand=True)

        # Always treat the first part as input_index
        df["_input_index"] = parse_parts[0].astype(int)

        # If there's a second column, use it as parse rank
        if parse_parts.shape[1] > 1:
            df["_parse_rank"] = parse_parts[1].astype(int)
        else:
            df["_parse_rank"] = 0  # default for collapsed parses

        # Sort by input_index then parse rank
        df = df.sort_values(by=["_input_index", "_parse_rank"]).reset_index(drop=True)

        # Drop the helper columns
        df = df.drop(columns=["_input_index", "_parse_rank", "input_index"])


    return df


def main(cmd_output_file=None):
    # Read settings from settings.txt
    settings = read_input_file("settings.txt")

    # Determine output file
    output_file = (
        cmd_output_file or
        settings.get("output_file") or
        "output.csv"
    )

    # Ensure pandas displays all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # Run parser
    parsed_df = run_parse(settings, output_file)

    # Process output
    processed_df = process_output(parsed_df, settings)

    # Ensure output file exists or is created
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            pass

    # Write output based on file extension
    _, ext = os.path.splitext(output_file)
    ext = ext.lower()

    if ext == ".xlsx":
        processed_df.to_excel(output_file, index=False)
    elif ext == ".csv":
        processed_df.to_csv(output_file, index=False)
    else:
        raise ValueError("Unsupported file extension. Please use '.csv' or '.xlsx'.")

    print(f"📁 Output written to: {output_file}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)