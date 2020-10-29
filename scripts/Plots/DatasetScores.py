import pandas as pd
import ast
import Helpers as hp
import json


class DatasetScores:

    def __init__(self, scorefile, jsonfile):
        self.scores = pd.read_csv(scorefile)

        with open(jsonfile, 'r', encoding='utf-8') as data_json:
            dictionary = json.load(data_json)

        self.total_docs = dictionary['stats']['total_docs']
        self.total_markers = dictionary['stats']['total_markers']
        self.different_markers = dictionary['stats']['different_markers']
        self.total_sb = dictionary['stats']['total_sb']
        self.total_sm = dictionary['stats']['total_sm']
        self.total_se = dictionary['stats']['total_se']
        self.total_db = dictionary['stats']['total_db']
        self.total_dm = dictionary['stats']['total_dm']
        self.total_de = dictionary['stats']['total_de']
        self.marker_dict = dictionary['marker']

        del dictionary

    def get_total_dm_count_statistics(self):
        """
        Computes the min, mean, max of the total number of DM per Text
        :return: a list of [min, a_mean, h_mean, median, mode, max] values
        """
        return hp.compute_statistics(self.scores['dm_count_doc'].dropna())

    def get_percent_dm_count_statistics(self):
        """
        Computes the min, mean, max of the percentage share that the DM
        have in a text
        :return: a list of [min, a_mean, h_mean, median, mode, max] values
        """
        return hp.compute_statistics(self.scores['dm_words_perc'].dropna())

    def get_total_dm_sentences_statistics(self):
        """
        Computes the min, mean, max of the total number of sentences
        that contain at least one DM per Text
        :return: a list of [min, a_mean, h_mean, median, mode, max] values
        """
        return hp.compute_statistics(self.scores['dm_sentences'].dropna())

    def get_percent_dm_sentences_statistics(self):
        """
        Computes the min, mean, max of the percentage share that sentences
        containing at least one DM have of a text
        :return:
        """
        return hp.compute_statistics(self.scores['dm_sentences_perc'].dropna())

    def get_total_dm_per_sentence_statistics(self):
        """
        Computes the min, mean, max of dm per sentence per text
        :return:
        """
        return hp.compute_statistics(self.get_sentence_counts())

    def get_total_dm_positions_sentence(self):
        """
        Computes the total number of DM at the beginning, the middle and the end
        of a sentence
        :return: a list [count_begin, count_middle, count_end]
        """
        return [sum(self.scores['dm_pos_sent_begin'].dropna()),
                sum(self.scores['dm_pos_sent_middle'].dropna()),
                sum(self.scores['dm_pos_sent_end'].dropna())]

    def get_percent_dm_positions_sentence(self):
        """
        Computes the perceantage share of dm that stand in the beginning, the middle
        or the end of a sentence
        :return:
        """
        values = self.get_total_dm_positions_sentence()
        whole = sum(values)

        return [hp.percentage(values[0], whole),
                hp.percentage(values[1], whole),
                hp.percentage(values[2], whole)]

    def get_total_dm_positions_document(self):
        """
        Computes the total number of DM at the beginning, the middle and the end
        of a document
        :return: a list [count_begin, count_middle, count_end]
        """
        return [sum(self.scores['dm_pos_doc_begin'].dropna()),
                sum(self.scores['dm_pos_doc_middle'].dropna()),
                sum(self.scores['dm_pos_doc_end'].dropna())]

    def get_percent_dm_positions_document(self):
        """
        Computes the perceantage share of dm that stand in the beginning, the middle
        or the end of a document
        :return:
        """
        values = self.get_total_dm_positions_document()
        whole = sum(values)

        return [hp.percentage(values[0], whole),
                hp.percentage(values[1], whole),
                hp.percentage(values[2], whole)]

    def get_sentence_counts(self):
        """
        Returns a list of counts that indicates how many sentences in this dataset contain
        as many discourse markers.
        E.g.: if  three sentences each contain 2 DM, 2 is added to the list 3 times
        :return: a list of all the counts
        """
        values = []

        for doc in self.scores['dm_count_sent'].dropna():
            doc_counts = ast.literal_eval(doc)

            for dm_counter in doc_counts:
                sentence_counter = int(doc_counts[dm_counter])
                for i in range(sentence_counter):
                    values.append(dm_counter)

        return values

    def compute_dm_per_sentence(self):
        """
        Create two lists, one of which contains the number of dm per sentence (x)
        and the other one (y) contains the number of sentences that contain as many dms.
        :return: a list of [[x_values],[y_values]]
        """
        values = {}

        for doc in self.scores['dm_count_sent'].dropna():
            doc_counts = ast.literal_eval(doc)

            for dm_counter in doc_counts:
                if dm_counter not in values:
                    values[dm_counter] = int(doc_counts[dm_counter])
                else:
                    values[dm_counter] += int(doc_counts[dm_counter])

        # x values are the number of dms per sentence
        x_values = []
        # y values are the number of sentences that contain as many dms.
        y_values = []
        for element in sorted(values.items()):
            x_values.append(element[0])
            y_values.append(element[1])

        return [x_values, y_values]

# ------- Functionaliyt concerning the marker dictionary with the single markers

    def get_total_marker_values(self):
        """
        Creates a dictionary with the markers as keys and their total number of occurrence in this dataset as value
        :return:
        """
        markers = {}
        for marker in self.marker_dict:
            markers[marker] = self.marker_dict[marker]['total']

        return markers

    def get_total_marker_percents(self):
        """
        Creates a dictionary with the markers as keys
        and their percentage-share in all the markers in this dataset as value
        :return:
        """
        percents = {}
        for marker in self.marker_dict:
            percents[marker] = (self.marker_dict[marker]['total'] * 100) / self.total_markers

        return percents

    def get_total_marker_statistics(self):
        """
        Creates a dictionary with the markers as keys and their average number of occurences
        (a_mean, h_mean, median, mode) over all the documents in this dataset as value-dict
        :return:
        """
        statistics = {}

        for marker in self.marker_dict:
            statistics[marker] = {}
            statistics[marker]['a_mean'] = self.marker_dict[marker]['total'] / self.total_docs
            statistics[marker]['h_mean'] = self.total_docs / self.marker_dict[marker]['inverse_sum_total']
            statistics[marker]['median'] = self.marker_dict[marker]['median_total']
            statistics[marker]['mode'] = self.marker_dict[marker]['mode_total'][0]

        return statistics

    def get_markers(self):
        """
        :return: a list of all the markers in this dataset
        """
        markers = []
        for marker in self.marker_dict:
            markers.append(marker)
        return markers

    def get_all_marker_values(self, marker):
        """
        Creates a List with all the values for a marker:
        [total, a_mean, h_mean, median, mode]
        :param marker:
        :return:
        """
        if marker in self.marker_dict:
            marker_values = [#self.marker_dict[marker]['total'],
                             self.marker_dict[marker]['total'] / self.total_docs,
                             self.total_docs / self.marker_dict[marker]['inverse_sum_total'],
                             self.marker_dict[marker]['median_total'],
                             self.marker_dict[marker]['mode_total'][0][0]]
        else:
            marker_values = [0] * 4

        return marker_values

