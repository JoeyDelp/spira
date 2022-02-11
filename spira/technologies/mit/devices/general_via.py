import spira.all as spira


from spira.technologies.mit.process import RDD


class GeneralVia(spira.Cell):
    """  """

    symbol = spira.StringParameter()
    bot_layer = spira.LayerParameter()
    top_layer = spira.LayerParameter()
    via_layer = spira.LayerParameter()

    def get_constructor_layer_mapping(self):
        cl1 = self.bot_layer & self.top_layer & self.via_layer
        # cl2 = self.bot_layer ~ self.via_layer
        # cl3 = self.bot_layer ~ self.via_layer
        mapping = {
            cl1 : RDD.PLAYER[self.symbol].UNION
        }
        return mapping

    def create_elements(self, elems):

        m1_params = RDD[self.bot_layer.process.symbol]
        m2_params = RDD[self.top_layer.process.symbol]
        via_params = RDD[self.via_layer.process.symbol]

        print(m1_params.items)

        # elems += spira.Box(alias=via_layer.process.symbol, layer=via_layer, width=self.m5_width, height=self.m5_width)

        return elems


def generate_list_of_default_vias():

    for layer in RDD.get_physical_layers_by_purpose(purposes=['VIA']):
        print(layer)


gv = generate_list_of_default_vias()


# print('\n--- Layer keys:')
# for k in RDD.keys:
#     print(k)

print('\n--- Via keys:')
for k1 in RDD.VIAS.keys:

    V = GeneralVia(
        symbol=k1,
        bot_layer=RDD.VIAS[k1]['BOT_LAYER'],
        top_layer=RDD.VIAS[k1]['TOP_LAYER'],
        via_layer=RDD.VIAS[k1]['VIA_LAYER'],
    )

    print(V.get_constructor_layer_mapping())



    

