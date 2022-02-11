import spira.all as spira
from spira.lrc.rules import __DoubleLayerDesignRule__


RDD = spira.get_rule_deck()


class Overlap(__DoubleLayerDesignRule__):
    minimum = param.FloatParameter()

    def __repr__(self):
        return 'Rule surround: min={}'.format(self.minimum)

    def apply(self, elems):
        pass
