from documentprocessor.text_cleaner import clean_text_as_string


def main():
    with open('/home/rivi/merged_trec/merged_trec') as input_file:
        with open('/home/rivi/clean_trec', 'w') as output_file:
            for line in input_file:
                output_file.write(clean_text_as_string(line))


if __name__ == '__main__':
    main()
