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

Prosodic was built by [Ryan Heuser](https://github.com/quadrismegistus), [Josh Falk](https://github.com/jsfalk), and [Arto Anttila](https://web.stanford.edu/~anttila/). [Sam Bowman](https://github.com/sleepinyourhat) has contributed to the codebase as well, adding several new metrical constraints.

Prosodic supports Python ≥ 3.9

For more information on Prosodic itself, visit the [official GitHub repository](https://github.com/quadrismegistus/prosodic).

---

## Setup

### Mac
#### 1. Install Xcode Command Line Tools
Open a new terminal window and run:  
`xcode-select --install`

#### 2. Install Homebrew
Install [Homebrew](https://brew.sh) if not already installed.

#### 3. Install Python, Build Tools, and Espeak via Homebrew
In a terminal window, run:  
`brew install python make gcc espeak`

#### 4. Clone or Download prosodic-tool
To clone prosodic-tool to your machine, run:  

`cd [Path to where you want the folder to live]`    
`git clone https://github.com/LiamMSmith/prosodic-tool.git`    
`cd prosodic-tool`  

You can also download prosodic-tool manually:  
1. Go to https://github.com/LiamMSmith/prosodic-tool  
2. Click the green `Code` button → `Download ZIP`  
3. Unzip the folder, then navigate to it in Terminal.

#### 5. Set up and run the Parse
In a terminal window, run the following:

`cd [PATH to your prosodic-tool folder]`    
`python3 -m venv prosodic-tool`    
`source prosodic-tool/bin/activate`    
`python parse.py`  

If you want to run the parser multiple times in one session, just run:  
`python parse.py` again after saving your changes to `settings.txt`.

#### 6. Close the virtual environment
When you're done, run:  
`deactivate`

#### 7. Future Runs
Now you're all set up! Next time you want to use prosodic-tool, you can skip most of the steps above and do the following:  

Navigate to your prosodic-tool folder and activate a virtual environment:  
`cd [PATH to your prosodic-tool folder]`    
`source prosodic-tool/bin/activate`  

Edit your `settings.txt` file to your liking, save it, and run:  
`python parse.py`

You can repeat running the file as many times as you like with `python parse.py`, then when you finish run `deactivate`.

### Windows
#### 1. Install Ubuntu
Install Ubuntu by following the directions in the video [here](https://www.youtube.com/watch?v=X-DHaQLrBi8)

#### 2. Clone or Download prosodic-tool
In an Ubuntu window, run the following commands:

`cd [Path to where you want the folder to live]`    
`git clone https://github.com/LiamMSmith/prosodic-tool.git`    
`cd prosodic-tool`

If you don’t have Git installed or prefer to download manually:

1. Go to https://github.com/LiamMSmith/prosodic-tool  
2. Click the green `Code` button → `Download ZIP`  
3. Unzip the folder somewhere on your computer  
4. In Ubuntu, navigate to it using the `/mnt/c/...` path format, e.g.:

`cd /mnt/c/Users/YourName/Downloads/prosodic-tool`

#### 3. Install the necessary packages
In an Ubuntu window, run the following commands:

`sudo apt update`    
`sudo add-apt-repository universe`    
`sudo apt install -y python3 python3-pip python3-venv build-essential espeak`    
`cd [PATH to your prosodic-tool folder]`    
`python3 -m venv prosodic-tool`  

#### 4. Run the Parse
Any time you want to run the program, open an Ubuntu window and run:

`cd [PATH to your prosodic-tool folder]`    
`source prosodic-tool/bin/activate`    
`python parse.py`  

If you want to run the parse file multiple times in one session, you can just run:  
`python parse.py` again after saving your changes to the settings file.

When you're finished, run `deactivate` to exit the virtual environment.

---

## Pre-Processing Data
prosodic-tool has a few features detailed below to make processing your texts easier. Any other pre-processing must be done manually.

### Automatic Pre-Processing
#### Malformed Text
prosodic-tool automatically cleans your text to avoid errors. This includes skipping lines that include non-english words, unknown characters, links, and other unreadable text. At the end of a parse, prosodic-tool will report how many lines were skipped due to malformed content.

#### Lineation
Multi-sentence text will be split into new lines at every full stop character `.`, `?`, `!`, `;`, `[`, and `]`. The setting `respect_new_lines` splits text into lines based on line breaks (used for analyzing verse) when `True`. 

### Custom Pre-Processing Settings

#### File Types
prosodic-tool can accept text in multiple different formats. Multi-sentence text can be input directly into settings.txt or processed via a `.txt`, `.xlsx`, or `.csv` file.

`.txt`: Can contain one or multiple lines of text.

`.csv` and `.xlsx`: Can contain one or multiple lines of text in each cell of the first column (excluding the first row which is considered a title row)

#### Syllable and Window Manipulation
Users are able to customize the parse by building a sentence window to analyze. Users have access to the following three settings to do this:

`min_syllables`: The minimum number of syllables needed for a line to be included. This allows you to filter out short sentences to keep them from affecting your analyses.

`max_syllables`: The maximum number of syllables needed for a line to be included. This allows you to filter out long sentences to keep them from affecting your analyses.

`window`: Allows you decide if you want to analyze the beginning, middle, or end of a given line. This allows you to explore how meter changes depending on what window of a sentence is analyzed.

---

## ⚙️ Settings

All settings are defined in the `settings.txt` file and control how the input text is parsed, filtered, and exported. Users DO NOT need to edit the `parse.py` file at all to change settings. Users can simply change the values in the `settings.txt` file, save the changes, and then run the `parse.py` file. If you would like to leave comments in your `settings.txt` file, any lines you add starting with '#' won't cause any issues. If you accidentally delete lines or are encountering errors from your `settings.txt`, you can always copy the file again from GitHub and start fresh.

Below is a full list of available settings, grouped by category.


### 📝 Input

| Setting           | Description                                                                 | Possible Values                      |
|-------------------|-----------------------------------------------------------------------------|--------------------------------------|
| `text`            | Input text directly. Supports multiple lines.                               | Any text. e.g. "When forty winters shall besiege thy brow" |
| `input_file`      | Path to a `.txt`, `.csv`, or `.xlsx` file for input.                          | e.g., `input.txt`, `poems.xlsx`, etc.      |
| `verse` | Whether to consider a line break as a new line (recommended for verse).     | `True`, `False`                      |


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
| `meter`     | Only include parses that match a specific foot type.                   | `None`, `iambic`, `trochaic`, `dactylic`, or `anapestic` |
| `pentameter`| If `True`, only include parses with exactly 5 stress peaks.            | `True`, `False`                  |


### 🧠 Sentence Processing Preferences

| Setting          | Description                                                                  | Possible Values              |
|------------------|------------------------------------------------------------------------------|------------------------------|
| `min_syllables`  | Minimum number of syllables required for a line to be considered.            | Positive Integer or 0          |
| `max_syllables`  | Maximum number of syllables allowed before cropping the line.                | Positive Integer       |
| `window`         | Which part of the sentence to parse if it exceeds `max_syllables`.            | `beginning`, `middle`, or `end` |
| `resolve_optionality` | Determines whether optional syllables are resolved before parsing.     | `True`, `False`              |
| `exhaustive`     | Includes harmonically bounded parses.              | `True`, `False`              |


### 📤 Output

| Setting          | Description                                                                 | Possible Values |
|------------------|-----------------------------------------------------------------------------|-----------------|
| `output_file`    | Path to the file where parsed output will be saved.                         | e.g., `output.csv` |
| `include_sums`   | Include sum columns for each constraint per sentence.                       | `True`, `False` |
| `MU`             | Include the number of parses per sentence.                                  | `True`, `False` |
| `MTS`            | Include the total number of constraint violations per sentence.             | `True`, `False` |
| `collapse_parses`| Only keep the single best parse per sentence (lowest violation count).      | `True`, `False` |
| `include_norms`  | Include normalized constraint violation values.                             | `True`, `False` |

---

## Running prosodic-tool
Once you have your `settings.txt` file configured (remember to save it), now you're ready to run your parse.

### 1. Navigate to your folder
In your terminal/command prompt, navigate to your prosodic-tool folder. If you downloaded the folder and unzipped it, the command will look something like:
`cd Users/[username]/Downloads/prosodic-tool`. If your prosodic-tool is not in your Downloads folder, you can replace 'Downloads' with whatever folder it is in.

### 2. Activate the Virtual Environment
Run `source prosodic-tool/bin/activate` to activate your virtual environment.

### 3. Run parse
In the same terminal, run `python parse.py`. You can optionally include an output file name in the command (ie. `python parse.py output.csv`) or specify the output in the settings.txt file.

### 4. Verify output
Your terminal will output the number of lines processed, total parses, and the number of skipped lines (due to syllable constraints). It will also specify which file the output was written to. You can verify that these details are what you expected.

### 5. Repeat!
You can continue to update the `settings.txt` file as many times as you like, then run `python parse.py` again to run on the updated settings. 

### 5. Deactivate your Virtual Environment
When you're finished, run `deactivate` to exit the virtual environment.

## Updating prosodic-tool
If there are updates to prosodic-tool and you cloned the repository, you can run the commands below to pull the updates:

`git fetch origin`  
`git checkout origin/main -- README.md parse.py`

## ⚙️ Questions?
If you run into any issues, feel free to email lsmith23 [at] alumni [dot] stanford [dot] edu

