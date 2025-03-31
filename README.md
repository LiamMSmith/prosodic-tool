# Prosodic Research Tool

This project is a research-oriented extension of [Prosodic](https://github.com/quadrismegistus/prosodic), designed to simplify and scale its use for analyzing poetic meter in large text datasets.

The tool adds features to make Prosodic easier to use for linguistic and literary research, including:

- Processing large volumes of text from `.txt`, `.csv`, or `.xlsx` files  
- Analyzing sentence windows by beginning, middle, or end based on syllable constraints  
- Customizing output with meter filtering, parse collapsing, and Metrical Tension Sum
- Pre-processing the text to filter out unrecognized words

---

### About Prosodic

**Prosodic** is a metrical-phonological parser written in Python. It currently supports English and Finnish, with the option to add other languages via pronunciation dictionaries or custom Python functions.

This version, Prosodic 2.x, is a near-total rewrite of the original project. Prosodic was built by [Ryan Heuser](https://github.com/quadrismegistus), [Josh Falk](https://github.com/jsfalk), and [Arto Anttila](https://web.stanford.edu/~anttila/). [Sam Bowman](https://github.com/sleepinyourhat) has contributed to the codebase as well, adding several new metrical constraints.

Prosodic supports Python ≥ 3.9

For more information on Prosodic itself, visit the [official GitHub repository](https://github.com/quadrismegistus/prosodic).

---

## ⚙️ Settings

All settings are defined in the `settings.txt` file and control how the input text is parsed, filtered, and exported. Users DO NOT need to edit the parse.py file at all to change settings. Below is a full list of available options, grouped by category.


### 📝 Input

| Setting           | Description                                                                 | Possible Values                      |
|-------------------|-----------------------------------------------------------------------------|--------------------------------------|
| `text`            | Input text directly. Supports multiple lines.                               | Any text. e.g. "When forty winters shall besiege thy brow" |
| `input_file`      | Path to a `.txt`, `.csv`, or `.xlsx` file for input.                          | e.g., `input.txt`, `poems.xlsx`, etc.      |
| `respect_new_lines` | Whether to consider a line break as a new line (recommended for verse).     | `True`, `False`                      |


### 🎼 Metrical Constraints

| Setting         | Description                                                              | Possible Values |
|-----------------|--------------------------------------------------------------------------|-----------------|
| `w_stress`      | Disallows weak positions from being stressed.                            | `True`, `False` |
| `s_unstress`    | Disallows strong positions from being unstressed.                        | `True`, `False` |
| `unres_within`  | Disallows unresolved stress clashes within a foot.                       | `True`, `False` |
| `unres_across`  | Disallows unresolved stress clashes across foot boundaries.              | `True`, `False` |
| `s_trough`      | Disallows strong positions from being troughs in pitch contour.          | `True`, `False` |
| `w_peak`        | Disallows weak positions from being peaks in pitch contour.              | `True`, `False` |


### 👣 Foot Constraints

| Setting     | Description                                                      | Possible Values |
|-------------|------------------------------------------------------------------|-----------------|
| `max_s`     | Maximum number of strong positions per foot.                     | Positive Integer |
| `max_w`     | Maximum number of weak positions per foot.                       | Positive Integer |
| `foot_size` | Disallow meter positions that exceed two syllables or are empty. | `True`, `False` |


### 📏 Meter Filters

| Setting     | Description                                                            | Possible Values                  |
|-------------|------------------------------------------------------------------------|----------------------------------|
| `meter`     | Only include parses that match a specific foot type.                   | `None`, `iambic`, `trochaic`, 'dactylic', or 'anapestic' |
| `pentameter`| If `True`, only include parses with exactly 5 stress peaks.            | `True`, `False`                  |


### 🧠 Sentence Processing Preferences

| Setting          | Description                                                                  | Possible Values              |
|------------------|------------------------------------------------------------------------------|------------------------------|
| `min_syllables`  | Minimum number of syllables required for a line to be considered.            | Positive Integer or 0          |
| `max_syllables`  | Maximum number of syllables allowed before cropping the line.                | Positive Integer       |
| `window`         | Which part of the sentence to crop if it exceeds `max_syllables`.            | `beginning`, `middle`, or `end` |
| `resolve_optionality` | Determines whether optional syllables are resolved before parsing.     | `True`, `False`              |
| `exhaustive`     | Use an exhaustive parsing algorithm (slower but more complete).              | `True`, `False`              |


### 📤 Output

| Setting          | Description                                                                 | Possible Values |
|------------------|-----------------------------------------------------------------------------|-----------------|
| `output_file`    | Path to the file where parsed output will be saved.                         | e.g., `output.csv` |
| `include_sums`   | Include sum columns for each constraint per sentence.                       | `True`, `False` |
| `MU`             | Include the number of parses per sentence.                                  | `True`, `False` |
| `MTS`            | Include the total number of constraint violations per sentence.             | `True`, `False` |
| `collapse_parses`| Only keep the single best parse per sentence (lowest violation count).      | `True`, `False` |
| `include_norms`  | Include normalized constraint violation values.                             | `True`, `False` |
