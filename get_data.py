import os
import sys
import codecs
import getopt

sys.path.insert(0, os.path.abspath('.'))

from utils.get_property_data import *

def usage():
    print("-------------------------------------------------------------------------")
    print("get_data.py [options]")
    print("-------------------------------------------------------------------------")
    print("Options:")
    print("-------------------------------------------------------------------------")
    print("    -f|--file_name     the path\\file_name of the file with property ids,")
    print("                       without .txt extension")
    print("    -h|--help")
    print("-------------------------------------------------------------------------")

if __name__ == "__main__":
    try:
        options, tmp = getopt.getopt(sys.argv[1:], "f:h", ["file_name=","help"])
        if len(options) == 0:
            usage()
            sys.exit(-1)

        file_name = None

        for opt, arg in options:
            if opt in ["-f", "--file_name"]:
                file_name = arg
            elif opt in ["-h", "--help"]:
                print("\n-------------------------------------------------------------------------")
                print(" USAGE: get_data.py -f <path\\file_name>")
                print("-------------------------------------------------------------------------")
                sys.exit(-1)


        # scrape properties data
        immo_data = scrape_properties(file_name)

        # save results in a json file
        output_file = save_to_json(file_name)

        print(f"Check {output_file} for scraped data...")

    except getopt.GetoptError:
        usage()
        sys.exit(-1)