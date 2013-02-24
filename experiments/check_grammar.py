#coding: utf-8
import os
from metrics import f_one_score
from pymorphy import get_morph
from text_worker import SIMPLE_GRAMMAR, data_gathering_iterator, COMPLEX_GRAMMAR


right_results_list = [
    (u"open", u"source"),
    (u"open", u"development"),
    (u"useful", u"way"),
    (u"accessible", u"way"),
    (u"practical", u"experiences"),
    (u"first", u"Academy"),
    (u"annual", u"Academy"),
    (u"week-long", u"summer"),
    (u"week-long", u"program"),
    (u"educational", u"summer"),
    (u"educational", u"program"),
    (u"interactive", u"curriculum"),
    (u"collaborative", u"curriculum"),
    (u"practical", u"introduction"),
    (u"cutting-edge", u"web"),
    (u"cutting-edge", u"application"),
    (u"cutting-edge", u"Applications"),
    (u"technical", u"talks"),
    (u"other", u"students"),
    (u"social", u"activities"),
    (u"more", u"information"),
    (u"first", u"anniversary"),
    (u"former", u"Scholars"),
    (u"former", u"finalists"),
    (u"former", u"Interns"),
    (u"other", u"GLIDErs"),
    (u"remarkable", u"talk"),
    (u"day's", u"activities"),
    (u"important", u"matters"),
    (u"Next", u"Generation"),
    (u"other", u"ideas"),
    (u"other", u"happenings"),
    (u"week-long", u"summer"),
    (u'biggest', u'challenge'),
    (u'marshmallow', u'stand'),
    (u"Kelly's", u'advice'),
    (u"dynamic", u'relationships'),
    (u"powerful", u'alliances'),
    (u'mutual', u'goals'),
    (u'first', u'topic'),
    (u'Google+', u'Community'),
    (u'Google+', u'page'),
    (u'next', u'topic'),
    (u'technical', u'development'),
    (u'professional', u'development'),
    (u'other', u'CS'),
    (u'technical', u'skills'),
    (u'useful', u'information'),
    (u'more', u'girls'),
    (u'more', u'opportunity'),
    (u'more', u'girls'),
    (u'beneficial', u'activities'),
    (u'own', u'way'),
    (u'little', u'way'),
    (u'more', u'photos'),
    (u'open', u'source'),
    (u'open', u'development'),
    (u"useful", u"way"),
    (u"accessible", u"way"),
    (u"practical", u"experience"),
    (u"third", u"Camp"),
    (u"annual", u"Camp"),
    (u"current", u"freshmen"),
    (u"current", u"sophomores"),
    (u"week-long", u"summer"),
    (u"week-long", u"program"),
    (u"educational", u"summer"),
    (u"educational", u"program"),
    (u'collaborative', u'curriculum'),
    (u'practical', u'introduction'),
    (u'talented', u'students'),
    (u"technical", u"talks"),
    (u"social", u"activities"),
    (u"current", u"freshmen"),
    (u"current", u"sophomores"),
    (u"four-year", u"university"),
    (u"academic", u"records"),
    (u"demonstrated", u"passion"),
    (u"high", u"students"),
    (u"potential", u"students"),
    (u"exciting", u"program"),
    (u"fast-paced", u"program"),
    (u"interactive", u"cources"),
    (u"former", u"Campers"),
    (u"more", u"information")
]

normilized_right_result_list = [
    (u'OPEN', u'SOURCE'),
    (u'OPEN', u'DEVELOPMENT'),
    (u'USEFUL', u'WAY'),
    (u'ACCESSIBLE', u'WAY'),
    (u'PRACTICAL', u'EXPERIENCE'),
    (u'FIRST', u'ACADEMY'),
    (u'ANNUAL', u'ACADEMY'),
    (u'WEEK-LONG', u'SUMMER'),
    (u'WEEK-LONG', u'PROGRAM'),
    (u'EDUCATIONAL', u'SUMMER'),
    (u'EDUCATIONAL', u'PROGRAM'),
    (u'INTERACTIVE', u'CURRICULUM'),
    (u'COLLABORATIVE', u'CURRICULUM'),
    (u'PRACTICAL', u'INTRODUCTION'),
    (u'CUTTING-EDGE', u'WEB'),
    (u'CUTTING-EDGE', u'APPLICATION'),
    (u'CUTTING-EDGE', u'APPLICATION'),
    (u'TECHNICAL', u'TALK'),
    (u'OTHER', u'STUDENT'),
    (u'SOCIAL', u'ACTIVITY'),
    (u'MANY', u'INFORMATION'),
    (u'FIRST', u'ANNIVERSARY'),
    (u'FORMER', u'SCHOLAR'),
    (u'FORMER', u'FINALIST'),
    (u'FORMER', u'INTERN'),
    (u'OTHER', u'GLIDER'),
    (u'REMARKABLE', u'TALK'),
    (u'DAY', u'ACTIVITY'),
    (u'IMPORTANT', u'MATTER'),
    (u'NEXT', u'GENERATION'),
    (u'OTHER', u'IDEA'),
    (u'OTHER', u'HAPPENING'),
    (u'WEEK-LONG', u'SUMMER'),
    (u'BIG', u'CHALLENGE'),
    (u'MARSHMALLOW', u'STAND'),
    (u'KELLY', u'ADVICE'),
    (u'DYNAMIC', u'RELATIONSHIP'),
    (u'POWERFUL', u'ALLIANCE'),
    (u'MUTUAL', u'GOAL'),
    (u'FIRST', u'TOPIC'),
    (u'GOOGLE+', u'COMMUNITY'),
    (u'GOOGLE+', u'PAGE'),
    (u'NEXT', u'TOPIC'),
    (u'TECHNICAL', u'DEVELOPMENT'),
    (u'PROFESSIONAL', u'DEVELOPMENT'),
    (u'OTHER', u'CS'),
    (u'TECHNICAL', u'SKILL'),
    (u'USEFUL', u'INFORMATION'),
    (u'MANY', u'GIRL'),
    (u'MANY', u'OPPORTUNITY'),
    (u'MANY', u'GIRL'),
    (u'BENEFICIAL', u'ACTIVITY'),
    (u'OWN', u'WAY'),
    (u'LITTLE', u'WAY'),
    (u'MANY', u'PHOTO'),
    (u'OPEN', u'SOURCE'),
    (u'OPEN', u'DEVELOPMENT'),
    (u'USEFUL', u'WAY'),
    (u'ACCESSIBLE', u'WAY'),
    (u'PRACTICAL', u'EXPERIENCE'),
    (u'THIRD', u'CAMP'),
    (u'ANNUAL', u'CAMP'),
    (u'CURRENT', u'FRESHMAN'),
    (u'CURRENT', u'SOPHOMORE'),
    (u'WEEK-LONG', u'SUMMER'),
    (u'WEEK-LONG', u'PROGRAM'),
    (u'EDUCATIONAL', u'SUMMER'),
    (u'EDUCATIONAL', u'PROGRAM'),
    (u'COLLABORATIVE', u'CURRICULUM'),
    (u'PRACTICAL', u'INTRODUCTION'),
    (u'TALENTED', u'STUDENT'),
    (u'TECHNICAL', u'TALK'),
    (u'SOCIAL', u'ACTIVITY'),
    (u'CURRENT', u'FRESHMAN'),
    (u'CURRENT', u'SOPHOMORE'),
    (u'FOUR-YEAR', u'UNIVERSITY'),
    (u'ACADEMIC', u'RECORD'),
    (u'DEMONSTRATE', u'PASSION'),
    (u'HIGH', u'STUDENT'),
    (u'POTENTIAL', u'STUDENT'),
    (u'EXCITING', u'PROGRAM'),
    (u'FAST-PACED', u'PROGRAM'),
    (u'INTERACTIVE', u'COURCE'),
    (u'FORMER', u'CAMPER'),
    (u'MANY', u'INFORMATION')
]

morph = get_morph("../dicts/en")


def get_grammars_precision_and_recall(grammar, dir_path):
    retrieved = 0.0
    relevant = 0.0
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            path = os.path.join(root, file_name)
            for result in data_gathering_iterator(path, morph, grammar):
                for subresult in result:
                    if subresult in normilized_right_result_list:
                        relevant += 1.0
                    retrieved += 1.0

    return relevant / retrieved, relevant / len(normilized_right_result_list)


def check_grammars():
    """Проверяет, что сложная грамматика действительно лучше простой

    """
    precision_1, recall_1 = get_grammars_precision_and_recall(SIMPLE_GRAMMAR, "../tests/texts/google/")
    precision_2, recall_2 = get_grammars_precision_and_recall(COMPLEX_GRAMMAR, "../tests/texts/google/")
    f_one_1 = f_one_score(precision_1, recall_1)
    f_one_2 = f_one_score(precision_2, recall_2)
    assert f_one_1 <= f_one_2, u"Наше предположение неверно. Сложная грамматика не лучше простой"


if __name__ == "__main__":
    check_grammars()