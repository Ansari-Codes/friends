from comps import CompFooter, CompHeader
from comps.Welcome import CompHero
from UI import INIT_THEME

async def create():
    await INIT_THEME()
    CompHeader.CompHeader()
    await CompHero.CompHero()
    CompFooter.CompFooter()
