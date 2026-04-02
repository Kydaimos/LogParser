#!/usr/bin/env python3
"""
LogParser.py - A simple script to parse text files and count keyword occurrences in specific columns.

Usage:
    python LogParser.py <file_path> <column_index> [keyword] [delimiter] [--group]
    python LogParser.py <file_path> <column_index> --all [delimiter]
    python LogParser.py <file_path> <column_index>           # no keyword   = analyze all entries
    python LogParser.py                                      # no arguments = interactive mode
    
Options:
    keyword    Search for specific keyword (optional - if omitted, shows all entries)
    --all      Analyze all unique entries in the column (no keyword filtering)
    --group    Group all entries containing the keyword together (instead of separate entries)
"""

from collections import Counter
from typing import Dict
import matplotlib.pyplot as plt
import os
import sys

# --- Display constants ---
TOP_N_SUMMARY            = 20  # number of keywords shown in the summary table
MAX_MATCHES_DISPLAY      = 5   # matching lines shown in keyword search mode
MAX_ENTRIES_DISPLAY      = 10  # sample entries shown in all-entries mode
RESULTS_WIDTH            = 50  # width of the results section separators
INTERACTIVE_HEADER_WIDTH = 40  # width of the interactive mode header
RANK_COL_WIDTH           = 6   # rank column width in the summary table
COUNT_COL_WIDTH          = 10  # count column width in the summary table
DEFAULT_KW_COL_WIDTH     = 30  # fallback keyword column width when no data is present


def parse_file_for_keyword(file_path: str, column_index: int, keyword: str = None, delimiter: str = None, group_by_keyword: bool = False) -> Dict[str, any]:  # return values are mixed types (int, str, Counter, list, bool)
    """
    Parse a text file and count occurrences of a keyword in a specific column.
    Also analyzes all keywords in the column for comprehensive statistics.
    
    Args:
        file_path (str): Path to the text file
        column_index (int): Column index to search (0-based)
        keyword (str): Keyword to search for (None = analyze all entries)
        delimiter (str): Column delimiter (auto-detected if None)
        group_by_keyword (bool): If True, groups all entries containing the keyword together
    
    Returns:
        Dict containing count and other statistics including all keywords analysis
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    count = 0
    total_lines = 0
    lines_with_keyword = []
    all_keywords = []  # Store all values from the specified column
    analyze_all = keyword is None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            total_lines += 1
            
            # Auto-detect delimiter if not specified.
            # NOTE: Once set on the first non-empty line, the delimiter is locked in
            # for the rest of the file. Mixed-delimiter files are not supported.
            if delimiter is None:
                if '\t' in line:
                    delimiter = '\t'
                elif ',' in line:
                    delimiter = ','
                elif '|' in line:
                    delimiter = '|'
                else:
                    delimiter = ' '  # Default to space
            
            # Split the line into columns
            columns = line.split(delimiter)
            
            # Check if the specified column exists
            if column_index < len(columns):
                column_value = columns[column_index].strip()
                
                # Add to all keywords list for analysis
                if column_value:  # Only add non-empty values
                    if analyze_all:
                        # When analyzing all entries, just add the column value
                        all_keywords.append(column_value)
                        count += 1  # Count all entries when no keyword specified
                        lines_with_keyword.append({
                            'line_number': line_number,
                            'column_value': column_value,
                            'full_line': line
                        })
                    elif group_by_keyword and keyword.lower() in column_value.lower():
                        # Group all entries containing the keyword under one category
                        all_keywords.append(f"[GROUPED] {keyword}")
                    else:
                        # Keep original behavior - separate entries
                        all_keywords.append(column_value)
                
                # Check for keyword (case-insensitive) - only if keyword is specified
                if not analyze_all and keyword and keyword.lower() in column_value.lower():
                    count += 1
                    lines_with_keyword.append({
                        'line_number': line_number,
                        'column_value': column_value,
                        'full_line': line
                    })
    
    # Analyze all keywords in the column
    keyword_counter = Counter(all_keywords)
    
    return {
        'keyword': keyword if keyword else 'ALL ENTRIES',
        'column_index': column_index,
        'count': count,
        'total_lines': total_lines,
        'percentage': (count / total_lines * 100) if total_lines > 0 else 0,
        'matches': lines_with_keyword,
        'delimiter_used': delimiter,
        'all_keywords': keyword_counter,
        'unique_keywords': len(keyword_counter),
        'grouped_by_keyword': group_by_keyword,
        'analyze_all': analyze_all
    }


def create_pie_chart(keyword_counter: Counter, target_keyword: str, column_index: int) -> None:
    """Create a pie chart showing the distribution of all keywords in the column."""
    try:
        # Get top 10 keywords for the pie chart (to avoid cluttering)
        top_keywords = keyword_counter.most_common(10)
        
        if not top_keywords:
            print("No data available for pie chart.")
            return
        
        # Prepare data for pie chart
        labels = []
        sizes = []
        colors = list(plt.cm.Set3(range(len(top_keywords))))
        
        # Highlight the target keyword if it's in the top keywords
        for i, (keyword, count) in enumerate(top_keywords):
            labels.append(f"{keyword}\n({count})")
            sizes.append(count)
            
            # Highlight target keyword in red
            if target_keyword.lower() in keyword.lower():
                colors[i] = 'red'
        
        # Create the pie chart with proper spacing
        fig, ax = plt.subplots(figsize=(12, 10))  # Increased height for better spacing
        
        # Add more space at the top for title
        plt.subplots_adjust(top=0.85, bottom=0.1, left=0.1, right=0.9)
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                            autopct='%1.1f%%', startangle=90,
                                            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
                                            pctdistance=0.85, labeldistance=1.1)  # Push labels outward
        
        # Customize the chart with title positioned higher
        fig.suptitle(f'Keyword Distribution in Column {column_index}\n(Top 10 Keywords)', 
                        fontsize=16, fontweight='bold', y=0.95)  # Position title higher
        
        # Make percentage text more readable with better contrast
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
            # Add white background/outline for better readability
            autotext.set_bbox(dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='black'))
        
        # Style the slice labels for better readability
        for text in texts:
            text.set_fontsize(9)
            text.set_fontweight('normal')
        
        # Add legend if there are many keywords
        if len(keyword_counter) > 10:
            remaining_count = sum(count for keyword, count in keyword_counter.most_common()[10:])
            if remaining_count > 0:
                plt.figtext(0.02, 0.02, f"Note: {len(keyword_counter) - 10} other keywords with {remaining_count} total occurrences not shown", 
                            fontsize=8, style='italic')
        
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.show()
        
    except ImportError:
        print("Matplotlib not available. Install with: pip install matplotlib")
    except Exception as e:
        print(f"Error creating pie chart: {e}")


def display_keyword_summary(keyword_counter: Counter, target_keyword: str) -> None:
    """Display a summary of all keywords found in the column."""
    # Dynamically size the keyword column to fit the longest value in the top 20
    top_keywords = keyword_counter.most_common(TOP_N_SUMMARY)
    kw_col_width = max((len(kw) for kw, _ in top_keywords), default=DEFAULT_KW_COL_WIDTH)
    kw_col_width = max(kw_col_width, len("Keyword"))  # Never narrower than the header
    table_width = RANK_COL_WIDTH + kw_col_width + COUNT_COL_WIDTH + 10 + 2  # Rank + Keyword + Count + Percentage + spacing

    print(f"\n{'='*table_width}")
    print(f"All Keywords Analysis (Column Summary)")
    print(f"{'='*table_width}")
    print(f"Total unique keywords found: {len(keyword_counter)}")
    print(f"Total keyword occurrences: {sum(keyword_counter.values())}")
    
    # Calculate keyword distribution statistics
    total_occurrences = sum(keyword_counter.values())
    target_count = sum(count for keyword, count in keyword_counter.items() 
                        if target_keyword.lower() in keyword.lower())
    
    if target_count > 0:
        print(f"Target keyword represents {target_count}/{total_occurrences} entries")
        print(f"Target keyword dominance: {(target_count/total_occurrences*100):.1f}% of all entries")
    
    print(f"\nTop {TOP_N_SUMMARY} Keywords:")
    print(f"{'-'*table_width}")
    print(f"{'Rank':<{RANK_COL_WIDTH}} {'Keyword':<{kw_col_width}} {'Count':<{COUNT_COL_WIDTH}} {'Percentage'}")
    print(f"{'-'*table_width}")
    
    for i, (keyword, count) in enumerate(top_keywords, 1):
        percentage = (count / total_occurrences * 100) if total_occurrences > 0 else 0
        
        # Highlight the target keyword
        if target_keyword.lower() in keyword.lower():
            print(f"{'→ ' + str(i):<{RANK_COL_WIDTH}} {keyword:<{kw_col_width}} {count:<{COUNT_COL_WIDTH}} {percentage:.1f}% ★")
        else:
            print(f"{i:<{RANK_COL_WIDTH}} {keyword:<{kw_col_width}} {count:<{COUNT_COL_WIDTH}} {percentage:.1f}%")
    
    if len(keyword_counter) > TOP_N_SUMMARY:
        remaining = len(keyword_counter) - TOP_N_SUMMARY
        print(f"\n... and {remaining} more unique keywords")


def display_results(results: Dict) -> None:
    """Display the parsing results in a formatted way."""
    print(f"\n{'='*RESULTS_WIDTH}")
    if results.get('analyze_all', False):
        print(f"Log Parser Results - All Entries Analysis")
    else:
        print(f"Log Parser Results - Target Keyword Analysis")
    print(f"{'='*RESULTS_WIDTH}")
    print(f"Search target: '{results['keyword']}'")
    print(f"Column index: {results['column_index']}")
    print(f"Delimiter used: '{results['delimiter_used']}'")
    print(f"Grouping mode: {'Grouped by keyword' if results.get('grouped_by_keyword', False) else 'Separate entries'}")
    
    # Enhanced comparison
    if results.get('analyze_all', False):
        print(f"\n📊 COMPLETE COLUMN ANALYSIS:")
        print(f"{'─'*RESULTS_WIDTH}")
        print(f"Total unique entries: {results['unique_keywords']}")
        print(f"Total log entries processed: {results['total_lines']}")
        print(f"Coverage: {results['count']}/{results['total_lines']} entries analyzed")
        print(f"Coverage percentage: {results['percentage']:.2f}%")
    else:
        print(f"\n📊 KEYWORD vs TOTAL LOGS COMPARISON:")
        print(f"{'─'*RESULTS_WIDTH}")
        print(f"Target keyword occurrences: {results['count']}")
        print(f"Total log entries processed: {results['total_lines']}")
        print(f"Keyword-to-total ratio: {results['count']}/{results['total_lines']}")
        print(f"Target keyword percentage: {results['percentage']:.2f}%")
        print(f"Non-matching logs: {results['total_lines'] - results['count']} ({100 - results['percentage']:.2f}%)")
    
    if results['matches'] and not results.get('analyze_all', False):
        print(f"\n🔍 Matching lines for target keyword:")
        print(f"{'-'*RESULTS_WIDTH}")
        for match in results['matches'][:MAX_MATCHES_DISPLAY]:
            print(f"Line {match['line_number']}: {match['column_value']}")
        
        if len(results['matches']) > MAX_MATCHES_DISPLAY:
            print(f"... and {len(results['matches']) - MAX_MATCHES_DISPLAY} more matches")
    elif results.get('analyze_all', False):
        print(f"\n📋 Sample entries from the column:")
        print(f"{'-'*RESULTS_WIDTH}")
        for match in results['matches'][:MAX_ENTRIES_DISPLAY]:
            print(f"Line {match['line_number']}: {match['column_value']}")
        
        if len(results['matches']) > MAX_ENTRIES_DISPLAY:
            print(f"... and {len(results['matches']) - MAX_ENTRIES_DISPLAY} more entries")
    else:
        print(f"\n❌ No matches found for keyword '{results['keyword']}'")
    
    # Display comprehensive keyword analysis
    display_keyword_summary(results['all_keywords'], results['keyword'])
    
    # Ask user if they want to see the pie chart
    try:
        show_chart = input(f"\nWould you like to see a pie chart of keyword distribution? (y/n): ").strip().lower()
        if show_chart in ['y', 'yes', '1']:
            create_pie_chart(results['all_keywords'], results['keyword'], results['column_index'])
    except KeyboardInterrupt:
        print("\nSkipping pie chart display.")
    except:  # Broad catch handles non-interactive environments (piped input, redirected stdin)
        # If we can't get user input (non-interactive mode), show chart automatically
        if len(results['all_keywords']) > 1:
            create_pie_chart(results['all_keywords'], results['keyword'], results['column_index'])

def interactive_mode() -> None:
    """Run the script in interactive mode."""
    print("Log Parser - Interactive Mode")
    print("=" * INTERACTIVE_HEADER_WIDTH)
    
    # Get file path
    file_path = input("Enter the path to your text file: ").strip()
    
    # Get column index
    try:
        column_index = int(input("Enter the column index to search (0-based): "))
    except ValueError:
        print("Invalid column index. Using default: 0")
        column_index = 0
    
    # Get keyword
    keyword = input("Enter the keyword to search for (or leave empty to analyze all entries): ").strip()
    if not keyword:  # Handle empty keyword
        keyword = None
    
    # Get delimiter (optional)
    delimiter = input("Enter delimiter (press Enter for auto-detection): ").strip()
    delimiter = delimiter if delimiter else None
    
    # Ask about grouping (only meaningful when a keyword is provided; ignored in analyze-all mode)
    group_choice = input("Group all entries containing the keyword together? (y/n): ").strip().lower()
    group_by_keyword = group_choice in ['y', 'yes', '1']
    
    if group_by_keyword:
        print("✓ Will group all entries containing the keyword together")
    else:
        print("✓ Will keep separate entries for each unique message")
    
    try:
        results = parse_file_for_keyword(file_path, column_index, keyword, delimiter, group_by_keyword)
        display_results(results)
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to handle command line arguments or run interactive mode."""
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nNot enough arguments provided. Running in interactive mode...\n")
        interactive_mode()
        return
    
    file_path = sys.argv[1]
    try:
        column_index = int(sys.argv[2])
    except ValueError:
        print("Error: Column index must be an integer")
        sys.exit(1)
    
    # Check if we have a third argument and if it's a flag or keyword
    keyword = None
    delimiter = None
    group_by_keyword = False
    analyze_all = False
    
    # Process arguments starting from position 3
    args = sys.argv[3:]
    
    for i, arg in enumerate(args):
        if arg == '--group':
            group_by_keyword = True
        elif arg == '--all':
            analyze_all = True
            keyword = None  # Override any keyword when using --all
        elif keyword is None and not arg.startswith('--'):
            keyword = arg  # First non-flag argument is the keyword
        elif not arg.startswith('--'):
            delimiter = arg  # Second non-flag argument is delimiter
    
    # If no keyword provided and not explicitly using --all, analyze all entries
    if keyword is None and not analyze_all:
        analyze_all = True
        print("No keyword provided. Analyzing ALL entries in the column...")
    
    # Note: analyze_all is not passed to parse_file_for_keyword — the function derives
    # it internally from keyword being None. The local variable is used only for the
    # informational print above and the --all flag override logic.
    try:
        results = parse_file_for_keyword(file_path, column_index, keyword, delimiter, group_by_keyword)
        display_results(results)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()