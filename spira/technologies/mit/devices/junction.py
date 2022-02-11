import spira.all as spira
from spira.yevon.geometry.route.routes import RouteStraight


from spira.technologies.mit import devices as dev
from spira.technologies.mit.process import RDD


__all__ = ['Junction']


class __Junction__(spira.Cell):
    """ Base class for Junction PCell. """

    radius = spira.NumberParameter()
    width = spira.NumberParameter(doc='Shunt resistance width')
    c5r = spira.Parameter(fdef_name='create_c5r')


class I5Contacts(__Junction__):
    """ Cell that contains all the vias of the bottom halve of the Junction. """

    i5 = spira.Parameter(fdef_name='create_i5')
    i6 = spira.Parameter(fdef_name='create_i6')

    sky_via = spira.BoolParameter(default=False)

    def create_i5(self):
        via = dev.ViaI5()
        V = spira.SRef(via, midpoint=(0,0))
        return V

    def create_i6(self):
        c = self.i5.midpoint
        w = (self.i5.reference.width + 4*RDD.I6.I5_MIN_SURROUND)
        via = dev.ViaI6(width=w, height=w)
        V = spira.SRef(via, midpoint=c)
        return V

    def create_c5r(self):
        # via = dev.ViaC5RA(width=self.width)
        via = dev.ViaC5RS()
        V = spira.SRef(via)
        if self.sky_via is True:
            V.connect(port=V.ports['R5:E0'], destination=self.i6.ports['M6:E2'], ignore_process=True)
        else:
            V.connect(port=V.ports['R5:E0'], destination=self.i5.ports['M5:E2'], ignore_process=True)
        return V

    def create_elements(self, elems):

        # Add the two via instances.
        elems += [self.i5, self.c5r]

        # Add the skyplane via instance if required.
        if self.sky_via is True:
            elems += self.i6

        # Add bounding box around all elements.
        box_shape = elems.bbox_info.bounding_box(margin=0.1)
        elems += spira.Polygon(shape=box_shape, layer=RDD.PLAYER.M6.METAL)

        return elems

    def create_ports(self, ports):
        ports += self.i5.ports['M5:E2'].copy(name='M5:P2')
        ports += self.c5r.ports['R5:E2'].copy(name='R5:P2')
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
        V.connect(port=V.ports['R5:E0'], destination=self.j5.ports['M5:E0'], ignore_process=True)
        return V

    def create_elements(self, elems):

        # Add the two via instances.
        elems += [self.j5, self.c5r]

        # Add bounding box around all elements.
        box_shape = elems.bbox_info.bounding_box(margin=0.1)
        elems += spira.Polygon(shape=box_shape, layer=RDD.PLAYER.M6.METAL)

        return elems

    def create_ports(self, ports):
        ports += self.j5.ports['M5:E0'].copy(name='M5:P0')
        ports += self.c5r.ports['R5:E2'].copy(name='R5:P2')
        return ports


class Junction(spira.Device):

    __name_prefix__ = 'Junction'

    length = spira.NumberParameter(default=1, doc='Length of the shunt resistance.')

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
    gnd_via = spira.BoolParameter(default=True)
    sky_via = spira.BoolParameter(default=False)

    def create_j5_cell(self):
        D = J5Contacts(width=self.width, radius=self.radius)
        S = spira.SRef(D)
        S.move(midpoint=S.ports['R5:P2'], destination=(0,0))
        return S

    def create_i5_cell(self):
        D = I5Contacts(width=self.width, radius=self.radius, sky_via=self.sky_via)
        S = spira.SRef(D)
        S.move(midpoint=S.ports['R5:P2'], destination=(0, self.length))
        return S

    def create_elements(self, elems):

        elems += self.i5
        elems += self.j5

        elems += RouteStraight(
            p1=self.i5.ports['R5:P2'].copy(width=self.width),
            p2=self.j5.ports['R5:P2'].copy(width=self.width),
            layer=RDD.PLAYER.R5.METAL)

        box_shape = elems.bbox_info.bounding_box(margin=0.3)
        m5_block = spira.Polygon(shape=box_shape, layer=RDD.PLAYER.M5.METAL)
        elems += m5_block
        i4 = dev.ViaI4()
        x,y = m5_block.center
        elems += spira.SRef(i4, midpoint=(x,y+0.35))
        #if self.gnd_via is True:
           # i4 = dev.ViaI4()
           # elems += spira.SRef(i4, midpoint=m5_block.center)

        return elems

    def create_ports(self, ports):
        ports += self.j5.ports['M6:E0'].copy(name='M6:P0')
        ports += self.j5.ports['M6:E1'].copy(name='M6:P1')
        ports += self.j5.ports['M6:E3'].copy(name='M6:P3')
        ports += self.i5.ports['M6:E1'].copy(name='M6:P4')
        ports += self.i5.ports['M6:E2'].copy(name='M6:P5')
        ports += self.i5.ports['M6:E3'].copy(name='M6:P6')
        return ports


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel', doc='Contains all the implemented junction devices.')

    # D = Junction(pcell=True)

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=D)

    # # v_model.view_virtual_connect(show_layers=False, write=True)
    # v_model.view_derived_contacts()
    # # v_model.view_derived_edges()

    # D = D.expand_flat_copy()

    # net = D.netlist

    # D.netlist_view(net=net)



    # -----------------------------------------------------------------

    # cell += spira.SRef(reference=j1, transformation=T)
    # cell += spira.SRef(reference=mask_cell)

    j2 = Junction(length=2, width=1.2, radius=1.4)
    cell += spira.SRef(j2, midpoint=(5, 0))
    D = j2()
    D.gdsii_output("filename")
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

    cell.gdsii_view()
    cell.gdsii_output(file_name='junction')









