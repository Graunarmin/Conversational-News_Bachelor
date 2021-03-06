import csv
import json
import sys


# --------- STATIC FUNCTIONS -----------
def sort_snippets(sorted_by_audio_id):
    """
    get an audiochunk that has the appropriate length and
    sort the snippets according to their id
    """
    for audio_id in sorted_by_audio_id:
        # get the first chunk that has 20 or more snippets
        if 15 <= len(sorted_by_audio_id[audio_id]) <= 55:
            # and sort them according to their snippet_id
            return sorted(sorted_by_audio_id[audio_id].items())


# --------------- CLASS -----------------
class TestData:
    """
    Create a test dataset for testing ways to punctate as accurate as possible.
    20 Snippets from 10 Shows
    """

    def __init__(self, shownames, data, outfile):
        self.csv_file = shownames
        self.show_names = []
        self.get_show_names()

        self.data_file = data
        self.out_file = outfile
        self.data = self.read_show_data()

        self.show_content = {}
        self.test_data = {}

    def get_show_names(self):
        """
        read in the csv-file to create a list of all relevant show names
        """

        with open(self.csv_file, 'r') as csv_file:
            show_reader = csv.reader(csv_file, delimiter=';')

            for row in show_reader:
                self.show_names.append(row[0])

    def read_show_data(self):
        """
        read in the data file line by line,
        processing each line before loading the next one
        """
        with open(self.data_file) as file:
            return json.load(file)

    def create_dataset(self):
        """
        create a dataset of theses shows with chunks of about 20 - 40 Snippets
        """
        for show in self.data:
            if show in self.show_names:
                self.add_show(show, self.data[show])
        self.write_json()

    def add_show(self, show, content):
        """
        add the given show and an appropriate audichunk to the output data
        """
        sorted_by_audio_id = {}
        # sorted_by_audio_id =
        #   {audio_id_1:{snippet_id_1:snippet_1, snippet_id_2:snippet_2}, audio_id_2:{...},...}
        for snippet in content:
            audio_chunk_id = content[snippet].split("/")
            audio_id = "/".join(audio_chunk_id[:len(audio_chunk_id) - 2])
            time = audio_chunk_id[len(audio_chunk_id) - 2]
            snippet_id = int(audio_chunk_id[len(audio_chunk_id) - 1])

            if audio_id in sorted_by_audio_id:
                sorted_by_audio_id[audio_id][snippet_id] = snippet
            else:
                sorted_by_audio_id[audio_id] = {}
                sorted_by_audio_id[audio_id][snippet_id] = snippet

        self.test_data[show] = sort_snippets(sorted_by_audio_id)

    def write_json(self):
        print("writing")
        with open(self.out_file, 'w') as outfile:
            json.dump(self.test_data, outfile, indent=2)


# --------------- MAIN -----------------
def main():
    """
    Argument 1: csv file that contains all relevant show names (../data/TestData_news-shows.csv)
    Argument 2: json file that contains all the data (../bigData/news_snippets.json)
    Argument 3: outfile name
    """

    test_data = TestData(sys.argv[1], sys.argv[2], sys.argv[3])
    test_data.create_dataset()


if __name__ == '__main__':
    main()