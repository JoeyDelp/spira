import spira.all as spira
from spira.yevon.geometry.route.routes import RouteStraight


from spira.technologies.mit import devices as dev
from spira.technologies.mit.process import RDD


__all__ = ['Junction']


def metal_box(elems, layer=RDD.PLAYER.M6.METAL, margin=0):
    box_shape = elems.bbox_info.bounding_box(margin)
    return spira.Polygon(shape=box_shape, layer=layer)


class __Junction__(spira.Cell):
    """ Base class for Junction PCell. """

    radius = spira.NumberParameter()
    width = spira.NumberParameter(doc='Shunt resistance width')
    c5r = spira.Parameter(fdef_name='create_c5r')


class I5Contacts(__Junction__):
    """ Cell that contains all the vias of the bottom halve of the Junction. """

    sky_via = spira.BoolParameter(default=False)
    block_margin = spira.NumberParameter(default=0)

    def get_instances(self):
        group = spira.Group()
        via_i5 = spira.SRef(reference=dev.ViaI5())
        via_c5r = spira.SRef(reference=dev.ViaC5RS())

        if self.sky_via is True:
            w = (via_i5.reference.width + 4*RDD.I6.I5_MIN_SURROUND)
            via_i6 = spira.SRef(reference=dev.ViaI6(width=w, height=w), midpoint=via_i5.midpoint)
            via_c5r.connect(port=via_c5r.ports['E0_R5'], destination=via_i6.ports['E2_M6'], ignore_process=True)
            group += via_i6
        else:
            via_c5r.connect(port=via_c5r.ports['E0_R5'], destination=via_i5.ports['E2_M5'], ignore_process=True)

        group += via_i5
        group += via_c5r

        return group

    def create_elements(self, elems):
        elems += self.get_instances()
        box_shape = elems.bbox_info.bounding_box(self.block_margin)
        elems += spira.Polygon(shape=box_shape, layer=RDD.PLAYER.M6.METAL)
        return elems

    def create_ports(self, ports):
        group = self.get_instances()
        ports += group.elements[1].ports['E2_M5'].copy(name='P2_M5')
        ports += group.elements[2].ports['E2_R5'].copy(name='P2_R5')
        return ports


class J5Contacts(__Junction__):
    """ Cell that contains all the vias of the top halve of the Junction. """

    j5 = spira.Parameter(fdef_name='create_j5')

    def create_j5(self):
        jj = dev.JJ(width=2*self.radius)
        D = spira.SRef(jj, midpoint=(0,0))
        return D

    def create_c5r(self):
        # via = dev.ViaC5RA(width=self.width)
        via = dev.ViaC5RS()
        V = spira.SRef(via)
        V.connect(port=V.ports['E0_R5'], destination=self.j5.ports['E0_M5'], ignore_process=True)
        return V

    def create_elements(self, elems):
        elems += self.j5
        elems += self.c5r
        elems += metal_box(elems)
        return elems

    def create_ports(self, ports):
        ports += self.j5.ports['E0_M5'].copy(name='P0_M5')
        ports += self.c5r.ports['E2_R5'].copy(name='P2_R5')
        return ports


class Junction(spira.Device):

    block_margin = spira.NumberParameter(default=0)

    text_type = spira.NumberParameter(default=91)

    length = spira.NumberParameter(default=1.5, doc='Length of the shunt resistance.')

    width = spira.NumberParameter(
        default=RDD.R5.MIN_SIZE,
        restriction=spira.RestrictRange(lower=RDD.R5.MIN_SIZE, upper=RDD.R5.MAX_WIDTH),
        doc='Width of the shunt resistance.')

    radius = spira.NumberParameter(
        default=RDD.J5.MIN_SIZE,
        restriction=spira.RestrictRange(lower=RDD.J5.MIN_SIZE, upper=RDD.J5.MAX_SIZE),
        doc='Radius of the circular junction layer.')

    i5 = spira.Parameter(fdef_name='create_i5_cell')
    j5 = spira.Parameter(fdef_name='create_j5_cell')

    # FIXME: This implementation can be upgraded.
    gnd_via = spira.BoolParameter(default=False)
    sky_via = spira.BoolParameter(default=False)

    def create_i5_cell(self):
        D = I5Contacts(width=self.width, radius=self.radius, sky_via=self.sky_via)
        S = spira.SRef(D)
        S.move(midpoint=S.ports['P2_R5'], destination=(0, self.length))
        return S

    def create_j5_cell(self):
        D = J5Contacts(width=self.width, radius=self.radius)
        S = spira.SRef(D)
        S.move(midpoint=S.ports['P2_R5'], destination=(0,0))
        return S

    def create_elements(self, elems):

        elems += self.i5
        elems += self.j5

        elems += RouteStraight(
            p1=self.i5.ports['P2_R5'].copy(width=self.width),
            p2=self.j5.ports['P2_R5'].copy(width=self.width),
            layer=RDD.PLAYER.R5.METAL)

        # m5_block = metal_box(elems, layer=RDD.PLAYER.M5.METAL, margin=0.1)
        # elems += m5_block

        # if self.gnd_via is True:
        #     i4 = dev.ViaI4()
        #     elems += spira.SRef(i4, midpoint=m5_block.center)

        return elems

    # def create_ports(self, ports):
    #     ports += self.j5.ports['E0_M6'].copy(name='P0_M6')
    #     ports += self.j5.ports['E1_M6'].copy(name='P1_M6')
    #     ports += self.j5.ports['E3_M6'].copy(name='P3_M6')
    #     ports += self.i5.ports['E1_M6'].copy(name='P4_M6')
    #     ports += self.i5.ports['E2_M6'].copy(name='P5_M6')
    #     ports += self.i5.ports['E3_M6'].copy(name='P6_M6')
    #     return ports


if __name__ == '__main__':

    cell = spira.Cell(name='Junction', doc='Contains all the implemented junction devices.')

    T = spira.Rotation(0)

    j1 = Junction(pcell=False)
    # j1 = Junction(pcell=False, sky_via=True, gnd_via=True)

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=j1.expand_flat_copy())
    # v_model.view_virtual_connect()

    j1.gdsii_output()
    # # j1.netlist_view()

    # from spira.yevon.vmodel.virtual import virtual_connect
    # vmodel = virtual_connect(device=j1)
    # vmodel.view_virtual_connect()

    # -----------------------------------------------------------------

    # cell += spira.SRef(reference=j1, transformation=T)
    # cell += spira.SRef(reference=mask_cell)

    # # j2 = Junction(length=1.5)
    # # cell += spira.SRef(j2, midpoint=(5, 0), transformation=T)

    # # j3 = Junction(width=1.2)
    # # cell += spira.SRef(j3, midpoint=(10, 0), transformation=T)

    # # j4 = Junction(radius=1.2)
    # # cell += spira.SRef(j4, midpoint=(15,0), transformation=T)

    # # j5 = Junction(gnd_via=True)
    # # cell += spira.SRef(j5, midpoint=(20,0), transformation=T)

    # # j6 = Junction(sky_via=True)
    # # cell += spira.SRef(j6, midpoint=(25,0), transformation=T)

    # # j7 = Junction(gnd_via=True, sky_via=True)
    # # cell += spira.SRef(j7, midpoint=(30,0), transformation=T)

    # print(Junction.length.__doc__)
    # print(Junction.width.__doc__)
    # print(Junction.radius.__doc__)

    # cell.gdsii_output()

    # -----------------------------------------------------------------

    # mask_cell = spira.Cell(name='MaskCell')
    # process_cell = spira.Cell(name='ProcessLayerCell')
    # contact_cell = spira.Cell(name='ContactLayerCell')

    # for k1 in RDD.VIAS.keys:
    #     V = RDD.VIAS[k1].PCELLS.DEFAULT(
    #         bot_layer=RDD.VIAS[k1].LAYER_STACK['BOT_LAYER'],
    #         top_layer=RDD.VIAS[k1].LAYER_STACK['TOP_LAYER'],
    #         via_layer=RDD.VIAS[k1].LAYER_STACK['VIA_LAYER'],
    #     )
    #     j1 = label_vias(
    #         symbol=k1,
    #         cell=j1,
    #         process_cell=process_cell,
    #         contact_cell=contact_cell,
    #         mapping=V.clayer_map
    #     )

    # for e in process_cell.elements:
    #     mask_cell += e
    # mask_cell += spira.SRef(reference=contact_cell)

    # j1 = add_contact_ports(D=j1, contact_cell=contact_cell)

    # nets = j1.nets(lcar=1)
    # g_cell = nets.disjoint()
    
    # from spira.yevon.utils.netlist import combine_net_nodes
    # g_cell = combine_net_nodes(g=g_cell, algorithm='d2d')
    # g_cell = combine_net_nodes(g=g_cell, algorithm='s2s')

    # j1.plotly_netlist(G=g_cell, graphname='metal', labeltext='id')










