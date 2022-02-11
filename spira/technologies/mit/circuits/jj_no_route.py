import spira.all as spira
from spira.yevon.geometry.route.routes import RouteStraight

from spira.technologies.mit import devices as dev
from spira.technologies.mit.process.database import RDD


class Jcc(spira.Circuit):
    """ Junction Connection Circuit consists of a simple Josephson
    junction, connected to two ports via a metal layer path. """

    p1 = spira.Parameter(fdef_name='create_p1')
    p2 = spira.Parameter(fdef_name='create_p2')

    jj1 = spira.Parameter(fdef_name='create_junction')

    def create_p1(self):
        midpoint = self.jj1.ports['P3_M6'] + [-5, 0]
        return spira.Port(name='P1_M6', midpoint=midpoint, orientation=0, width=1)

    def create_p2(self):
        midpoint = self.jj1.ports['P1_M6'] + [5, 0]
        return spira.Port(name='P2_M6', midpoint=midpoint, orientation=180, width=1)

    def create_junction(self):
        jj = dev.Junction(pcell=True)
        return spira.SRef(jj, midpoint=(0, 0))

    def create_structures(self, elems):
        elems += self.jj1
        return elems

    def create_routes(self, elems):

        elems += spira.Rectangle(p1=(-5,-3), p2=(-0.9,-0.8), layer=RDD.PLAYER.M6.METAL)
        elems += spira.Rectangle(p1=(1,-3), p2=(5,-0.8), layer=RDD.PLAYER.M6.METAL)

        return elems

    def create_ports(self, ports):
        ports += [self.p1, self.p2]
        return ports


if __name__ == '__main__':

    jj = Jcc(pcell=True)

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=jj.expand_flat_copy())
    # v_model.view_virtual_connect()

    jj.gdsii_output()
    # jj.netlist_view()


