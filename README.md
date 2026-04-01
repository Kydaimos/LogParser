# LogParser - Enhanced Log Analysis Tool

A Python script that parses text files to search for specific keywords in columns and provides comprehensive analysis including pie charts.

## Features

- 🔍 **Keyword Search**: Search for specific keywords in any column
- 📊 **Complete Analysis**: Analyze ALL unique entries when no keyword provided
- 🎯 **Flexible Modes**: Keyword search, complete analysis, or grouped analysis
- 🥧 **Pie Chart Visualization**: Visual representation of keyword distribution
- 🚀 **Auto-detection**: Automatically detects file delimiters (tab, comma, pipe, space)
- 📈 **Statistics**: Shows counts, percentages, and rankings
- � **Enhanced Charts**: Pie charts with clear outlines and readable percentage labels

## Installation

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:
   ```bash
   pip install matplotlib
   ```

## Usage

### Command Line Mode

```bash
python LogParser.py <file_path> <column_index> [keyword] [delimiter] [--group]
python LogParser.py <file_path> <column_index> --all [delimiter]
```

**Parameters:**
- `file_path`: Path to your text file
- `column_index`: Column to search (0-based indexing)
- `keyword`: Keyword to search for (optional - if omitted, analyzes all entries)
- `delimiter`: Optional delimiter (auto-detected if not specified)

**Options:**
- `--all`: Analyze all unique entries in the column (no keyword filtering)
- `--group`: Group all entries containing the keyword together (instead of separate entries)

**Examples:**
```bash
# Search for "ERROR" in column 1 (log level)
python LogParser.py sample_log.txt 1 ERROR

# Analyze ALL entries in column 1 (log levels) - no keyword needed
python LogParser.py sample_log.txt 1

# Explicitly analyze all entries with --all flag
python LogParser.py sample_log.txt 1 --all

# Analyze all message types in column 3
python LogParser.py sample_log.txt 3 --all

# Search with grouping - groups all "connection" related messages together
python LogParser.py sample_log.txt 3 connection --group

# Search for "user123" in column 3 with tab delimiter
python LogParser.py logfile.txt 3 user123 "\t"

# Search for "database" in column 2 with custom delimiter
python LogParser.py data.txt 2 database "|"
```

### Interactive Mode

Run without arguments for interactive mode:
```bash
python LogParser.py
```

The script will prompt you for:
- File path
- Column index
- Keyword to search (or leave empty to analyze all entries)
- Delimiter (optional)
- Grouping option (for keyword searches)

## Analysis Modes

### 1. **Keyword Search Mode**
Search for specific keywords in your data:
```bash
python LogParser.py sample_log.txt 1 ERROR
```
- Shows how many times "ERROR" appears
- Displays percentage vs total logs
- Highlights your keyword in results

### 2. **Complete Analysis Mode** 
Analyze ALL unique entries (no keyword needed):
```bash
python LogParser.py sample_log.txt 1        # No keyword = analyze all
python LogParser.py sample_log.txt 1 --all  # Explicit --all flag
```
- Shows frequency of every unique value in the column
- Perfect for data exploration
- Reveals patterns you might not know about

### 3. **Grouped Analysis Mode**
Group related entries together:
```bash
python LogParser.py sample_log.txt 3 connection --group
```
- Groups all "connection" related messages as one category
- Useful for high-level pattern analysis

## Output Features

### 1. Target Keyword Analysis
- Shows specific matches for your search term
- Displays count and percentage
- Lists matching lines with line numbers

### 2. Complete Column Analysis
- **All Keywords Summary**: Lists all unique keywords found
- **Top 20 Display**: Shows most common keywords with statistics
- **Ranking System**: Ranks keywords by frequency
- **Target Highlighting**: Marks your search keyword with ★

### 3. Visual Pie Chart
- Interactive pie chart showing keyword distribution
- Highlights your target keyword in red
- Shows top 10 keywords to avoid clutter
- Displays both count and percentage

## Sample Data Format

The script works with various delimited text files:

**CSV/txt Format:**
```
timestamp,level,module,message
2026-04-01 10:00:01,INFO,database,Connection established
2026-04-01 10:00:05,ERROR,authentication,Login failed
```

**Tab-delimited:**
```
2024-01-01 10:30:45	INFO	User login successful	user123
2024-01-01 10:31:12	ERROR	Database connection failed	system
```

**Pipe-delimited:**
```
INFO|User login successful|user123|192.168.1.100
ERROR|Database connection failed|system|192.168.1.50
```

## Column Indexing

Remember that column indexing is **0-based**:
- Column 0: First column
- Column 1: Second column  
- Column 2: Third column
- etc.

## Example Output

### Keyword Search Example:
```
==================================================
Log Parser Results - Target Keyword Analysis
==================================================
Keyword searched: 'ERROR'
Column index: 1
Delimiter used: ','
Grouping mode: Separate entries

📊 KEYWORD vs TOTAL LOGS COMPARISON:
──────────────────────────────────────────────────
Target keyword occurrences: 6
Total log entries processed: 47
Keyword-to-total ratio: 6/47
Target keyword percentage: 12.77%
Non-matching logs: 41 (87.23%)

============================================================
All Keywords Analysis (Column Summary)
============================================================
Total unique keywords found: 5
Total keyword occurrences: 47

Top 20 Keywords:
------------------------------------------------------------
Rank   Keyword                        Count      Percentage
------------------------------------------------------------
1      INFO                           18         38.3      %
→ 2    ERROR                          6          12.8      % ★
3      WARNING                        6          12.8      %
4      DEBUG                          3          6.4       %
5      CRITICAL                       3          6.4       %
```

### Complete Analysis Example:
```
==================================================
Log Parser Results - All Entries Analysis
==================================================
Search target: 'ALL ENTRIES'
Column index: 2
Delimiter used: ','

📊 COMPLETE COLUMN ANALYSIS:
──────────────────────────────────────────────────
Total unique entries: 5
Total log entries processed: 47
Coverage: 47/47 entries analyzed
Coverage percentage: 100.00%

Top 20 Keywords:
------------------------------------------------------------
Rank   Keyword                        Count      Percentage
------------------------------------------------------------
1      database                       12         25.5      %
2      authentication                 8          17.0      %
3      system                         7          14.9      %
4      network                        6          12.8      %
5      application                    3          6.4       %
```

## Troubleshooting

### Common Issues:

1. **"File not found"**: Check the file path is correct
2. **"Column index out of range"**: Verify the column exists in your data
3. **"Matplotlib not available"**: Install with `pip install matplotlib`
4. **No pie chart display**: Make sure you have a GUI environment for matplotlib

### Tips:

- Use forward slashes (`/`) in file paths on all systems
- For files with headers, they'll be included in the analysis
- Empty lines are automatically skipped
- Case-insensitive keyword matching is used
- **No keyword needed**: Just provide file and column to analyze all entries
- Use `--group` for high-level pattern analysis
- Pie charts have enhanced visibility with outlines and readable text

## Common Use Cases

### **Data Exploration:**
```bash
python LogParser.py access.log 2      # See all HTTP status codes
python LogParser.py error.log 1       # See all error levels
python LogParser.py app.log 3         # See all message types
```

### **Specific Analysis:**
```bash
python LogParser.py access.log 2 "404"         # Find 404 errors
python LogParser.py system.log 1 "CRITICAL"    # Find critical issues
python LogParser.py app.log 3 "timeout"        # Find timeout issues
```

### **Pattern Analysis:**
```bash
python LogParser.py app.log 3 "database" --group    # Group all DB-related logs
python LogParser.py error.log 3 "connection" --group # Group connection issues
```

## License

This script is open source and available for modification and distribution.
