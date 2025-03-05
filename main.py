import sys


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python script.py <input-file-path> <output-file-path>")
    else:
        user_input_file = sys.argv[1]
        user_output_file = sys.argv[2]
        if user_input_file[0] == "~":
            print(
                "Wildcard character detected on input path, please provide absolute path:"
            )
            print("/home/user/<input-file-path>")

        if user_output_file[0] == "~":
            print(
                "Wildcard character detected on output path, please provide the absolute path:"
            )
            print("/home/user/<output-file-path>")

        print(f"\nTemplate creation success\n\nTemplate path: {user_output_file}")
