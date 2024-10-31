from queries import (
    get_books_after_2001,
    count_books_by_type,
    readers_borrowed_manuals,
    get_books_by_section,
    calculate_return_deadline,
    count_publications_by_section
)

def print_formatted_results(results, headers):
    col_widths = [max(len(str(item)) for item in column) for column in zip(*results, headers)]
    
    header_row = " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers))

    # header body
    print("+-" + "-+-".join("-" * width for width in col_widths) + "-+")
    print("| " + header_row + " |")
    print("+-" + "-+-".join("-" * width for width in col_widths) + "-+")

    # table body
    for row in results:
        formatted_row = " | ".join(str(item).ljust(col_widths[i]) for i, item in enumerate(row))
        print("| " + formatted_row + " |")

    # table bottom
    print("+-" + "-+-".join("-" * width for width in col_widths) + "-+\n")

def main():
    print("Books after 2001:")
    print_formatted_results(get_books_after_2001(), ["Title"])
    
    print("Count of books by type:")
    print_formatted_results(count_books_by_type(), ["Type", "Count"])

    print("Readers who borrowed manuals:")
    print_formatted_results(readers_borrowed_manuals(), ["Last Name", "First Name"])

    print("Books in specified section:")
    section = "технічна"
    print_formatted_results(get_books_by_section(section), ["Title"])

    print("Return deadlines for borrowed books:")
    print_formatted_results(calculate_return_deadline(), ["Title", "Return Date"])

    print("Publications by section and type:")
    print_formatted_results(count_publications_by_section(), ["Section", "Type", "Count"])

if __name__ == "__main__":
    main()
