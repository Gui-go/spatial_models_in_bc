"""
Scrap of Balneário Camboriú real state data
"""

from vr_class import VR


if __name__ == '__main__':
    primeira_pagina='https://www.vivareal.com.br/venda/santa-catarina/florianopolis/apartamento_residencial/?__vt=lnv:c'
    vr = VR(primeira_pagina)
    vr.run(270)

