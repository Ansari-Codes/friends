from comps import CompFooter, CompHeader
from comps.Welcome import CompHero
from UI import INIT_THEME

async def create():
    INIT_THEME()
    CompHeader.CompHeader()
    CompHero.CompHero()
    CompFooter.CompFooter()
