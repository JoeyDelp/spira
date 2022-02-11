import spira.all as spira
from copy import deepcopy
from spira.yevon.geometry import shapes
from spira.yevon.visualization import color


from spira.technologies.mit.process import RDD


class JJ(spira.Device):
    """ Via component for the AIST process. """
    
    __name_prefix__ = 'Jj'

    width = spira.NumberParameter(
        default=RDD.J5.MIN_SIZE+2*RDD.J5.C5J_MIN_SURROUND, 
        restriction=spira.RestrictRange(lower=RDD.C5J.MIN_SIZE+2*RDD.J5.C5J_MIN_SURROUND, upper=RDD.J5.MAX_SIZE)
    )

    jj_radius = spira.Parameter(fdef_name='create_jj_radius', doc='Width of the via layer polygon.')
    c5j_radius = spira.Parameter(fdef_name='create_c5j_radius', doc='Width of the via layer polygon.')

    m5_width = spira.Parameter(fdef_name='create_m5_width', doc='Width of the via layer polygon.')
    m6_width = spira.Parameter(fdef_name='create_m6_width', doc='Width of the via layer polygon.')

    def create_jj_radius(self):
        return (self.width/2)

    def create_c5j_radius(self):
        return self.jj_radius - RDD.J5.C5J_MIN_SURROUND

    def create_m5_width(self):
        return 2*(self.jj_radius + RDD.M5.J5_MIN_SURROUND)

    def create_m6_width(self):
        return 2*(self.c5j_radius + RDD.C5J.M6_MIN_SURROUND)

    def create_elements(self, elems):
        elems += spira.Circle(layer=RDD.PLAYER.C5J.VIA, box_size=[2*self.c5j_radius, 2*self.c5j_radius])
        elems += spira.Circle(layer=RDD.PLAYER.J5.JUNCTION, box_size=[2*self.jj_radius, 2*self.jj_radius])
        elems += spira.Box(alias='M5', layer=RDD.PLAYER.M5.METAL, width=self.m5_width, height=self.m5_width)
        elems += spira.Box(alias='M6', layer=RDD.PLAYER.M6.METAL, width=self.m6_width, height=self.m6_width)
        return elems

    def create_ports(self, ports):
        p0 = self.elements['M5'].ports.unlock
        p1 = self.elements['M6'].ports.unlock
        return ports


class ViaC5RA(spira.Device):
    """ Via component for the MiTLL process. """

    __name_prefix__ = 'C5R_Alternative'

    width = spira.NumberParameter(default=RDD.R5.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.R5.MIN_SIZE))

    height = spira.Parameter(fdef_name='create_height')
    via_width = spira.Parameter(fdef_name='create_via_width')
    via_height = spira.Parameter(fdef_name='create_via_height')

    m6_width = spira.Parameter(fdef_name='create_m6_width', doc='Width of the via layer polygon.')
    m6_height = spira.Parameter(fdef_name='create_m6_height', doc='Width of the via layer polygon.')

    def create_m6_width(self):
        return (self.via_width + 2*RDD.C5R.M6_MIN_SURROUND)

    def create_via_width(self):
        return (self.width + 2*RDD.C5R.R5_MAX_SIDE_SURROUND)

    def create_via_height(self):
        return RDD.C5R.MIN_SIZE

    def create_height(self):
        return self.via_height + 2*RDD.R5.C5R_MIN_SURROUND

    def create_elements(self, elems):
        elems += spira.Box(layer=RDD.PLAYER.C5R.VIA, width=self.via_width, height=self.via_height)
        elems += spira.Box(alias='M6', layer=RDD.PLAYER.M6.METAL, width=self.m6_width, height=self.height)
        elems += spira.Box(alias='R5', layer=RDD.PLAYER.R5.METAL, width=self.width, height=self.height,)
        return elems

    def create_ports(self, ports):
        p0 = self.elements['M6'].ports.unlock
        p1 = self.elements['R5'].ports.unlock
        return ports


class ViaC5RS(spira.Device):
    """ Via component for the AIST process. """

    __name_prefix__ = 'C5R_Standard'

    width = spira.NumberParameter(default=RDD.C5R.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.C5R.MIN_SIZE))
    height = spira.NumberParameter(default=RDD.C5R.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.C5R.MIN_SIZE))

    r5_width = spira.Parameter(fdef_name='create_r5_width', doc='Width of the via layer polygon.')
    r5_height = spira.Parameter(fdef_name='create_r5_height', doc='Width of the via layer polygon.')

    m6_width = spira.Parameter(fdef_name='create_m6_width', doc='Width of the via layer polygon.')
    m6_height = spira.Parameter(fdef_name='create_m6_height', doc='Width of the via layer polygon.')

    def create_m6_width(self):
        return (self.width + 2*RDD.C5R.M6_MIN_SURROUND)

    def create_m6_height(self):
        return (self.height + 2*RDD.C5R.M6_MIN_SURROUND)

    def create_r5_width(self):
        return (self.width + 2*RDD.R5.C5R_MIN_SURROUND)

    def create_r5_height(self):
        return (self.height + 2*RDD.R5.C5R_MIN_SURROUND)

    def create_elements(self, elems):
        elems += spira.Box(layer=RDD.PLAYER.C5R.VIA, width=self.width, height=self.height)
        elems += spira.Box(alias='M6', layer=RDD.PLAYER.M6.METAL, width=self.m6_width, height=self.m6_height)
        elems += spira.Box(alias='R5', layer=RDD.PLAYER.R5.METAL, width=self.r5_width, height=self.r5_height)
        return elems

    def create_ports(self, ports):
        # ports += self.elements['R5'].ports['E0_R5'].copy(name='P0')
        # ports += self.elements['R5'].ports['E2_R5'].copy(name='P2')
        # print('\n--------')
        # print(self.elements)
        # print(self.elements['R5'].edge_ports)
        ports += self.elements['R5'].edge_ports['R5:E0'].copy(name='P0')
        ports += self.elements['R5'].edge_ports['R5:E2'].copy(name='P2')
        return ports


class ViaI4(spira.Device):
    """ Via component for the AIST process. """
    
    __name_prefix__ = 'I4'

    width = spira.NumberParameter(default=RDD.I4.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.I4.MIN_SIZE))
    height = spira.NumberParameter(default=RDD.I4.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.I4.MIN_SIZE))

    m4_width = spira.Parameter(fdef_name='create_m4_width', doc='Width of the via layer polygon.')
    m4_height = spira.Parameter(fdef_name='create_m4_height', doc='Width of the via layer polygon.')
    
    m5_width = spira.Parameter(fdef_name='create_m5_width', doc='Width of the via layer polygon.')
    m5_height = spira.Parameter(fdef_name='create_m5_height', doc='Width of the via layer polygon.')

    def create_m4_width(self):
        return (self.width + 2*RDD.M4.I4_MIN_SURROUND)

    def create_m5_width(self):
        return (self.width + 2*RDD.I4.M5_MIN_SURROUND)

    def create_m4_height(self):
        return (self.height + 2*RDD.M4.I4_MIN_SURROUND)

    def create_m5_height(self):
        return (self.height + 2*RDD.I4.M5_MIN_SURROUND)

    def create_elements(self, elems):
        elems += spira.Box(layer=RDD.PLAYER.I4.VIA, width=self.width, height=self.height)
        elems += spira.Box(alias='M4', layer=RDD.PLAYER.M4.GND, width=self.m4_width, height=self.m4_height)
        elems += spira.Box(alias='M5', layer=RDD.PLAYER.M5.METAL, width=self.m5_width, height=self.m5_height)
        return elems

    def create_ports(self, ports):
        p0 = self.elements['M5'].ports.unlock
        p1 = self.elements['M4'].ports.unlock
        return ports


class ViaI5(spira.Device):
    """ Via component for the AIST process. """
    
    __name_prefix__ = 'I5'

    width = spira.NumberParameter(default=RDD.I5.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.I5.MIN_SIZE))
    height = spira.NumberParameter(default=RDD.I5.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.I5.MIN_SIZE))

    m6_width = spira.Parameter(fdef_name='create_m6_width', doc='Width of the via layer polygon.')
    m6_height = spira.Parameter(fdef_name='create_m6_height', doc='Width of the via layer polygon.')

    m5_width = spira.Parameter(fdef_name='create_m5_width', doc='Width of the via layer polygon.')
    m5_height = spira.Parameter(fdef_name='create_m5_height', doc='Width of the via layer polygon.')

    def create_m6_width(self):
        return (self.width + 2*RDD.M5.MIN_SURROUND_OF_I5)

    def create_m5_width(self):
        return (self.width + 2*RDD.I5.MIN_SURROUND_BY_M6)

    def create_m6_height(self):
        return (self.height + 2*RDD.M5.MIN_SURROUND_OF_I5)

    def create_m5_height(self):
        return (self.height + 2*RDD.I5.MIN_SURROUND_BY_M6)

    def create_elements(self, elems):
        elems += spira.Box(layer=RDD.PLAYER.I5.VIA, width=self.width, height=self.height)
        elems += spira.Box(alias='M5', layer=RDD.PLAYER.M5.METAL, width=self.m6_width, height=self.m6_height)
        elems += spira.Box(alias='M6', layer=RDD.PLAYER.M6.METAL, width=self.m6_width, height=self.m6_height)
        return elems

    def create_ports(self, ports):
        # FIXME: Causes Pin label adding to netlist. Must be filtered or suspended.
        # ports += self.elements['M5'].ports.unlock
        # ports += self.elements['M6'].ports.unlock
        ports += self.elements['M5'].edge_ports.unlock
        ports += self.elements['M6'].edge_ports.unlock
        # print(ports)
        return ports


class ViaI6(spira.Device):
    """ Via component for the AIST process. """

    __name_prefix__ = 'I6'

    width = spira.NumberParameter(default=RDD.I6.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.I6.MIN_SIZE))
    height = spira.NumberParameter(default=RDD.I6.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.I6.MIN_SIZE))

    m6_width = spira.Parameter(fdef_name='create_m6_width', doc='Width of the via layer polygon.')
    m6_height = spira.Parameter(fdef_name='create_m6_height', doc='Width of the via layer polygon.')

    m7_width = spira.Parameter(fdef_name='create_m7_width', doc='Width of the via layer polygon.')
    m7_height = spira.Parameter(fdef_name='create_m7_height', doc='Width of the via layer polygon.')

    def create_m6_width(self):
        return (self.width + 2*RDD.M6.I6_MIN_SURROUND)

    def create_m7_width(self):
        return (self.width + 2*RDD.I6.M7_MIN_SURROUND)

    def create_m6_height(self):
        return (self.height + 2*RDD.M6.I6_MIN_SURROUND)

    def create_m7_height(self):
        return (self.height + 2*RDD.I6.M7_MIN_SURROUND)

    def create_elements(self, elems):
        elems += spira.Box(layer=RDD.PLAYER.I6.VIA, width=self.width, height=self.height)
        elems += spira.Box(alias='M6', layer=RDD.PLAYER.M6.METAL, width=self.m6_width, height=self.m6_height)
        elems += spira.Box(alias='M7', layer=RDD.PLAYER.M7.METAL, width=self.m7_width, height=self.m7_height)
        return elems

    def create_ports(self, ports):
        p0 = self.elements['M6'].ports.unlock
        p1 = self.elements['M7'].ports.unlock
        return ports


if __name__ == '__main__':

    cell = spira.Cell(name='ViaDevices', doc='Contains all the implemented via devices.')

    v1 = ViaC5RA()
    v1_ref = spira.SRef(v1, midpoint=(0,0))
    cell += v1_ref

    v2 = ViaC5RS()
    v2_ref = spira.SRef(v2, midpoint=(0,5))
    cell += v2_ref

    i4 = ViaI4()
    i4_ref = spira.SRef(i4, midpoint=(5,0))
    cell += i4_ref

    i5 = ViaI5()
    i5_ref = spira.SRef(i5, midpoint=(10,0))
    cell += i5_ref

    i6 = ViaI6()
    i6_ref = spira.SRef(i6, midpoint=(15,0))
    cell += i6_ref

    jj = JJ()
    jj_ref = spira.SRef(jj, midpoint=(20,0))
    cell += jj_ref

    cell.gdsii_output(file_name='ViaC5RA')



