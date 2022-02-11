import spira.all as spira

from spira.yevon.geometry.line import *
from spira.yevon.geometry.vector import *

from spira.technologies.mit import devices as dev
from spira.technologies.mit.process.database import RDD


class Resistor(spira.Circuit):
    """ Resistor PCell of type Circuit between two vias connecting to layer M6. """

    length = spira.NumberParameter(default=7)

    width = spira.NumberParameter(
        default=RDD.R5.MIN_SIZE,
        restriction=spira.RestrictRange(lower=RDD.R5.MIN_SIZE),
        doc='Width of the shunt resistance.')

    via = spira.CellParameter(
        default=dev.ViaC5RS,
        restriction=spira.RestrictType([dev.ViaC5RA, dev.ViaC5RS]),
        doc='Via component for connecting R5 to M6')

    via_left = spira.Parameter(fdef_name='create_via_left')
    via_right = spira.Parameter(fdef_name='create_via_right')

    def validate_parameters(self):
        if self.length < self.width:
            raise ValueError('Length cannot be less than width.')
        return True

    def create_via_left(self):
        via = self.via(width=0.3+self.width)
        T = spira.Rotation(rotation=-90)
        return spira.SRef(via, transformation=T)

    def create_via_right(self):
        via = self.via(width=0.3+self.width)
        T = spira.Rotation(rotation=-90)
        return spira.SRef(via, midpoint=(self.length, 0), transformation=T)

    def create_elements(self, elems):

        elems += [self.via_left, self.via_right]

        elems += spira.RouteStraight(
            p1=self.via_left.ports['R5:E0'],
            p2=self.via_right.ports['R5:E2'],
            layer=RDD.PLAYER.R5.METAL)

        return elems

    def create_ports(self, ports):

        ports += self.via_left.ports['M6:E1'].copy(name='M6:P1')
        ports += self.via_left.ports['M6:E2'].copy(name='M6:P2')
        ports += self.via_left.ports['M6:E3'].copy(name='M6:P3')

        ports += self.via_right.ports['M6:E0'].copy(name='M6:P4')
        ports += self.via_right.ports['M6:E1'].copy(name='M6:P5')
        ports += self.via_right.ports['M6:E3'].copy(name='M6:P6')

        return ports


if __name__ == '__main__':

    # cell = spira.Cell(name='Toplevel')

    # c1 = Resistor()
    # cell += spira.SRef(c1, midpoint=(0, 0))

    # c2 = Resistor(length=15)
    # s2 = spira.SRef(c2, midpoint=(0, 5))
    # # s2.rotate(30)
    # cell += s2

    # c3 = Resistor(via=dev.ViaC5RA)
    # cell += spira.SRef(c3, midpoint=(0, 10))

    # c4 = Resistor(via=dev.ViaC5RA, width=1.5)
    # cell += spira.SRef(c4, midpoint=(0, 15))

    # c2.gdsii_output(file_name='Resistor')

    # ------------------------------------------------------------------

    D = Resistor(via=dev.ViaC5RA)

    D.gdsii_view()
    # D.gdsii_output(file_name='res_s')
    D.gdsii_output(file_name='res_a')

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=D)

    # v_model.view_virtual_connect(show_layers=True)
    # # v_model.view_derived_contacts()
    # # v_model.view_derived_edges()

    # # from spira.yevon.filters.boolean_filter import ElectricalAttachFilter
    # # D = ElectricalAttachFilter()(D)

    # # # D.output.view_netlist()
    # # # D.output.view_gdsii()
    # # # D.output.write_gdsii()

    # # D.netlist_view()


