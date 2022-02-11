import spira.all as spira

from spira.technologies.mit import devices as dev
from spira.technologies.mit.process.database import RDD


class JunctionCircuit(spira.Circuit):
    """ Circuit containing only a single JJ connected to two ports. """

    p1 = spira.Parameter(fdef_name='create_p1')
    p2 = spira.Parameter(fdef_name='create_p2')

    jj1 = spira.Parameter(fdef_name='create_junction')

    def create_p1(self):
        midpoint = self.jj1.ports['P3_M6'] + [-5, 0]
        return spira.Port(name='Pt1_M6', midpoint=midpoint, orientation=0, width=1)

    def create_p2(self):
        midpoint = self.jj1.ports['P1_M6'] + [5, 0]
        return spira.Port(name='Pt2_M6', midpoint=midpoint, orientation=180, width=1)

    def create_junction(self):
        jj = dev.Junction()
        return spira.SRef(jj, midpoint=(0, 0))

    def create_elements(self, elems):
        elems += self.jj1

        jj_p1 = self.jj1.ports['P3_M6'].copy(width=self.p1.width)
        elems += spira.RouteStraight(p1=self.p1, p2=jj_p1, layer=RDD.PLAYER.M6.METAL)

        jj_p2 = self.jj1.ports['P1_M6'].copy(width=self.p2.width)
        elems += spira.RouteStraight(p1=self.p2, p2=jj_p2, layer=RDD.PLAYER.M6.METAL)

        return elems

    def create_ports(self, ports):
        ports += [self.p1, self.p2]
        return ports


if __name__ == '__main__':

    D = JunctionCircuit()

    D.gdsii_view()
    # D.gdsii_output(file_name='JunctionCircuit')

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=D)
    # v_model.view_virtual_connect()

    # from spira.yevon.filters.boolean_filter import ElectricalAttachFilter
    # D = ElectricalAttachFilter()(D)

    # D.netlist_view()


