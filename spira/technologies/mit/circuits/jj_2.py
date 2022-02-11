import spira.all as spira

from spira.technologies.mit import devices as dev
from spira.technologies.mit.process.database import RDD


class JunctionCircuit(spira.Circuit):

    p1 = spira.Parameter(fdef_name='create_p1')
    p2 = spira.Parameter(fdef_name='create_p2')

    jj1 = spira.Parameter(fdef_name='create_jj1')
    jj2 = spira.Parameter(fdef_name='create_jj2')

    def create_p1(self):
        return spira.Port(name='Pt1_M6', midpoint=(-15, 0), orientation=0, width=1)

    def create_p2(self):
        return spira.Port(name='Pt2_M6', midpoint=(15, 0), orientation=180, width=1)

    def create_jj1(self):
        jj = dev.Junction()
        S = spira.SRef(jj)
        S.distance_alignment(port='P1_M6', destination=self.p1, distance=5)
        return S

    def create_jj2(self):
        jj = dev.Junction()
        S = spira.SRef(jj)
        S.distance_alignment(port='P3_M6', destination=self.p2, distance=-5)
        return S

    def create_elements(self, elems):
        elems += self.jj1
        elems += self.jj2

        jj_p1 = self.jj1.ports['P1_M6'].copy(width=self.p1.width)
        elems += spira.RouteStraight(p1=self.p1, p2=jj_p1, layer=RDD.PLAYER.M6.METAL)

        jj_p2 = self.jj2.ports['P3_M6'].copy(width=self.p2.width)
        elems += spira.RouteStraight(p1=self.p2, p2=jj_p2, layer=RDD.PLAYER.M6.METAL)

        elems += spira.RouteStraight(
            p1=self.jj1.ports['P3_M6'].copy(width=1),
            p2=self.jj2.ports['P1_M6'].copy(width=1),
            layer=RDD.PLAYER.M6.METAL)

        return elems

    def create_ports(self, ports):
        ports += [self.p1, self.p2]
        return ports


if __name__ == '__main__':

    D = JunctionCircuit()

    # D = D.expand_transform()
    # D = D.expand_flat_copy()

    # D.gdsii_output()

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=D)
    # v_model.view_virtual_connect()

    from spira.yevon.filters.boolean_filter import ElectricalAttachFilter
    D = ElectricalAttachFilter()(D)

    D.netlist_view()


