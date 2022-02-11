from spira.yevon.process.all import *
from spira.yevon.process import get_rule_deck

RDD = get_rule_deck()

# FIXME: Move a geometry bridge class.
RDD.LCAR_DEVICE = 1
RDD.LCAR_CIRCUIT = 100

# ---------------------------------- GDSII ---------------------------------------

RDD.GDSII = ParameterDatabase()
RDD.GDSII.TEXT = 64
RDD.GDSII.UNIT = 1e-6
RDD.GDSII.GRID = 1e-12
RDD.GDSII.PRECISION = 1e-9

# ---------------------------------- Engines ---------------------------------------

RDD.ENGINE = ParameterDatabase()
RDD.ENGINE.SPICE = 'JOSIM_ENGINE'
RDD.ENGINE.GEOMETRY = 'GMSH_ENGINE'
RDD.ENGINE.IMPEDANCE = 'INDUCTEX_ENGINE'

# ---------------------------------- Process ---------------------------------------

RDD.PROCESS = ProcessLayerDatabase()

RDD.PROCESS.VIRTUAL = ProcessLayer(name='Virtual Layer', symbol='VIR')
RDD.PROCESS.LABEL = ProcessLayer(name='Contact 3', symbol='LBL')
RDD.PROCESS.PORT = ProcessLayer(name='IX Port', symbol='PRT')

RDD.PROCESS.GND = ProcessLayer(name='Ground Plane', symbol='GND')
RDD.PROCESS.SKY = ProcessLayer(name='Sky Plane', symbol='SKY')
RDD.PROCESS.R5 = ProcessLayer(name='Resistor 1', symbol='R5')
RDD.PROCESS.M0 = ProcessLayer(name='Metal 0', symbol='M0')
RDD.PROCESS.M1 = ProcessLayer(name='Metal 1', symbol='M1')
RDD.PROCESS.M2 = ProcessLayer(name='Metal 2', symbol='M2')
RDD.PROCESS.M3 = ProcessLayer(name='Metal 3', symbol='M3')
RDD.PROCESS.M4 = ProcessLayer(name='Metal 4', symbol='M4')
RDD.PROCESS.M5 = ProcessLayer(name='Metal 5', symbol='M5')
RDD.PROCESS.M6 = ProcessLayer(name='Metal 6', symbol='M6')
RDD.PROCESS.M7 = ProcessLayer(name='Metal 7', symbol='M7')
RDD.PROCESS.M8 = ProcessLayer(name='Metal 8', symbol='M8')
RDD.PROCESS.CM1 = ProcessLayer(name='Metal Contact 1', symbol='CM1')
RDD.PROCESS.CM2 = ProcessLayer(name='Metal Contact 2', symbol='CM2')
RDD.PROCESS.CM3 = ProcessLayer(name='Metal Contact 3', symbol='CM3')
RDD.PROCESS.I0 = ProcessLayer(name='Metal Contact 0', symbol='I0')
RDD.PROCESS.I1 = ProcessLayer(name='Metal Contact 1', symbol='I1')
RDD.PROCESS.I2 = ProcessLayer(name='Metal Contact 2', symbol='I2')
RDD.PROCESS.I3 = ProcessLayer(name='Metal Contact 3', symbol='I3')
RDD.PROCESS.I4 = ProcessLayer(name='Metal Contact 4', symbol='I4')
RDD.PROCESS.I5 = ProcessLayer(name='Metal Contact 5', symbol='I5')
RDD.PROCESS.I6 = ProcessLayer(name='Metal Contact 6', symbol='I6')
RDD.PROCESS.C5R = ProcessLayer(name='Resistor Contact 1', symbol='C5R')
RDD.PROCESS.C5J = ProcessLayer(name='Junction Contact 1', symbol='C5J')
RDD.PROCESS.J5 = ProcessLayer(name='Junction 1', symbol='J5')

# ---------------------------------- Layer Purposes ----------------------------------

RDD.PURPOSE = PurposeLayerDatabase()
RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', symbol='GND')
RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', symbol='METAL')
RDD.PURPOSE.DEVICE_METAL = PurposeLayer(name='Device metals', symbol='DEVICE_METAL')
RDD.PURPOSE.CIRCUIT_METAL = PurposeLayer(name='Circuit metals', symbol='CIRCUIT_METAL')
RDD.PURPOSE.ROUTE = PurposeLayer(name='Metal routes', symbol='ROUTE')
RDD.PURPOSE.RESISTOR = PurposeLayer(name='Polygon resistor', symbol='RES')
RDD.PURPOSE.SKY = PurposeLayer(name='Sky plane polygons', symbol='SKY')
RDD.PURPOSE.PROTECTION = PurposeLayer(name='Protection layer for via structures', symbol='PRO')
RDD.PURPOSE.VIA = PurposeLayer(name='Via layer', symbol='VIA')
RDD.PURPOSE.JUNCTION = PurposeLayer(name='Junction layer', symbol='JJ')
RDD.PURPOSE.NTRON = PurposeLayer(name='nTron layer', symbol='NTRON')
RDD.PURPOSE.HOLE = PurposeLayer(name='Polygon holes', symbol='HOLE')
RDD.PURPOSE.DUMMY = PurposeLayer(name='Sky plane polygons', symbol='DUM')
RDD.PURPOSE.BOUNDARY_BOX = PurposeLayer(name='Bounding Box', symbol='BBOX', doc='')
RDD.PURPOSE.INTERSECTED = PurposeLayer(name='Bounding Box', symbol='AND', doc='')
RDD.PURPOSE.UNION = PurposeLayer(name='Union', symbol='OR', doc='')
RDD.PURPOSE.DIFFERENCE = PurposeLayer(name='Bounding Box', symbol='NOR', doc='')

# ---------------------------------- Text Purposes ------------------------------------

RDD.PURPOSE.TEXT = PurposeLayerDatabase()
RDD.PURPOSE.TEXT.PIN = PurposeLayer(name='PinText', symbol='PT')
RDD.PURPOSE.TEXT.TERMINAL = PurposeLayer(name='PinText', symbol='TT')
RDD.PURPOSE.TEXT.EDGE = PurposeLayer(name='EdgeText', symbol='ET')
RDD.PURPOSE.TEXT.CONTACT = PurposeLayer(name='ContactText', symbol='CT')
RDD.PURPOSE.TEXT.ROUTE = PurposeLayer(name='RouteText', symbol='IT')
RDD.PURPOSE.TEXT.DUMMY = PurposeLayer(name='DummyText', symbol='DT')

# ---------------------------------- Port Purposes ------------------------------------

RDD.PURPOSE.PORT = PurposeLayerDatabase()
RDD.PURPOSE.PORT.PIN = PurposeLayer(name='PinPort', symbol='P')
RDD.PURPOSE.PORT.TERMINAL = PurposeLayer(name='TermPort', symbol='T')
RDD.PURPOSE.PORT.EDGE = PurposeLayer(name='EdgePort', symbol='E')
RDD.PURPOSE.PORT.CONTACT = PurposeLayer(name='ContactPort', symbol='C')
RDD.PURPOSE.PORT.ROUTE = PurposeLayer(name='RoutePort', symbol='I')
RDD.PURPOSE.PORT.BRANCH = PurposeLayer(name='BranchPort', symbol='B')
RDD.PURPOSE.PORT.DUMMY = PurposeLayer(name='DummyPort', symbol='D')
RDD.PURPOSE.PORT.INSIDE_EDGE_ENABLED = PurposeLayer(
    name='Enabled edge', symbol='EDGE_IE', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED = PurposeLayer(
    name='Disabled edge', symbol='EDGE_ID', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED = PurposeLayer(
    name='Enabled edge', symbol='EDGE_OE', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED = PurposeLayer(
    name='Disabled edge', symbol='EDGE_OD', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.TEXT_ENABLED = PurposeLayer(
    name='Enabled text', symbol='TEXT_E', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.TEXT_DISABLED = PurposeLayer(
    name='Disabled text', symbol='TEXT_D', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.DIRECTION = PurposeLayer(
    name='Arrow', symbol='DIR', doc='Layer that represents the direction of a polygon edge terminal.')
RDD.PURPOSE.PORT.IXPORT = PurposeLayer(name='IX port', symbol='PRT')
# -------------------------------- Error Purposes ------------------------------------

RDD.PURPOSE.ERROR = PurposeLayerDatabase()
RDD.PURPOSE.ERROR.SPACING = PurposeLayer(name='nTron layer', symbol='SP')
RDD.PURPOSE.ERROR.MIN_WIDTH = PurposeLayer(name='nTron layer', symbol='MAXW')
RDD.PURPOSE.ERROR.MAX_WIDTH = PurposeLayer(name='nTron layer', symbol='MINW')
RDD.PURPOSE.ERROR.ENCLOSURE = PurposeLayer(name='nTron layer', symbol='ENC')
RDD.PURPOSE.ERROR.OVERLAP = PurposeLayer(name='nTron layer', symbol='OVR')
RDD.PURPOSE.ERROR.DENSITY = PurposeLayer(name='nTron layer', symbol='OVR')

# ------------------------------- DEFAULT ----------------------------------

RDD.PLAYER = PhysicalLayerDatabase()

RDD.PORT = ParameterDatabase()
RDD.PORT.WIDTH = 0.5

# --------------------------------- Name Generator -------------------------------------

class TechAdminTree(LazyDatabase):
    """ A technology tree with a name generator. """
    def initialize(self):
        from spira.yevon.gdsii.generators import NameGenerator
        self.NAME_GENERATOR = NameGenerator(
            prefix_attribute='__name_prefix__',
            counter=0,
            process_name=''
        )

RDD.ADMIN = TechAdminTree()

# ----------------------------------- Filters -----------------------------------------

RDD.FILTERS = ParameterDatabase()

class PCellFilterDatabase(LazyDatabase):
    """ Define the filters that will be used when creating a spira.PCell object. """

    def initialize(self):
        from spira.yevon import filters

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.ProcessBooleanFilter(name='boolean', metal_purpose=RDD.PURPOSE.DEVICE_METAL)
        f += filters.SimplifyFilter(name='simplify')
        f += filters.ContactAttachFilter(name='contact_attach')

        f['boolean'] = True
        f['simplify'] = True
        f['contact_attach'] = True

        self.DEVICE = f

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.ProcessBooleanFilter(name='boolean', metal_purpose=RDD.PURPOSE.CIRCUIT_METAL)
        f += filters.SimplifyFilter(name='simplify')

        f['boolean'] = True
        f['simplify'] = True

        self.CIRCUIT = f

        f = filters.ToggledCompositeFilter(name='mask_filters', filters=[])
        f += filters.ElectricalAttachFilter(name='erc')
        f += filters.PinAttachFilter(name='pin_attach')
        f += filters.DeviceMetalFilter(name='device_metal')

        f['erc'] = True
        f['pin_attach'] = True
        f['device_metal'] = False

        self.MASK = f

RDD.FILTERS.PCELL = PCellFilterDatabase()


class OutputFilterDatabase(LazyDatabase):
    """ Define the filters that will be used when creating a spira.PCell object. """

    def initialize(self):
        from spira.yevon import filters

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.PortCellFilter(name='cell_ports')
        f += filters.PortPolygonEdgeFilter(name='edge_ports')
        f += filters.PortPolygonContactFilter(name='contact_ports')

        f['cell_ports'] = True
        f['edge_ports'] = True
        f['contat_ports'] = True

        self.PORTS = f

RDD.FILTERS.OUTPUT = OutputFilterDatabase()
