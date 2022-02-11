import numpy as np
import spira.all as spira
from spira.yevon.visualization import color

from spira.technologies.mit import devices as dev
from spira.technologies.mit.process.database import RDD


class MetalBlock(spira.Cell):
    """ Place a metal layer around the defined contact layers. """

    margin = spira.NumberParameter(default=0.0, doc='Margin value between metal layer and nearest contact layers.')
    layer = spira.PhysicalLayerParameter(default=RDD.PLAYER.M6, doc='Metal layer to be wrapped around the cell bounding box.')

    def create_elements(self, elems):
        # cell = spira.Cell(elements=elems.flatten())
        cell = spira.Cell(elements=elems)
        bb = cell.bbox
        margin = self.margin
        p1 = [bb[0][0]-margin, bb[0][1]-margin]
        p2 = [bb[1][0]+margin, bb[1][1]+margin]
        alias = self.layer.layer.name
        # alias = '{}_{}'.format(self.layer.layer.name, self.alias)
        elems = pc.Rectangle(alias=alias, layer=self.layer, p1=p1, p2=p2)
        return elems


class __Junction__(spira.Cell):
    """ Base class for Junction PCell. """

    radius = spira.FloatParameter()
    width = spira.FloatParameter(doc='Shunt resistance width')
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
        via = dev.ViaC5RA(width=self.width)
        V = spira.SRef(via)
        V.connect(port=V.ports['R5_e0'], destination=self.i5.ports['M5_e2'])
        return V

    def create_elements(self, elems):
        elems += self.i5
        elems += self.c5r
        if self.sky_via is True:
            elems += self.i6
        elems += MetalBlock(layer=RDD.PLAYER.M6).create_elements(elems)
        return elems

    def create_ports(self, ports):
        ports += self.i5.ports['M5_e2']
        ports += self.c5r.ports['R5_e2']
        return ports


class J5Contacts(__Junction__):
    """ Cell that contains all the vias of the top halve of the Junction. """

    j5 = spira.Parameter(fdef_name='create_j5')

    def create_j5(self):
        jj = dev.JJ(width=2*self.radius)
        D = spira.SRef(jj, midpoint=(0,0))
        return D

    def create_c5r(self):
        via = dev.ViaC5RA(width=self.width)
        V = spira.SRef(via)
        V.connect(port=V.ports['R5_e0'], destination=self.j5.ports['M5_e0'])
        return V

    def create_elements(self, elems):
        elems += self.j5
        elems += self.c5r
        elems += MetalBlock(layer=RDD.PLAYER.M6).create_elements(elems)
        return elems

    def create_ports(self, ports):
        ports += self.j5.ports['M5_e0']
        ports += self.c5r.ports['R5_e2']
        for p in self.elements['M6'].ports:
            ports += p.copy(name=p.name)
        return ports


class Junction(spira.Circuit):

    __name_prefix__ = 'Junction'

    color = spira.ColorParameter(default=color.COLOR_PLUM, doc='The color of the Junction representative node in a graph network (netlist).')
    text_type = spira.NumberParameter(default=91)

    length = spira.NumberParameter(default=1, doc='Length of the shunt resistance.')
    width = spira.NumberParameter(default=RDD.R5.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.R5.MIN_SIZE, upper=RDD.R5.MAX_WIDTH), doc='Width of the shunt resistance.')
    radius = spira.NumberParameter(default=RDD.J5.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.J5.MIN_SIZE, upper=RDD.J5.MAX_SIZE), doc='Radius of the circular junction layer.')

    i5 = spira.Parameter(fdef_name='create_i5_cell')
    j5 = spira.Parameter(fdef_name='create_j5_cell')

    gnd_via = spira.BoolParameter(default=False)
    sky_via = spira.BoolParameter(default=False)

    def create_i5_cell(self):
        D = I5Contacts(width=self.width, radius=self.radius, sky_via=self.sky_via)
        S = spira.SRef(D)
        S.move(midpoint=S.ports['R5_e2'], destination=(0, self.length))
        return S

    def create_j5_cell(self):
        D = J5Contacts(width=self.width, radius=self.radius)
        S = spira.SRef(D)
        S.move(midpoint=S.ports['R5_e2'], destination=(0,0))
        return S

    def create_elements(self, elems):
        R = spira.Route(
            port1=self.i5.ports['R5_e2'],
            port2=self.j5.ports['R5_e2'],
            width=self.width,
            layer=RDD.PLAYER.R5
        )
        elems += spira.SRef(R)

        elems += self.i5
        elems += self.j5

        m5 = MetalBlock(layer=RDD.PLAYER.M5, margin=0.1).create_elements(elems)
        elems += m5

        if self.gnd_via is True:
            i4 = dev.ViaI4()
            elems += spira.SRef(i4, midpoint=m5.center)

        return elems

    def create_ports(self, ports):
        for p in self.j5.ports:
            if p.name == 'M6_e1':
                el = p.edgelayer.copy(datatype=199)
                ports += p.copy(name='P2', text_type=self.text_type, edgelayer=el)
            if p.name == 'M6_e3':
                el = p.edgelayer.copy(datatype=199)
                ports += p.copy(name='P1', text_type=self.text_type, edgelayer=el)
        return ports


from spira.netex.containers import __CellContainer__
class Connector(__CellContainer__):
    """ Contains the expanded cell for connection detection. """

    def create_elements(self, elems):
        elems = self.cell.elements
        return elems

    def create_ports(self, ports):
        elems = self.cell.elements
        # ports = elems[0].ports & elems[1]
        # ports = elems[0].ports
        for i in range(len(elems)):
            for j in range(len(elems)):
                if i != j:
                    e1 = elems[i]
                    e2 = elems[j]
                    if e1.layer == e2.layer:
                        if e1.layer.layer.number == 60:
                            pl = elems[i].ports & elems[j]
                            for p in pl:
                                ports += p
        return ports


if __name__ == '__main__':

    cell = spira.Cell(name='Junction', doc='Contains all the implemented junction devices.')

    T = spira.Rotation(0)

    j1 = Junction()
    S = spira.SRef(j1, midpoint=(0, 0), transformation=T)

    # D = S.expand_flat_copy()
    # D.gdsii_output()
    
    # connector = Connector(cell=D)
    # # connector.ports
    # connector.gdsii_output()

    cell += S
    cell.gdsii_output()

    # j1 = Junction()
    # cell += spira.SRef(j1, midpoint=(0, 0), transformation=T)

    # j2 = Junction(length=1.5)
    # cell += spira.SRef(j2, midpoint=(5, 0), transformation=T)

    # j3 = Junction(width=1.2)
    # cell += spira.SRef(j3, midpoint=(10, 0), transformation=T)

    # j4 = Junction(radius=1.2)
    # cell += spira.SRef(j4, midpoint=(15,0), transformation=T)

    # j5 = Junction(gnd_via=True)
    # cell += spira.SRef(j5, midpoint=(20,0), transformation=T)

    # j6 = Junction(sky_via=True)
    # cell += spira.SRef(j6, midpoint=(25,0), transformation=T)

    # j7 = Junction(gnd_via=True, sky_via=True)
    # cell += spira.SRef(j7, midpoint=(30,0), transformation=T)

    # print(Junction.length.__doc__)
    # print(Junction.width.__doc__)
    # print(Junction.radius.__doc__)

    # cell.gdsii_output()









